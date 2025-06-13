import os
import time
import pickle
from typing import Dict, Optional, cast
import numpy as np
from loguru import logger
import threading
import queue
import hashlib

from chat_engine.data_models.chat_data_type import ChatDataType, EngineChannelType
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail, \
    ChatDataConsumeMode
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition, DataBundleEntry, DataBundle, VariableSize
from handlers.avatar.liteavatar.model.audio_input import SpeechAudio
from handlers.avatar.liteavatar.avatar_handler_liteavatar import Tts2FaceEvent
from handlers.avatar.musetalk.avatar_musetalk_processor import AvatarMuseTalkProcessor
from handlers.avatar.musetalk.avatar_musetalk_algo import MuseAvatarV15
from handlers.avatar.musetalk.avatar_musetalk_config import AvatarMuseTalkConfig
from engine_utils.general_slicer import slice_data, SliceContext


# Context class for MuseTalk avatar handler
class AvatarMuseTalkContext(HandlerContext):
    """
    Context class for MuseTalk avatar handler
    """
    def __init__(self, session_id: str, event_in_queue: queue.Queue, event_out_queue: queue.Queue, audio_out_queue: queue.Queue, video_out_queue: queue.Queue, shared_status):
        """
        Initialize the context for the MuseTalk avatar handler.
        This context manages the communication queues, configuration, and output threads for audio/video/events.
        Args:
            session_id (str): Unique session identifier.
            event_in_queue (queue.Queue): Queue for incoming events.
            event_out_queue (queue.Queue): Queue for outgoing events.
            audio_out_queue (queue.Queue): Queue for outgoing audio data.
            video_out_queue (queue.Queue): Queue for outgoing video data.
            shared_status: Shared state object for VAD and other flags.
        """
        super().__init__(session_id)
        self.config: Optional[AvatarMuseTalkConfig] = None  # Handler configuration
        self.event_in_queue: queue.Queue = event_in_queue  # Event input queue
        self.audio_out_queue: queue.Queue = audio_out_queue  # Audio output queue
        self.video_out_queue: queue.Queue = video_out_queue  # Video output queue
        self.event_out_queue: queue.Queue = event_out_queue  # Event output queue
        self.shared_state = shared_status  # Shared state for VAD, etc.
        self.input_slice_context = None  # Audio slicing context for segmenting input audio
        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}  # Output data definitions
        self.media_out_thread: threading.Thread = None  # Thread for outputting media
        self.event_out_thread: threading.Thread = None  # Thread for outputting events
        self.loop_running = True  # Control flag for threads
        # Start threads for outputting media and events
        try:
            self.media_out_thread = threading.Thread(target=self._media_out_loop)
            self.media_out_thread.start()
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to start media_out_thread: {e}")
        try:
            self.event_out_thread = threading.Thread(target=self._event_out_loop)
            self.event_out_thread.start()
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to start event_out_thread: {e}")

    def return_data(self, data: np.ndarray, chat_data_type: ChatDataType) -> None:
        """
        Package and submit output data for downstream consumption.
        Handles both audio and video data, ensuring correct format and type.
        Args:
            data: The output data (audio or video).
            chat_data_type (ChatDataType): The type of data (AUDIO/VIDEO).
        """
        definition = self.output_data_definitions.get(chat_data_type)
        if definition is None:
            logger.error(f"Definition is None, chat_data_type={chat_data_type}")
            return
        data_bundle = DataBundle(definition)
        if chat_data_type.channel_type == EngineChannelType.AUDIO:
            # Ensure audio data is float32 and has correct shape
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
            # Ensure video data has batch dimension
            data_bundle.set_main_data(data[np.newaxis, ...])
        else:
            return
        chat_data = ChatData(type=chat_data_type, data=data_bundle)
        self.submit_data(chat_data)

    def _media_out_loop(self) -> None:
        """
        Continuously output audio and video data from queues.
        This thread checks the audio and video output queues and returns data to the engine.
        """
        while self.loop_running:
            no_output = True
            if self.audio_out_queue.qsize() > 0:
                try:
                    audio = self.audio_out_queue.get_nowait()
                    self.return_data(audio, ChatDataType.AVATAR_AUDIO)
                    no_output = False
                except Exception as e:
                    logger.opt(exception=True).error(f"Exception when getting audio data: {e}")
            if self.video_out_queue.qsize() > 0:
                try:
                    video = self.video_out_queue.get_nowait()
                    if not isinstance(video, np.ndarray):
                        logger.error(f"video_out_queue got non-ndarray: {type(video)}, content: {str(video)[:100]}")
                        continue
                    self.return_data(video, ChatDataType.AVATAR_VIDEO)
                    no_output = False
                except Exception as e:
                    logger.opt(exception=True).error(f"Exception when getting video data: {e}")
            if no_output:
                time.sleep(0.01)
        logger.info("Media out loop exit")

    def _event_out_loop(self) -> None:
        """
        Continuously output event data from queue.
        This thread checks the event output queue and updates shared state if needed.
        """
        logger.info("Event out loop started")
        while self.loop_running:
            try:
                event = self.event_out_queue.get(timeout=0.1)
                if isinstance(event, Tts2FaceEvent):
                    if event == Tts2FaceEvent.SPEAKING_TO_LISTENING:
                        self.shared_state.enable_vad = True
                        if self.config.debug:
                            logger.info("shared_state.enable_vad = True")
                else:
                    logger.warning(f"event_out_queue got unknown event type: {type(event)}, value: {event}")
            except queue.Empty:
                continue
            except Exception as e:
                logger.opt(exception=True).error(f"Exception: {e}")
        logger.info("Event out loop exit")
    
    def clear(self) -> None:
        """
        Clean up context and stop threads.
        Signals threads to exit and joins them.
        """
        logger.info("Clear musetalk context")
        self.loop_running = False
        self.event_in_queue.put_nowait(Tts2FaceEvent.STOP)
        try:
            self.media_out_thread.join(timeout=5)
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to join media_out_thread: {e}")
        try:
            self.event_out_thread.join(timeout=5)
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to join event_out_thread: {e}")

