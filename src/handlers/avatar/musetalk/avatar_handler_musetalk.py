import os

# xformers has a strict flash-attn version window check that may reject
# newer ABI-compatible releases.  Bypass it so the two libraries coexist.
os.environ.setdefault("XFORMERS_IGNORE_FLASH_VERSION_CHECK", "1")

import hashlib
from typing import Dict, List, Optional, cast
import numpy as np
from loguru import logger
import threading

from chat_engine.data_models.chat_data_type import ChatDataType, EngineChannelType
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail, \
    ChatDataConsumeMode
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry, DataBundle, VariableSize
from handlers.avatar.musetalk.musetalk_data_models import (
    MuseTalkSpeechAudio, MuseTalkProcessorCallbacks,
)
from handlers.avatar.musetalk.musetalk_processor import AvatarMuseTalkProcessor
from handlers.avatar.musetalk.musetalk_algo import MuseTalkAlgoV15
from handlers.avatar.musetalk.musetalk_config import AvatarMuseTalkConfig
from engine_utils.general_slicer import slice_data, SliceContext


class MuseTalkProcessorPool:
    """Pool of AvatarMuseTalkProcessor instances for multi-session support."""

    def __init__(self, avatar: MuseTalkAlgoV15, config: AvatarMuseTalkConfig, pool_size: int):
        self._lock = threading.Lock()
        self._processors: List[AvatarMuseTalkProcessor] = []
        self._active: List[bool] = []
        for _ in range(pool_size):
            self._processors.append(AvatarMuseTalkProcessor(avatar, config))
            self._active.append(False)
        logger.info(f"MuseTalkProcessorPool created with {pool_size} processors")

    def acquire(self) -> Optional[AvatarMuseTalkProcessor]:
        with self._lock:
            for i, active in enumerate(self._active):
                if not active:
                    self._active[i] = True
                    logger.info(f"MuseTalkProcessorPool: acquired processor {i}")
                    return self._processors[i]
        logger.warning("MuseTalkProcessorPool: no available processor")
        return None

    def release(self, processor: AvatarMuseTalkProcessor):
        with self._lock:
            for i, p in enumerate(self._processors):
                if p is processor:
                    self._active[i] = False
                    logger.info(f"MuseTalkProcessorPool: released processor {i}")
                    return
        logger.warning("MuseTalkProcessorPool: processor not found in pool")

    def destroy(self):
        for p in self._processors:
            try:
                p.stop()
            except Exception as e:
                logger.opt(exception=True).warning(f"Error stopping processor during pool destroy: {e}")


