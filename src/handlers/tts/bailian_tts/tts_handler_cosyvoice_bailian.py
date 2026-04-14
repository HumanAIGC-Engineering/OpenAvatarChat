import io
import os
import re
import time
from dataclasses import dataclass, field
from typing import Dict, Optional, Set, cast
import librosa
import numpy as np
from loguru import logger
from pydantic import BaseModel, Field
from abc import ABC
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from engine_utils.directory_info import DirectoryInfo
from dashscope.audio.tts_v2 import SpeechSynthesizer, ResultCallback, AudioFormat
import dashscope

from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_stream import StreamKey, ChatStreamIdentity
from chat_engine.data_models.chat_stream_config import ChatStreamConfig


class TTSConfig(HandlerBaseConfigModel, BaseModel):
    ref_audio_path: str = Field(default=None)
    ref_audio_text: str = Field(default=None)
    voice: str = Field(default=None)
    sample_rate: int = Field(default=24000)
    api_key: str = Field(default=os.getenv("DASHSCOPE_API_KEY"))
    model_name: str = Field(default="cosyvoice-1")


@dataclass
class BailianTTSSession:
    """Per-stream session state, isolates synthesizer for each input stream."""
    input_stream_id: ChatStreamIdentity
    output_stream_key: Optional[StreamKey] = None
    synthesizer: Optional[SpeechSynthesizer] = None
    cancelled: bool = False

    def reset(self):
        self.cancelled = True
        if self.synthesizer is not None:
            try:
                self.synthesizer.streaming_cancel()
            except Exception:
                pass
            self.synthesizer = None


class TTSContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.api_links: Dict[StreamKey, BailianTTSSession] = {}
        self.dump_audio = False
        self.audio_dump_file = None

    @classmethod
    def _create_session(cls, input_stream: ChatStreamIdentity) -> BailianTTSSession:
        return BailianTTSSession(input_stream_id=input_stream)

    def handle_text_stream(self, data: ChatData, handler: 'HandlerTTS'):
        input_stream = data.stream_id
        input_stream_key = input_stream.key

        session = self.api_links.get(input_stream_key)
        if session is None:
            # 新的输入流到达，取消所有旧 session（同一时间只有一个合成器活跃）
            for old_key, old_session in list(self.api_links.items()):
                logger.info(f"TTS: Cancelling previous session for stream {old_key}")
                old_session.reset()
            self.api_links.clear()

            session = self._create_session(input_stream)
            self.api_links[input_stream_key] = session

            # 为新的输入流创建输出流，建立 1:1 的显式关联
            streamer = self.data_submitter.get_streamer(ChatDataType.AVATAR_AUDIO)
            output_stream_id = streamer.new_stream(
                sources=[session.input_stream_id],
                name="bailian_tts",
                config=ChatStreamConfig(cancelable=True)
            )
            session.output_stream_key = output_stream_id.key

        text = data.data.get_main_data()
        if text is not None:
            text = re.sub(r"<\|.*?\|>", "", text)

        text_end = data.is_last_data

        try:
            if not text_end:
                if session.synthesizer is None:
                    streamer = self.data_submitter.get_streamer(ChatDataType.AVATAR_AUDIO)
                    callback = CosyvoiceCallBack(
                        context=self,
                        output_definition=streamer.data_definition,
                        session=session)
                    session.synthesizer = SpeechSynthesizer(
                        model=handler.model_name, voice=handler.voice,
                        callback=callback, format=AudioFormat.PCM_24000HZ_MONO_16BIT)
                logger.info(f'streaming_call {text}')
                session.synthesizer.streaming_call(text)
            else:
                logger.info(f'streaming_call last {text}')
                if session.synthesizer is not None:
                    session.synthesizer.streaming_call(text)
                    session.synthesizer.streaming_complete()
                session.synthesizer = None
                self.api_links.pop(input_stream_key, None)
        except Exception as e:
            logger.error(e)
            session.reset()
            self.api_links.pop(input_stream_key, None)


