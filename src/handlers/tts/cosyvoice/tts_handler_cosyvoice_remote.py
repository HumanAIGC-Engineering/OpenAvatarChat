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
import requests
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from engine_utils.directory_info import DirectoryInfo


class TTSConfig(HandlerBaseConfigModel, BaseModel):
    api_url: str = Field(default="http://127.0.0.1:50000/inference_zero_shot")
    spk_id: str = Field(default=None)
    ref_audio_path: str = Field(default=None)
    ref_audio_text: str = Field(default=None)
    sample_rate: int = Field(default=24000)
    stream: bool = Field(default=True)
    speed: float = Field(default=1.0)
    # 远程服务返回的音频采样率
    remote_sample_rate: int = Field(default=22050)


class TTSContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.local_session_id = 0
        self.input_text = ''
        self.dump_audio = False
        self.audio_dump_file = None
        self.current_speech_id = None
        self.is_processing = False


class HandlerTTS(HandlerBase, ABC):
    def __init__(self):
        super().__init__()

        self.api_url = None
        self.spk_id = None
        self.ref_audio_path = None
        self.ref_audio_text = None
        self.sample_rate = None
        self.stream = True
        self.speed = 1.0
        self.remote_sample_rate = 22050

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
        self.api_url = config.api_url
        self.spk_id = config.spk_id
        self.ref_audio_path = config.ref_audio_path
        self.ref_audio_text = config.ref_audio_text
        self.sample_rate = config.sample_rate
        self.stream = config.stream
        self.speed = config.speed
        self.remote_sample_rate = config.remote_sample_rate
        
        logger.info(f"CosyVoice Remote TTS 已加载，API地址: {self.api_url}")
        if self.spk_id:
            logger.info(f"使用音色ID: {self.spk_id}")
        if self.ref_audio_path:
            logger.info(f"使用参考音频: {self.ref_audio_path}")

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

    def call_remote_tts(self, text: str, context: TTSContext, output_definition, speech_id: str):
        """调用远程CosyVoice服务"""
        try:
            # 准备请求参数
            params = {
                'tts_text': text,
            }
            #目前只支持 inference_zero_shot 接口
            if 'inference_zero_shot' not in self.api_url:
                raise Exception("目前只支持 inference_zero_shot 接口")

            # 根据配置选择使用spk_id还是参考音频
            if self.ref_audio_path and self.ref_audio_text:
                params['prompt_text'] = self.ref_audio_text
            else:
                raise Exception("请配置参考音频和文字")

            logger.info(f"调用远程TTS API: {text[:50]}...")
            files = [('prompt_wav', ('prompt_wav', open(self.ref_audio_path, 'rb'), 'application/octet-stream'))]
            response = requests.request("POST",self.api_url, data=params, files=files, stream=True)
            if response.status_code != 200:
                logger.error(f"远程TTS API返回错误状态码 {response.status_code}")
                logger.error(f"响应内容: {response.text}")
                self._send_end_signal(context, output_definition, speech_id)
                return
            
            # 处理流式响应
            temp_bytes = b''
            chunk_size = self.sample_rate * 2  # 1秒的数据量（16bit = 2 bytes）
            
            for chunk in response.iter_content(chunk_size=16000):
                if chunk:
                    temp_bytes += chunk
                    
                    # 当累积足够的数据时，进行处理和发送
                    if len(temp_bytes) >= chunk_size:
                        audio_data = self._process_audio_chunk(temp_bytes, context)
                        if audio_data is not None:
                            self._send_audio_data(context, output_definition, audio_data, speech_id, False)
                        temp_bytes = b''
            
            # 处理剩余的数据
            if len(temp_bytes) > 0:
                audio_data = self._process_audio_chunk(temp_bytes, context)
                if audio_data is not None:
                    self._send_audio_data(context, output_definition, audio_data, speech_id, False)
            
            logger.info(f"TTS合成完成: {text[:50]}...")
            
        except requests.exceptions.Timeout:
            logger.error("远程TTS API请求超时")
            self._send_end_signal(context, output_definition, speech_id)
        except requests.exceptions.RequestException as e:
            logger.error(f"远程TTS API请求失败: {e}")
            self._send_end_signal(context, output_definition, speech_id)
        except Exception as e:
            logger.error(f"调用远程TTS时发生错误: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self._send_end_signal(context, output_definition, speech_id)

    def _process_audio_chunk(self, audio_bytes: bytes, context: TTSContext) -> Optional[np.ndarray]:
        """处理音频数据块"""
        try:
            # 将字节数据转换为numpy数组
            audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32767.0
            
            # 如果远程服务的采样率与目标采样率不同，进行重采样
            if self.remote_sample_rate != self.sample_rate:
                audio_data = librosa.resample(
                    audio_data, 
                    orig_sr=self.remote_sample_rate, 
                    target_sr=self.sample_rate
                )
            
            # 添加batch维度
            audio_data = audio_data[np.newaxis, ...]
            
            if context.dump_audio and context.audio_dump_file:
                context.audio_dump_file.write(audio_data.tobytes())
            
            return audio_data
            
        except Exception as e:
            logger.error(f"处理音频数据块时发生错误: {e}")
            return None

    def _send_audio_data(self, context: TTSContext, output_definition, 
                        audio_data: np.ndarray, speech_id: str, is_end: bool):
        """发送音频数据"""
        output = DataBundle(output_definition)
        output.set_main_data(audio_data)
        output.add_meta("avatar_speech_end", is_end)
        output.add_meta("speech_id", speech_id)
        context.submit_data(output)

    def _send_end_signal(self, context: TTSContext, output_definition, speech_id: str):
        """发送结束信号"""
        output = DataBundle(output_definition)
        output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
        output.add_meta("avatar_speech_end", True)
        output.add_meta("speech_id", speech_id)
        context.submit_data(output)
        logger.info(f"语音结束信号已发送，speech_id: {speech_id}")

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_AUDIO).definition
        context = cast(TTSContext, context)
        
        if inputs.type == ChatDataType.AVATAR_TEXT:
            text = inputs.data.get_main_data()
        else:
            return
        
        speech_id = inputs.data.get_meta("speech_id")
        if speech_id is None:
            speech_id = context.session_id

        if text is not None:
            text = re.sub(r"<\|.*?\|>", "", text)
            text = self.filter_text(text)
            context.input_text += text

        text_end = inputs.data.get_meta("avatar_text_end", False)
        
        if not text_end:
            # 流式处理：按句子分割
            sentences = re.split(r'(?<=[,.~!?，。！？])', context.input_text)
            if len(sentences) > 1:  # 至少有一个完整句子
                complete_sentences = sentences[:-1]  # 完整句子
                context.input_text = sentences[-1]  # 剩余的未完成部分

                # 对完整句子进行处理
                for sentence in complete_sentences:
                    sentence = sentence.strip()
                    if len(sentence) < 1:
                        continue
                    logger.info(f'处理句子: {sentence}')
                    self.call_remote_tts(sentence, context, output_definition, speech_id)
        else:
            # 处理最后一句
            if context.input_text and len(context.input_text.strip()) > 0:
                logger.info(f'处理最后一句: {context.input_text}')
                self.call_remote_tts(context.input_text, context, output_definition, speech_id)
            
            context.input_text = ''
            # 发送结束信号
            self._send_end_signal(context, output_definition, speech_id)

    def destroy_context(self, context: HandlerContext):
        context = cast(TTSContext, context)
        logger.info('销毁上下文')
        if context.audio_dump_file:
            context.audio_dump_file.close()