class AvatarMuseTalkContext(HandlerContext):
    """Per-session context for MuseTalk avatar handler."""

    def __init__(self, session_id: str, processor: AvatarMuseTalkProcessor):
        super().__init__(session_id)
        self.config: Optional[AvatarMuseTalkConfig] = None
        self.processor = processor
        self.input_slice_context: Optional[SliceContext] = None
        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}

        self._current_tts_stream_key: Optional[str] = None
        self._stream_key_lock = threading.Lock()
        self._playback_streamer = None

    def init_playback_streamer(self):
        """Eagerly create a CLIENT_PLAYBACK lifecycle streamer. Must be called after stream_manager is set."""
        if self._playback_streamer is None and self.stream_manager is not None:
            self._playback_streamer = self.stream_manager.create_lifecycle_streamer(
                data_type=ChatDataType.CLIENT_PLAYBACK,
                producer_name="AvatarMuseTalk",
                config=ChatStreamConfig(cancelable=False),
            )
        return self._playback_streamer

    def get_playback_streamer(self):
        return self._playback_streamer

    def _build_callbacks(self) -> MuseTalkProcessorCallbacks:
        """Build callbacks that bridge Processor output to engine's submit_data."""
        def on_video_frame(frame: np.ndarray):
            self._return_data(frame, ChatDataType.AVATAR_VIDEO)

        def on_audio_frame(audio_data: np.ndarray):
            self._return_data(audio_data, ChatDataType.AVATAR_AUDIO)

        def on_speech_end(speech_id: str):
            streamer = self.get_playback_streamer()
            with self._stream_key_lock:
                current_key = self._current_tts_stream_key
                if current_key is None:
                    logger.debug(f"MuseTalk: on_speech_end ignored (no active stream, likely interrupted): speech_id={speech_id}")
                    return
                if speech_id is not None and speech_id != current_key:
                    logger.warning(f"MuseTalk: on_speech_end speech_id mismatch, "
                                   f"callback={speech_id}, current={current_key}, skip closing")
                    return
                self._current_tts_stream_key = None
            if streamer is not None:
                streamer.finish_current()
                logger.info(f"MuseTalk: CLIENT_PLAYBACK stream closed for stream_key={current_key}")

        return MuseTalkProcessorCallbacks(
            on_video_frame=on_video_frame,
            on_audio_frame=on_audio_frame,
            on_speech_end=on_speech_end,
        )

    def _return_data(self, data: np.ndarray, chat_data_type: ChatDataType) -> None:
        """Package and submit output data for downstream consumption."""
        definition = self.output_data_definitions.get(chat_data_type)
        if definition is None:
            logger.error(f"Definition is None, chat_data_type={chat_data_type}")
            return
        data_bundle = DataBundle(definition)
        if chat_data_type.channel_type == EngineChannelType.AUDIO:
            if data is not None:
                if data.dtype != np.float32:
                    logger.warning("Audio data dtype is not float32")
                    data = data.astype(np.float32)
                if data.ndim == 1:
                    logger.warning("Audio data ndim is 1")
                    data = data[np.newaxis, ...]
                elif data.ndim == 2 and data.shape[0] != 1:
                    logger.warning("Audio data shape is not [1, N]")
                    data = data[:1, ...]
            else:
                logger.error("Audio data is None")
                data = np.zeros([1, 0], dtype=np.float32)
            data_bundle.set_main_data(data)
        elif chat_data_type.channel_type == EngineChannelType.VIDEO:
            data_bundle.set_main_data(data[np.newaxis, ...])
        else:
            return
        chat_data = ChatData(type=chat_data_type, data=data_bundle)
        self.submit_data(chat_data)

    def interrupt(self):
        """Interrupt current speech: close playback stream, stop pipeline, clear slicer state.

        Called when CLIENT_PLAYBACK stream is cancelled (via STREAM_CANCEL signal).
        The stream may already be cancelled externally; finish_current() is a safe no-op in that case.
        """
        logger.info("MuseTalk interrupt: notifying processor")
        with self._stream_key_lock:
            self._current_tts_stream_key = None
        if self._playback_streamer is not None:
            self._playback_streamer.finish_current()
        if self.processor is not None:
            self.processor.interrupt()
        if self.input_slice_context is not None:
            discarded = self.input_slice_context.flush()
            if discarded is not None:
                logger.info(f"MuseTalk interrupt: discarded {len(discarded)} samples from input slicer remainder")
        logger.info("MuseTalk interrupt: done")

    def clear(self) -> None:
        logger.info("Clear musetalk context")