class HandlerAvatarMusetalk(HandlerBase):
    def __init__(self) -> None:
        """
        Initialize MuseTalk avatar handler.
        """
        super().__init__()
        self.processor: Optional[AvatarMuseTalkProcessor] = None
        self.avatar: Optional[MuseAvatarV15] = None
        self.audio_input_thread = None
        self.event_in_queue = queue.Queue()
        self.event_out_queue = queue.Queue()
        self.audio_out_queue = queue.Queue()
        self.video_out_queue = queue.Queue()
        self.output_data_definitions: Dict[ChatDataType, DataBundleDefinition] = {}
        self.shared_state = None
        self._debug_cache = {}

    def _save_debug_cache(self, speech_id: str, debug_root: str) -> None:
        """
        Save and clear debug cache for a given speech_id.
        """
        debug_file = os.path.join(debug_root, f"{speech_id}.pkl")
        try:
            with open(debug_file, "wb") as f:
                pickle.dump(self._debug_cache[speech_id], f)
            del self._debug_cache[speech_id]
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to save debug record: {e}")

    def get_handler_info(self) -> HandlerBaseInfo:
        """
        Return handler registration info.
        """
        return HandlerBaseInfo(
            config_model=AvatarMuseTalkConfig,
            load_priority=-999,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[AvatarMuseTalkConfig] = None):
        """
        Load and initialize model and processor, setup output data structure.
        """
        if not isinstance(handler_config, AvatarMuseTalkConfig):
            handler_config = AvatarMuseTalkConfig()
        audio_output_definition = DataBundleDefinition()
        audio_output_definition.add_entry(DataBundleEntry.create_audio_entry(
            "avatar_muse_audio",
            1,
            handler_config.output_audio_sample_rate,
        ))
        audio_output_definition.lockdown()
        self.output_data_definitions[ChatDataType.AVATAR_AUDIO] = audio_output_definition
        video_output_definition = DataBundleDefinition()
        video_output_definition.add_entry(DataBundleEntry.create_framed_entry(
            "avatar_muse_video",
            [VariableSize(), VariableSize(), VariableSize(), 3],
            0,
            handler_config.fps
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
        # auto generate avatar_id
        video_path = handler_config.avatar_video_path
        video_basename = os.path.splitext(os.path.basename(video_path))[0]
        video_hash = hashlib.md5(video_path.encode()).hexdigest()[:8]
        auto_avatar_id = f"avatar_{video_basename}_{video_hash}"
        logger.info(f"Auto generated avatar_id: {auto_avatar_id}")
        
        self.avatar = MuseAvatarV15(
            avatar_id=auto_avatar_id,
            video_path=handler_config.avatar_video_path,
            bbox_shift=0,
            batch_size=handler_config.batch_size,
            force_preparation=handler_config.force_create_avatar,
            parsing_mode="jaw",
            left_cheek_width=90,
            right_cheek_width=90,
            audio_padding_length_left=2,
            audio_padding_length_right=2,
            fps=handler_config.fps,
            version="v15",
            result_dir=result_dir,
            extra_margin=10,
            vae_type=vae_type,
            unet_model_path=unet_model_path,
            unet_config=unet_config,
            whisper_dir=whisper_dir,
            gpu_id=0,
            debug=handler_config.debug
        )
        self.processor = AvatarMuseTalkProcessor(
            self.avatar,
            handler_config
        )
        logger.info("HandlerAvatarMusetalk loaded and processor initialized.")

    def create_context(self, session_context: SessionContext,
                      handler_config: Optional[AvatarMuseTalkConfig] = None) -> HandlerContext:
        """
        Create and start session context.
        """
        logger.info(f"HandlerAvatarMusetalk.create_context called, session_context={session_context}, handler_config={handler_config}")
        if not isinstance(handler_config, AvatarMuseTalkConfig):
            handler_config = AvatarMuseTalkConfig()
        self.shared_state = session_context.shared_states
        self.processor.audio_output_queue = self.audio_out_queue
        self.processor.video_output_queue = self.video_out_queue
        self.processor.event_out_queue = self.event_out_queue
        context = AvatarMuseTalkContext(
            session_context.session_info.session_id,
            self.event_in_queue,
            self.event_out_queue,
            self.audio_out_queue,
            self.video_out_queue,
            self.shared_state
        )
        context.output_data_definitions = self.output_data_definitions
        context.config = handler_config
        
        output_audio_sample_rate = handler_config.output_audio_sample_rate
        fps = handler_config.fps
        frame_audio_len_float = output_audio_sample_rate / fps
        if not frame_audio_len_float.is_integer():
            logger.error(f"output_audio_sample_rate / fps = {output_audio_sample_rate} / {fps} = {frame_audio_len_float}, is not an integer, there may be cumulative error in audio-video alignment!")

        context.input_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=output_audio_sample_rate,
            slice_axis=0,
        )
        logger.info("Context created and processor started.")
        return context

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        """
        Start context.
        """
        self.processor.start()
        logger.info("Context started and processor started.")
        if hasattr(handler_context, 'config') and getattr(handler_context.config, 'debug_replay_speech_id', None):
            speech_id = handler_context.config.debug_replay_speech_id
            def _delayed_replay():
                time.sleep(2)
                self.replay_handle(speech_id, handler_context)
            threading.Thread(target=_delayed_replay, daemon=True).start()

    def get_handler_detail(self, session_context: SessionContext,
                         context: HandlerContext) -> HandlerDetail:
        """
        Return handler input/output data type details.
        """
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
            ),
        }
        return HandlerDetail(inputs=inputs, outputs=outputs)

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """
        Main handler logic for processing audio input and sending to processor.
        Receives audio data, slices it, wraps it as SpeechAudio, and sends to processor.
        """
        # Efficient debug data storage, write once at speech_end, record simplified inputs and output_definitions
        if hasattr(context, 'config') and getattr(context.config, 'debug_save_handler_audio', False):
            debug_root = "logs/audio_segments/"
            speech_id = inputs.data.get_meta("speech_id") or "unknown"
            os.makedirs(debug_root, exist_ok=True)
            now = time.time()
            input_type = inputs.type.name if hasattr(inputs.type, "name") else str(inputs.type)
            main_data = inputs.data.get_main_data()
            if isinstance(main_data, np.ndarray):
                main_data = main_data.tolist()
            meta = dict(inputs.data.metadata) if hasattr(inputs.data, "metadata") else {}
            sample_rate = None
            try:
                sample_rate = inputs.data.get_main_definition_entry().sample_rate
            except Exception:
                pass
            output_def = None
            if inputs.type in output_definitions:
                output_def = output_definitions[inputs.type].definition
            record = {
                "timestamp": now,
                "inputs": {
                    "type": input_type,
                    "main_data": main_data,
                    "meta": meta,
                    "sample_rate": sample_rate,
                },
                "output_definition": output_def,
                "speech_id": speech_id,
                "speech_end": inputs.data.get_meta("avatar_speech_end", False),
            }
            if speech_id not in self._debug_cache:
                self._debug_cache[speech_id] = []
            self._debug_cache[speech_id].append(record)
            if record["speech_end"]:
                self._save_debug_cache(speech_id, debug_root)

        if inputs.type != ChatDataType.AVATAR_AUDIO:
            return
        context = cast(AvatarMuseTalkContext, context)
        speech_id = inputs.data.get_meta("speech_id")
        speech_end = inputs.data.get_meta("avatar_speech_end", False)
        audio_entry = inputs.data.get_main_definition_entry()
        audio_array = inputs.data.get_main_data()
        if context.config.debug:
            logger.info(f"AvatarMuseTalk Handle Input: speech_id={speech_id}, speech_end={speech_end}, audio_array.shape={getattr(audio_array, 'shape', None)}")
        input_sample_rate = audio_entry.sample_rate
        if input_sample_rate != context.config.output_audio_sample_rate:
            logger.error(f"Input sample rate {input_sample_rate} != output sample rate {context.config.output_audio_sample_rate}")
            return
        if audio_array is not None and audio_array.dtype != np.float32:
            audio_array = audio_array.astype(np.float32)
        if audio_array is None:
            audio_array = np.zeros([input_sample_rate], dtype=np.float32)
            logger.error(f"Audio data is None, fill with 1s silence, speech_id: {speech_id}")
        # Slice audio into segments for processing
        for audio_segment in slice_data(context.input_slice_context, audio_array.squeeze()):
            speech_audio = SpeechAudio(
                speech_id=speech_id,
                end_of_speech=False,
                audio_data=audio_segment.tobytes(),
                sample_rate=input_sample_rate
            )
            if self.processor:
                self.processor.add_audio(speech_audio)
        if speech_end:
            # On speech end, flush remaining audio, fill with zeros if empty
            end_segment = context.input_slice_context.flush()
            if end_segment is None:
                logger.warning(f"Last segment is empty: speech_id={speech_id}, speech_end={speech_end}")
                fps = context.config.fps if hasattr(context.config, "fps") else 25
                frame_len = input_sample_rate // fps
                # 2 frames audio for silence
                zero_frames = np.zeros([2 * frame_len], dtype=np.float32)
                audio_data = zero_frames.tobytes()
            else:
                audio_data = end_segment.tobytes()
            speech_audio = SpeechAudio(
                speech_id=speech_id,
                end_of_speech=True,
                audio_data=audio_data,
                sample_rate=input_sample_rate
            )
            if self.processor:
                self.processor.add_audio(speech_audio)

    def _pack_debug_record(self, inputs: ChatData, output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """
        Helper: Pack inputs and output_definitions into a simplified serializable structure.
        """
        input_type = inputs.type.name if hasattr(inputs.type, "name") else str(inputs.type)
        main_data = inputs.data.get_main_data()
        if isinstance(main_data, np.ndarray):
            main_data = main_data.tolist()
        meta = dict(inputs.data.metadata) if hasattr(inputs.data, "metadata") else {}
        sample_rate = None
        try:
            sample_rate = inputs.data.get_main_definition_entry().sample_rate
        except Exception:
            pass
        output_def = None
        if inputs.type in output_definitions:
            output_def = output_definitions[inputs.type].definition
        return {
            "type": input_type,
            "main_data": main_data,
            "meta": meta,
            "sample_rate": sample_rate,
            "output_definition": output_def,
        }

    def _unpack_debug_record_to_chatdata(self, input_record, output_definition, ChatDataType):
        """
        Helper: Restore ChatData object from simplified structure.
        """
        chat_data_type = getattr(ChatDataType, input_record["type"], None)
        definition = output_definition
        if definition is None:
            raise RuntimeError("No output_definition in debug record!")
        from chat_engine.data_models.runtime_data.data_bundle import DataBundle
        data_bundle = DataBundle(definition)
        main_data = np.array(input_record["main_data"], dtype=np.float32)
        data_bundle.set_main_data(main_data)
        for k, v in input_record["meta"].items():
            data_bundle.add_meta(k, v)
        return ChatData(type=chat_data_type, data=data_bundle)

    def replay_handle(self, speech_id, context):
        """
        Replay handle records for the specified speech_id.
        """
        import pickle, os, time
        from chat_engine.data_models.chat_data_type import ChatDataType
        debug_file = os.path.join("logs/audio_segments", f"{speech_id}.pkl")
        if not os.path.exists(debug_file):
            logger.error(f"Debug file for speech_id {speech_id} not found.")
            return
        try:
            with open(debug_file, "rb") as f:
                records = pickle.load(f)
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to load debug file: {e}")
            return
        if not records:
            logger.error("No records to replay.")
            return
        records.sort(key=lambda x: x["timestamp"])
        for i, record in enumerate(records):
            chat_data = self._unpack_debug_record_to_chatdata(record["inputs"], record["output_definition"], ChatDataType)
            if i > 0:
                interval = record["timestamp"] - records[i-1]["timestamp"]
                logger.info(f"Replay {i+1}/{len(records)}: speech_end={record['speech_end']}, interval: {interval:.3f} s")
                if interval > 0:
                    time.sleep(interval)
            else:
                logger.info(f"Replay {i+1}/{len(records)}: speech_end={record['speech_end']}, first record")
            output_definitions = {chat_data.type: HandlerDataInfo(type=chat_data.type, definition=record["output_definition"])}
            self.handle(context, chat_data, output_definitions)

    def destroy_context(self, context: HandlerContext):
        """
        Clean up and stop processor and related threads.
        """
        if isinstance(context, AvatarMuseTalkContext):
            if self.processor:
                self.processor.stop()
            if self.audio_input_thread:
                self.audio_input_thread.join()
                self.audio_input_thread = None
            context.clear()


