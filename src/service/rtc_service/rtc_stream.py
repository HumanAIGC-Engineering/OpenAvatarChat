import asyncio
import json
import time
import uuid
import weakref
from typing import Optional, Dict

import numpy as np
# noinspection PyPackageRequirements
from fastrtc import (
    AsyncAudioVideoStreamHandler,
    AudioEmitType,
    VideoEmitType,
    get_current_context,
)
from loguru import logger

from chat_engine.common.client_handler_base import ClientHandlerDelegate, ClientSessionDelegate
from chat_engine.data_models.engine_channel_type import EngineChannelType
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
from engine_utils.interval_counter import IntervalCounter
from handlers.client.ws_client.ws_message_protocol import (
    EchoHumanText,
    EchoTextPayload,
    MessageHeader,
    MessageType,
    serialize_message,
)

def _get_h264_encoder_info():
    """Get H.264 encoder info dynamically to avoid circular imports"""
    try:
        from handlers.client.rtc_client import client_handler_rtc
        return client_handler_rtc._selected_h264_encoder, client_handler_rtc._actual_h264_encoder
    except Exception:
        return "unknown", None


class RtcStream(AsyncAudioVideoStreamHandler):
    def __init__(self,
                 session_id: Optional[str],
                 expected_layout="mono",
                 input_sample_rate=16000,
                 output_sample_rate=24000,
                 output_frame_size=480,
                 fps=30,
                 stream_start_delay = 0.5,
                 ):
        super().__init__(
            expected_layout=expected_layout,
            input_sample_rate=input_sample_rate,
            output_sample_rate=output_sample_rate,
            output_frame_size=output_frame_size,
            fps=fps
        )
        self.client_handler_delegate: Optional[ClientHandlerDelegate] = None
        self.client_session_delegate: Optional[ClientSessionDelegate] = None

        self.weak_factory: Optional[weakref.ReferenceType[RtcStream]] = None

        self.session_id = session_id
        self.stream_start_delay = stream_start_delay

        self.chat_channel = None
        self.chat_channel_loop = None
        self.first_audio_emitted = False

        self.quit = asyncio.Event()
        self.last_frame_time = 0

        self.emit_counter = IntervalCounter("emit counter")

        self.start_time = None
        self.timestamp_base = self.input_sample_rate

        self.streams: Dict[str, RtcStream] = {}
        self.owns_session = False


    # copy is used as create_instance in fastrtc
    def copy(self, **kwargs) -> AsyncAudioVideoStreamHandler:
        try:
            if self.client_handler_delegate is None:
                raise Exception("ClientHandlerDelegate is not set.")

            new_stream = RtcStream(
                '',
                expected_layout=self.expected_layout,
                input_sample_rate=self.input_sample_rate,
                output_sample_rate=self.output_sample_rate,
                output_frame_size=self.output_frame_size,
                fps=self.fps,
                stream_start_delay=self.stream_start_delay,
            )
            new_stream.weak_factory = weakref.ref(self)
            return new_stream
        except Exception as e:
            logger.opt(exception=True).error(f"Failed to create stream: {e}")
            raise

    async def start_up(self):
        if self.client_session_delegate is not None:
            return

        factory = self
        if self.weak_factory is not None and self.weak_factory() is not None:
            factory = self.weak_factory()

        if factory.client_handler_delegate is None:
            raise RuntimeError("ClientHandlerDelegate is not set.")

        session_id = self.session_id
        if not session_id:
            try:
                session_id = get_current_context().webrtc_id
            except Exception:
                session_id = uuid.uuid4().hex

        selected_encoder, _ = _get_h264_encoder_info()
        logger.debug(f"[{session_id}] H.264 encoder: {selected_encoder}")

        if session_id in factory.streams:
            existing = factory.streams.get(session_id)
            # Cleanup stale entries left by interrupted connections.
            if existing is None or existing.client_session_delegate is None or existing.quit.is_set():
                factory.streams.pop(session_id, None)
            else:
                base_session_id = session_id
                session_id = f"{base_session_id}-{uuid.uuid4().hex[:8]}"
                logger.warning(f"Session id conflict for {base_session_id}, fallback to {session_id}")

        self.session_id = session_id
        existing_delegate = factory.client_handler_delegate.find_session_delegate(session_id)
        if existing_delegate is not None:
            self.client_session_delegate = existing_delegate
            self.owns_session = False
            logger.info(f"Reuse existing session delegate for session {session_id}")
        else:
            try:
                self.client_session_delegate = factory.client_handler_delegate.start_session(
                    session_id=session_id,
                    timestamp_base=self.input_sample_rate,
                )
                self.owns_session = True
            except RuntimeError as e:
                # Another client path (e.g. WS) may create the same session concurrently.
                if "already exists" not in str(e):
                    raise
                existing_delegate = factory.client_handler_delegate.find_session_delegate(session_id)
                if existing_delegate is None:
                    raise
                self.client_session_delegate = existing_delegate
                self.owns_session = False
                logger.info(f"Session {session_id} created concurrently, reusing existing delegate")

        factory.streams[session_id] = self

    async def emit(self) -> AudioEmitType:
        try:
            # if not self.args_set.is_set():
            # await self.wait_for_args()
            while self.client_session_delegate is None and not self.quit.is_set():
                await asyncio.sleep(0.01)
            if self.client_session_delegate is None:
                return None

            if not self.first_audio_emitted:
                self.client_session_delegate.clear_data()
                self.first_audio_emitted = True

            while not self.quit.is_set():
                chat_data = await self.client_session_delegate.get_data(EngineChannelType.AUDIO)
                if chat_data is None or chat_data.data is None:
                    continue
                audio_array = chat_data.data.get_main_data()
                if audio_array is None:
                    continue
                sample_num = audio_array.shape[-1]
                self.emit_counter.add_property("audio_emit", sample_num / self.output_sample_rate)
                return self.output_sample_rate, audio_array
        except Exception as e:
            logger.opt(exception=e).error("Error in emit: ")
            raise

    async def video_emit(self) -> VideoEmitType:
        try:
            if not self.first_audio_emitted:
                await asyncio.sleep(0.1)
            while self.client_session_delegate is None and not self.quit.is_set():
                await asyncio.sleep(0.01)
            if self.client_session_delegate is None:
                return None
            
            self.emit_counter.add_property("video_emit")
            
            while not self.quit.is_set():
                get_data_start = time.perf_counter()
                video_frame_data: ChatData = await self.client_session_delegate.get_data(EngineChannelType.VIDEO)
                get_data_wait_time = time.perf_counter() - get_data_start

                _slow_video_threshold_s = 0.12
                if get_data_wait_time > _slow_video_threshold_s:
                    logger.debug(
                        f"[{self.session_id}] Slow video data retrieval: "
                        f"{get_data_wait_time:.3f}s (threshold {_slow_video_threshold_s}s)"
                    )
                
                if video_frame_data is None or video_frame_data.data is None:
                    continue
                
                frame_data = video_frame_data.data.get_main_data().squeeze()
                if frame_data is None:
                    continue

                return frame_data
        except Exception as e:
            logger.opt(exception=e).error("Error in video_emit")
            raise

    async def receive(self, frame: tuple[int, np.ndarray]):
        if self.client_session_delegate is None:
            return
        timestamp = self.client_session_delegate.get_timestamp()
        if timestamp[0] / timestamp[1] < self.stream_start_delay:
            return
        _, array = frame
        self.client_session_delegate.put_data(
            EngineChannelType.AUDIO,
            array,
            timestamp,
            self.input_sample_rate,
        )

    async def video_receive(self, frame):
        if self.client_session_delegate is None:
            return
        timestamp = self.client_session_delegate.get_timestamp()
        if timestamp[0] / timestamp[1] < self.stream_start_delay:
            return
        self.client_session_delegate.put_data(
            EngineChannelType.VIDEO,
            frame,
            timestamp,
            self.fps,
        )

    def set_channel(self, channel):
            super().set_channel(channel)
            self.chat_channel = channel
            try:
                self.chat_channel_loop = asyncio.get_running_loop()
            except RuntimeError:
                self.chat_channel_loop = None
                
            @channel.on("message")
            def _(message):
                logger.info(f"Received message Custom: {message}")
                try:
                    message = json.loads(message)
                except Exception as e:
                    logger.info(e)
                    message = {}

                if self.client_session_delegate is None:
                    return
                timestamp = self.client_session_delegate.get_timestamp()
                if timestamp[0] / timestamp[1] < self.stream_start_delay:
                    return
                logger.info(f'on_chat_datachannel: {message}')
    
                if message['header']['name'] == 'Interrupt':
                    self.client_session_delegate.emit_signal(
                        ChatSignal(
                            type=ChatSignalType.INTERRUPT,
                            source_type=ChatSignalSourceType.CLIENT,
                            source_name="rtc",
                        )
                    )
                elif message['header']['name'] == 'SendHumanText':
                    # self.client_session_delegate.emit_signal(
                    #     ChatSignal(
                    #         type=ChatSignalType.INTERRUPT,
                    #         source_type=ChatSignalSourceType.CLIENT,
                    #         source_name="rtc",
                    #     )
                    # )
                    self.client_session_delegate.emit_signal(
                        ChatSignal(
                            # begin a new round of responding
                            type=ChatSignalType.STREAM_BEGIN,
                            stream_type=ChatDataType.AVATAR_AUDIO,
                            source_type=ChatSignalSourceType.CLIENT,
                            source_name="rtc",
                        )
                    )
                    self.client_session_delegate.put_data(
                        EngineChannelType.TEXT,
                        message['payload']['text'],
                        loopback=True
                    )
                    # Keep immediate user-text echo for pure RTC mode.
                    # WsLam delegate has its own text echo path, so skip here to avoid duplicates.
                    if not hasattr(self.client_session_delegate, "ws_text_queue"):
                        try:
                            payload = message.get("payload", {})
                            response = EchoHumanText(
                                header=MessageHeader(
                                    name=MessageType.ECHO_HUMAN_TEXT,
                                    request_id=str(uuid.uuid4()),
                                ),
                                payload=EchoTextPayload(
                                    stream_key=payload.get("stream_key"),
                                    mode="full_text",
                                    text=payload.get("text", ""),
                                    end_of_speech=payload.get("end_of_speech", True),
                                    metadata=None,
                                ),
                            )
                            self.chat_channel.send(json.dumps(serialize_message(response)))
                        except Exception as e:
                            logger.opt(exception=e).warning("Failed to send local human text echo")
                # else:

                # channel.send(json.dumps({"type": "chat", "unique_id": unique_id, "message": message}))
          
    async def on_chat_datachannel(self, message: Dict, channel):
        # {"type":"chat",id:"标识属于同一段话", "message":"Hello, world!"}
        # unique_id = uuid.uuid4().hex
        pass
    def shutdown(self):
        self.quit.set()
        factory = None
        if self.weak_factory is not None:
            factory = self.weak_factory()
        if factory is None:
            factory = self
        self.client_session_delegate = None
        if self.session_id in factory.streams:
            factory.streams.pop(self.session_id, None)
        if self.owns_session and factory.client_handler_delegate is not None:
            factory.client_handler_delegate.stop_session(self.session_id)