class HandlerAvatarMuseTalk(HandlerBase):
    def __init__(self) -> None:
        super().__init__()
        self.avatar: Optional[MuseTalkAlgoV15] = None
        self.processor_pool: Optional[MuseTalkProcessorPool] = None
        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}
        self._handler_config: Optional[AvatarMuseTalkConfig] = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=AvatarMuseTalkConfig,
            load_priority=-999,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[AvatarMuseTalkConfig] = None):
        if not isinstance(handler_config, AvatarMuseTalkConfig):
            handler_config = AvatarMuseTalkConfig()
        self._handler_config = handler_config

        audio_output_definition = DataBundleDefinition()
        audio_output_definition.add_entry(DataBundleEntry.create_audio_entry(
            "avatar_muse_audio", 1, handler_config.output_audio_sample_rate,
        ))
        audio_output_definition.lockdown()
        self.output_data_definitions[ChatDataType.AVATAR_AUDIO] = audio_output_definition

        video_output_definition = DataBundleDefinition()
        video_output_definition.add_entry(DataBundleEntry.create_framed_entry(
            "avatar_muse_video",
            [VariableSize(), VariableSize(), VariableSize(), 3],
            0, handler_config.fps,
        ))
        video_output_definition.lockdown()
        self.output_data_definitions[ChatDataType.AVATAR_VIDEO] = video_output_definition

        project_root = os.getcwd()
        model_dir = os.path.join(project_root, handler_config.model_dir)
        vae_type = "sd-vae"
        unet_model_path = os.path.join(model_dir, "musetalkV15", "unet.pth")
        unet_config = os.path.join(model_dir, "musetalkV15", "musetalk.json")
        whisper_dir = os.path.join(model_dir, "whisper")
        result_dir = os.path.join(project_root, handler_config.avatar_model_dir)

        video_path = handler_config.avatar_video_path
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        video_hash = hashlib.md5(video_path.encode()).hexdigest()[:8]
        auto_avatar_id = f"avatar_{video_basename}_{video_hash}"
        logger.info(f"Auto generated avatar_id: {auto_avatar_id}")

        self.avatar = MuseTalkAlgoV15(
            avatar_id=auto_avatar_id,
            video_path=handler_config.avatar_video_path,
            bbox_shift=0,
            batch_size=handler_config.batch_size,
            force_preparation=handler_config.force_create_avatar,
            parsing_mode="jaw",
            left_cheek_width=90, right_cheek_width=90,
            audio_padding_length_left=2, audio_padding_length_right=2,
            fps=handler_config.fps,
            version="v15",
            result_dir=result_dir,
            extra_margin=10,
            vae_type=vae_type,
            unet_model_path=unet_model_path,
            unet_config=unet_config,
            whisper_dir=whisper_dir,
            gpu_id=0,
            debug=handler_config.debug,
        )

        self.processor_pool = MuseTalkProcessorPool(
            self.avatar, handler_config, handler_config.concurrent_limit,
        )
        logger.info(
            f"HandlerAvatarMuseTalk loaded: avatar ready, processor pool size={handler_config.concurrent_limit}")

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[AvatarMuseTalkConfig] = None) -> HandlerContext:
        if not isinstance(handler_config, AvatarMuseTalkConfig):
            handler_config = AvatarMuseTalkConfig()

        processor = self.processor_pool.acquire()
        if processor is None:
            raise RuntimeError(
                f"No available MuseTalk processor. "
                f"concurrent_limit={self._handler_config.concurrent_limit} reached."
            )

        try:
            context = AvatarMuseTalkContext(
                session_context.session_info.session_id,
                processor,
            )
            context.output_data_definitions = self.output_data_definitions
            context.config = handler_config

            callbacks = context._build_callbacks()
            processor.set_callbacks(callbacks)

            output_audio_sample_rate = handler_config.output_audio_sample_rate
            fps = handler_config.fps
            assert output_audio_sample_rate % fps == 0, (
                f"output_audio_sample_rate ({output_audio_sample_rate}) must be divisible by "
                f"fps ({fps}). This should have been auto-corrected by AvatarMuseTalkConfig."
            )

            context.input_slice_context = SliceContext.create_numpy_slice_context(
                slice_size=output_audio_sample_rate,
                slice_axis=0,
            )
            logger.info(f"Context created for session {session_context.session_info.session_id}")
            return context
        except Exception:
            processor.set_callbacks(None)
            self.processor_pool.release(processor)
            raise

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        context = cast(AvatarMuseTalkContext, handler_context)
        context.init_playback_streamer()
        context.processor.start()
        logger.info(f"Context started, processor running for session {context.session_id}")

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        """Return handler input/output data type details."""
        context = cast(AvatarMuseTalkContext, context)
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                input_consume_mode=ChatDataConsumeMode.ONCE,
            )
        }
        outputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=context.output_data_definitions[ChatDataType.AVATAR_AUDIO],
            ),
            ChatDataType.AVATAR_VIDEO: HandlerDataInfo(
                type=ChatDataType.AVATAR_VIDEO,
                definition=context.output_data_definitions[ChatDataType.AVATAR_VIDEO],
                output_stream_config=ChatStreamConfig(cancelable=False, auto_link_input=False),
            ),
        }
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
            signal_filters=[
                # 监听 CLIENT_PLAYBACK 的 STREAM_CANCEL 信号（用于打断）
                SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, ChatDataType.CLIENT_PLAYBACK),
            ]
        )

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """Process audio input and send to processor."""
        if inputs.type != ChatDataType.AVATAR_AUDIO:
            return
        context = cast(AvatarMuseTalkContext, context)

        stream_key_str = inputs.stream_id.stream_key_str if inputs.stream_id else None
        with context._stream_key_lock:
            prev_key = context._current_tts_stream_key
            need_switch = bool(stream_key_str and stream_key_str != prev_key)
            if need_switch:
                context._current_tts_stream_key = stream_key_str
        if need_switch:
            if context.input_slice_context is not None:
                discarded = context.input_slice_context.flush()
                if discarded is not None:
                    logger.info(f"MuseTalk: flushed {len(discarded)} samples from slicer on stream switch "
                                f"(prev={prev_key} -> new={stream_key_str})")
            streamer = context.get_playback_streamer()
            if streamer is not None and prev_key:
                streamer.finish_current()
                logger.info(
                    f"MuseTalk: CLIENT_PLAYBACK stream closed (implicit) for previous stream_key={prev_key}")
            if streamer is not None:
                sources = [inputs.stream_id] if inputs.stream_id else []
                streamer.open_stream(sources=sources, name=f"playback:{stream_key_str}")
                logger.info(f"MuseTalk: CLIENT_PLAYBACK stream opened for stream_key={stream_key_str}")

        speech_id = inputs.stream_id.stream_key_str if inputs.stream_id else None
        speech_end = inputs.is_last_data
        audio_entry = inputs.data.get_main_definition_entry()
        audio_array = inputs.data.get_main_data()
        if context.config.debug:
            logger.info(
                f"AvatarMuseTalk Handle Input: speech_id={speech_id}, speech_end={speech_end}, audio_array.shape={getattr(audio_array, 'shape', None)}")
        input_sample_rate = audio_entry.sample_rate
        if input_sample_rate != context.config.output_audio_sample_rate:
            logger.error(
                f"Input sample rate {input_sample_rate} != output sample rate {context.config.output_audio_sample_rate}")
            return
        if audio_array is not None and audio_array.dtype != np.float32:
            audio_array = audio_array.astype(np.float32)
        if audio_array is None:
            audio_array = np.zeros([input_sample_rate], dtype=np.float32)
            logger.error(f"Audio data is None, fill with 1s silence, speech_id: {speech_id}")

        for audio_segment in slice_data(context.input_slice_context, audio_array.squeeze()):
            speech_audio = MuseTalkSpeechAudio(
                speech_id=speech_id,
                end_of_speech=False,
                audio_data=audio_segment.tobytes(),
                sample_rate=input_sample_rate,
            )
            context.processor.add_audio(speech_audio)

        if speech_end:
            end_segment = context.input_slice_context.flush()
            if end_segment is None:
                logger.warning(f"Last segment is empty: speech_id={speech_id}, speech_end={speech_end}")
                fps = context.config.fps
                frame_len = input_sample_rate // fps
                zero_frames = np.zeros([2 * frame_len], dtype=np.float32)
                audio_data = zero_frames.tobytes()
            else:
                audio_data = end_segment.tobytes()
            speech_audio = MuseTalkSpeechAudio(
                speech_id=speech_id,
                end_of_speech=True,
                audio_data=audio_data,
                sample_rate=input_sample_rate,
            )
            context.processor.add_audio(speech_audio)

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        if not isinstance(context, AvatarMuseTalkContext):
            return
        if signal.type == ChatSignalType.STREAM_CANCEL and signal.related_stream.data_type == ChatDataType.CLIENT_PLAYBACK:
            # CLIENT_PLAYBACK 流被取消（上游 TTS/LLM 被打断）
            logger.info(f"MuseTalk: Received STREAM_CANCEL signal, interrupting avatar")
            context.interrupt()

    def destroy_context(self, context: HandlerContext):
        """Clean up and stop processor, release back to pool."""
        if isinstance(context, AvatarMuseTalkContext):
            if context._playback_streamer is not None:
                try:
                    context._playback_streamer.finish_current()
                except Exception:
                    pass
            processor = context.processor
            if processor:
                processor.stop()
                processor.set_callbacks(None)
                self.processor_pool.release(processor)
            context.clear()
            logger.info(f"Context destroyed for session {context.session_id}")

    def destroy(self):
        if self.processor_pool:
            self.processor_pool.destroy()
            logger.info("HandlerAvatarMuseTalk destroyed, processor pool cleaned up")