class HandlerTTS(HandlerBase, ABC):
    def __init__(self):
        super().__init__()

        self.ref_audio_path = None
        self.ref_audio_text = None
        self.voice = None
        self.ref_audio_buffer = None
        self.sample_rate = None
        self.model_name = None
        self.api_key = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=TTSConfig,
        )

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("avatar_audio", 1, self.sample_rate))
        inputs = [
            HandlerDataInfo(type=ChatDataType.AVATAR_TEXT),
        ]
        outputs = [
            HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=definition,
            )
        ]
        return HandlerDetail(
            inputs=inputs,
            outputs=outputs,
            signal_filters=[
                SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, None)
            ]
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        config = cast(TTSConfig, handler_config)
        self.voice = config.voice
        self.sample_rate = config.sample_rate
        self.ref_audio_path = config.ref_audio_path
        self.ref_audio_text = config.ref_audio_text
        self.model_name = config.model_name
        if 'DASHSCOPE_API_KEY' in os.environ:
            # load API-key from environment variable DASHSCOPE_API_KEY
            dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
        else:
            dashscope.api_key = config.api_key  # set API-key manually

    def create_context(self, session_context, handler_config=None):
        if not isinstance(handler_config, TTSConfig):
            handler_config = TTSConfig()
        context = TTSContext(session_context.session_info.session_id)
        if context.dump_audio:
            dump_file_path = os.path.join(DirectoryInfo.get_project_dir(), 'temp',
                                          f"dump_avatar_audio_{context.session_id}_{time.localtime().tm_hour}_{time.localtime().tm_min}.pcm")
            context.audio_dump_file = open(dump_file_path, "wb")
        return context

    def start_context(self, session_context, context: HandlerContext):
        context = cast(TTSContext, context)

    def filter_text(self, text):
        pattern = r"[^a-zA-Z0-9\u4e00-\u9fff,.\~!?，。！？ ]"  # 匹配不在范围内的字符
        filtered_text = re.sub(pattern, "", text)
        return filtered_text

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(TTSContext, context)
        if inputs.type == ChatDataType.AVATAR_TEXT:
            context.handle_text_stream(inputs, self)

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        """处理 STREAM_CANCEL 信号，终止被取消的 stream 的处理"""
        context = cast(TTSContext, context)
        if signal.type == ChatSignalType.STREAM_CANCEL and signal.related_stream:
            stream_key = signal.related_stream.key
            if stream_key is None:
                return
            # 检查是否为我们的输入流被取消
            session = context.api_links.pop(stream_key, None)
            if session:
                logger.info(f"TTS: Cancelling session for input stream {stream_key}")
                session.reset()
                return
            # 检查是否为我们的输出流被取消（例如下游发起的打断）
            for key, session in list(context.api_links.items()):
                if session.output_stream_key == stream_key:
                    logger.info(f"TTS: Cancelling session for output stream {stream_key}")
                    session.reset()
                    context.api_links.pop(key, None)
                    return

    def destroy_context(self, context: HandlerContext):
        context = cast(TTSContext, context)
        logger.info('destroy context')
        for session in context.api_links.values():
            try:
                session.reset()
            except Exception as e:
                logger.opt(exception=e).warning("Failed to reset BailianTTS session on destroy")
        context.api_links.clear()
        if context.audio_dump_file is not None:
            try:
                context.audio_dump_file.close()
            except Exception:
                pass


class CosyvoiceCallBack(ResultCallback):
    def __init__(self, context: TTSContext, output_definition,
                 session: BailianTTSSession):
        super().__init__()
        self.context = context
        self.output_definition = output_definition
        self.session = session
        self.temp_bytes = b''
        self._finished = False

    @property
    def is_cancelled(self) -> bool:
        return self.session.cancelled

    def on_open(self) -> None:
        logger.info('TTS: WebSocket connected')

    def on_event(self, message) -> None:
        pass

    def _submit_end_frame(self) -> None:
        if self._finished:
            return
        self._finished = True
        # 如果 session 已被取消，不要提交结束帧（避免 finish 掉新的 stream）
        if self.is_cancelled:
            return
        output = DataBundle(self.output_definition)
        output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
        self.context.submit_data(output, finish_stream=True)

    def on_data(self, data: bytes) -> None:
        if self.is_cancelled:
            return
        self.temp_bytes += data
        if len(self.temp_bytes) > 24000:
            output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(
                np.float32) / 32767
            output_audio = output_audio[np.newaxis, ...]
            output = DataBundle(self.output_definition)
            output.set_main_data(output_audio)
            self.context.submit_data(output)
            self.temp_bytes = b''

    def on_complete(self) -> None:
        if self.is_cancelled:
            self.temp_bytes = b''
            logger.info('TTS: Synthesis cancelled, skipping output in on_complete')
            return
        if len(self.temp_bytes) > 0:
            output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(np.float32) / 32767
            output_audio = output_audio[np.newaxis, ...]
            output = DataBundle(self.output_definition)
            output.set_main_data(output_audio)
            self.context.submit_data(output)
            self.temp_bytes = b''
        self._submit_end_frame()
        logger.info('TTS: Synthesis complete')

    def on_error(self, message) -> None:
        if self.is_cancelled:
            logger.info(f'TTS: Synthesis error after cancel (expected): {message}')
            return
        logger.error(f'TTS: Service error: {message}')
        self._submit_end_frame()

    def on_close(self) -> None:
        if self.is_cancelled:
            self.temp_bytes = b''
            logger.info('TTS: Synthesis cancelled, skipping output in on_close')
            return
        logger.info('TTS: WebSocket closed')
