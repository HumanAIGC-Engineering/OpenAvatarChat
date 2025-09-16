import io
import os
import re
import time
from typing import Dict, Optional, cast
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


class TTSConfig(HandlerBaseConfigModel, BaseModel):
    ref_audio_path: str = Field(default=None)
    ref_audio_text: str = Field(default=None)
    voice: str = Field(default=None)
    sample_rate: int = Field(default=24000)
    api_key: str = Field(default=os.getenv("DASHSCOPE_API_KEY"))
    model_name: str = Field(default="cosyvoice-1")


class TTSContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.local_session_id = 0
        self.input_text = ''
        self.dump_audio = False
        self.audio_dump_file = None
        self.synthesizer = None


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
        inputs = {
            ChatDataType.AVATAR_TEXT: HandlerDataInfo(
                type=ChatDataType.AVATAR_TEXT,
            )
        }
        outputs = {
            ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
                type=ChatDataType.AVATAR_AUDIO,
                definition=definition,
            )
        }
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
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
        context.input_text = ''
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
        output_definition = output_definitions.get(ChatDataType.AVATAR_AUDIO).definition
        context = cast(TTSContext, context)
        if inputs.type == ChatDataType.AVATAR_TEXT:
            text = inputs.data.get_main_data()
        else:
            return
        speech_id = inputs.data.get_meta("speech_id")
        if (speech_id is None):
            speech_id = context.session_id

        if text is not None:
            text = re.sub(r"<\|.*?\|>", "", text)

        text_end = inputs.data.get_meta("avatar_text_end", False)
        try:
            if not text_end:
                if context.synthesizer is None:
                    callback = CosyvoiceCallBack(
                        context=context, output_definition=output_definition, speech_id=speech_id)
                    context.synthesizer = SpeechSynthesizer(
                        model=self.model_name, voice=self.voice, callback=callback, format=AudioFormat.PCM_24000HZ_MONO_16BIT)
                logger.info(f'streaming_call {text}')
                context.synthesizer.streaming_call(text)
            else:
                logger.info(f'streaming_call last {text}')
                context.synthesizer.streaming_call(text)
                context.synthesizer.streaming_complete()
                context.synthesizer = None
                context.input_text = ''
        except Exception as e:
            logger.error(e)
            context.synthesizer.streaming_complete()
            context.synthesizer = None

    def destroy_context(self, context: HandlerContext):
        context = cast(TTSContext, context)
        logger.info('destroy context')


class CosyvoiceCallBack(ResultCallback):
    def __init__(self, context: TTSContext, output_definition, speech_id):
        super().__init__()
        self.context = context
        self.output_definition = output_definition
        self.speech_id = speech_id
        self.temp_bytes = b''

    def on_open(self) -> None:
        logger.info('连接成功')

    def on_event(self, message) -> None:
        # 实现接收合成结果的逻辑
        # logger.info(message)
        pass

    def on_data(self, data: bytes) -> None:
        self.temp_bytes += data
        if len(self.temp_bytes) > 24000:
            # 实现接收合成二进制音频结果的逻辑
            output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(
                np.float32)/32767  # librosa.load(io.BytesIO(self.temp_bytes), sr=None)[0]
            output_audio = output_audio[np.newaxis, ...]
            output = DataBundle(self.output_definition)
            output.set_main_data(output_audio)
            output.add_meta("avatar_speech_end", False)
            output.add_meta("speech_id", self.speech_id)
            self.context.submit_data(output)
            self.temp_bytes = b''

    def on_complete(self) -> None:
        if len(self.temp_bytes) > 0:
            output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(np.float32)/32767
            output_audio = output_audio[np.newaxis, ...]
            output = DataBundle(self.output_definition)
            output.set_main_data(output_audio)
            output.add_meta("avatar_speech_end", False)
            output.add_meta("speech_id", self.speech_id)
            self.context.submit_data(output)
            self.temp_bytes = b''
        output = DataBundle(self.output_definition)
        output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
        output.add_meta("avatar_speech_end", True)
        output.add_meta("speech_id", self.speech_id)
        self.context.submit_data(output)
        logger.info(f"speech end")
        logger.info('合成完成')

    def on_error(self, message) -> None:
        logger.error(f'bailian tts 服务出现异常,请确保参数正确：${message}')
        output = DataBundle(self.output_definition)
        output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
        output.add_meta("avatar_speech_end", True)
        output.add_meta("speech_id", self.speech_id)
        self.context.submit_data(output)
        logger.info(f"speech end")

    def on_close(self) -> None:
        logger.info('连接关闭')
