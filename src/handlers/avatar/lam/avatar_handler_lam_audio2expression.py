import os
import queue
import sys
import time
from typing import Dict, Optional, Set, cast, List

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.common.handler_base import HandlerBase
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel, ChatEngineConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry, DataBundle
from chat_engine.data_models.internal.handler_definition_data import HandlerBaseInfo, HandlerDetail, HandlerDataInfo, \
    ChatDataConsumeMode
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.chat_stream import StreamKey
from engine_utils.directory_info import DirectoryInfo
from engine_utils.general_slicer import SliceContext, slice_data
from chat_engine.data_models.chat_stream_config import ChatStreamConfig


class AvatarLAMConfig(HandlerBaseConfigModel, BaseModel):
    model_name: str = "LAM_audio2exp"
    feature_extractor_model_name: str = "wav2vec2-base-960h"
    audio_sample_rate: int = Field(default=24000)


class AvatarLAMContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[AvatarLAMConfig] = None
        self.inference_context = None
        self.input_slice_context: Optional[SliceContext] = None
        self.active_stream_keys: Set[StreamKey] = set()


class HandlerAvatarLAM(HandlerBase):
    def __init__(self):
        super().__init__()
        self.infer = None
        self.arkit_channels: List[str] = []

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=AvatarLAMConfig
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        if not isinstance(handler_config, AvatarLAMConfig):
            handler_config = AvatarLAMConfig()
        algo_module_path = os.path.join(self.handler_root, "LAM_Audio2Expression")
        if algo_module_path not in sys.path:
            sys.path.append(algo_module_path)
        from .LAM_Audio2Expression.engines.defaults import (
            default_config_parser,
            default_setup,
        )
        from .LAM_Audio2Expression.engines.infer import INFER
        project_dir = DirectoryInfo.get_project_dir()
        model_path = os.path.join(project_dir, engine_config.model_root, handler_config.model_name)
        wav2vec_path = os.path.join(project_dir, engine_config.model_root, handler_config.feature_extractor_model_name)
        config_file = os.path.join(self.handler_root, "LAM_Audio2Expression",
                                   "configs", "lam_audio2exp_config_streaming.py")
        wav2vec_config_file = os.path.join(self.handler_root, "LAM_Audio2Expression",
                                           "configs", "wav2vec2_config.json")
        weight_path = os.path.join(model_path, "pretrained_models", "lam_audio2exp_streaming.tar")

        weight_path = weight_path.replace("\\", "/")
        wav2vec_path = wav2vec_path.replace("\\", "/")
        config_file = config_file.replace("\\", "/")
        wav2vec_config_file = wav2vec_config_file.replace("\\", "/")

        cfg = default_config_parser(config_file, {
            "weight": weight_path,
            "model": {
                "backbone": {
                    "pretrained_encoder_path": wav2vec_path,
                    "wav2vec2_config_path": wav2vec_config_file,
                }
            }
        })
        cfg = default_setup(cfg)
        self.infer = INFER.build(dict(type=cfg.infer.type, cfg=cfg))
        self.infer.model.eval()
        arkit_channel_list_path = os.path.join(self.handler_root, "assets", "arkit_face_channels.txt")
        self.arkit_channels.clear()
        for line in open(arkit_channel_list_path, "r"):
            self.arkit_channels.append(line.strip())

        t_start = time.monotonic()
        # warmup the model
        context: Optional[Dict] = None
        self.infer.infer_streaming_audio(
            context=context,
            audio=np.zeros([handler_config.audio_sample_rate], dtype=np.float32),
            ssr=handler_config.audio_sample_rate,
        )
        dur_warmup = time.monotonic() - t_start
        logger.info(f"LAM_Audio2Expression warmup finished in {dur_warmup * 1000} milliseconds.")

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        if not isinstance(handler_config, AvatarLAMConfig):
            handler_config = AvatarLAMConfig()
        context = AvatarLAMContext(session_context.session_info.session_id)

        context.config = handler_config
        context.input_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=round(handler_config.audio_sample_rate * 1.0),
            slice_axis=0,
        )
        return context

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        context = cast(AvatarLAMContext, context)
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_framed_entry(
            name="arkit_face",
            shape=[1, 52],
            time_axis=0,
            sample_rate=30,
            channel_axis=1,
            channel_names=self.arkit_channels
        ))
        definition.add_entry(DataBundleEntry.create_audio_entry(
            name="avatar_audio",
            channel_num=1,
            sample_rate=context.config.audio_sample_rate,
        ))
        inputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                input_consume_mode=ChatDataConsumeMode.ONCE,
            )
        }
        outputs = {
            ChatDataType.AVATAR_MOTION_DATA: HandlerDataInfo(
                type=ChatDataType.AVATAR_MOTION_DATA,
                definition=definition
            )
        }
        return HandlerDetail(
            inputs=inputs,
            outputs=outputs
        )

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_MOTION_DATA).definition
        context = cast(AvatarLAMContext, context)
        streamer = context.data_submitter.get_streamer(ChatDataType.AVATAR_MOTION_DATA)
        stream = streamer.current_stream
        stream_key = stream.identity.stream_key_str if stream is not None else None
        if stream_key is None:
            stream = streamer.new_stream(sources=[inputs.stream_id],
                                         name="lam_audio2expression", config=ChatStreamConfig(cancelable=True))
            stream_key = stream.stream_key_str
        is_last = inputs.is_last_data
        speech_text = inputs.data.get_meta("avatar_speech_text")

        if stream_key:
            context.active_stream_keys.add(stream_key)

        audio = inputs.data.get_main_data()
        audio_segments = queue.Queue()
        for audio_segment in slice_data(context.input_slice_context, audio.squeeze()):
            audio_segments.put_nowait(audio_segment)
        if is_last:
            end_segment = context.input_slice_context.flush()
            if end_segment is not None:
                audio_segments.put_nowait(end_segment)
        if audio_segments.empty() and is_last:
            audio_segments.put_nowait(np.zeros([50], dtype=np.float32))
        while not audio_segments.empty():
            if stream_key and stream_key not in context.active_stream_keys:
                logger.info(f"LAM: Stream {stream_key} no longer active, stopping inference")
                context.inference_context = None
                break
            t_start = time.monotonic()
            audio_segment = audio_segments.get_nowait()
            result, context_update = self.infer.infer_streaming_audio(
                audio=audio_segment,
                ssr=context.config.audio_sample_rate,
                context=context.inference_context,
            )
            context.inference_context = context_update
            need_flush = is_last and audio_segments.empty()
            if need_flush:
                context.inference_context = None
            output = DataBundle(output_definition)
            arkit_data = result.get("expression")
            if arkit_data is None:
                continue

            output.set_main_data(arkit_data.astype(np.float32))
            output.set_data("avatar_audio", audio_segment[np.newaxis, ...])
            output.add_meta("stream_key", inputs.stream_id.stream_key_str if inputs.stream_id else None)
            if speech_text is not None:
                output.add_meta("avatar_speech_text", speech_text)
            dur_inference = time.monotonic() - t_start
            logger.info(f"Inference on {audio_segment.shape[-1] / context.config.audio_sample_rate:.2f} second audio "
                        f"finished in {dur_inference * 1000} milliseconds. Got output: {str(output)}")
            streamer.stream_data(output, finish_stream=is_last)
        if stream_key and is_last:
            context.active_stream_keys.discard(stream_key)

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        context = cast(AvatarLAMContext, context)
        if signal.type == ChatSignalType.STREAM_CANCEL and signal.related_stream:
            stream_key = signal.related_stream.stream_key_str
            if stream_key is not None and stream_key in context.active_stream_keys:
                context.active_stream_keys.discard(stream_key)
                logger.info(f"LAM: Removed stream {stream_key} from active set")

    def destroy_context(self, context: HandlerContext):
        pass
