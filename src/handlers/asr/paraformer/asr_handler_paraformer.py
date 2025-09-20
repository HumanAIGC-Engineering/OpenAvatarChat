import re
import os
import time
import threading
import queue
from typing import Dict, Optional, cast, Union, List, Any
from loguru import logger
import numpy as np
from pydantic import BaseModel, Field
from abc import ABC
import torch
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry
from chat_engine.contexts.session_context import SessionContext
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult

from engine_utils.directory_info import DirectoryInfo
from engine_utils.general_slicer import SliceContext, slice_data


class ASRConfig(HandlerBaseConfigModel, BaseModel):
    model_name: str = Field(default="paraformer-realtime-v2")
    api_key: str = Field(default=None)  # Field(default=os.getenv("DASHSCOPE_API_KEY"))
    sample_rate: int = Field(default=16000)
    format: str = Field(default="pcm")
    enable_intermediate_result: bool = Field(default=True)
    enable_punctuation_prediction: bool = Field(default=True)
    enable_inverse_text_normalization: bool = Field(default=True)
    language_hints: List[str] = Field(default=["zh", "en"])
    max_sentence_silence: int = Field(default=800)
    enable_emotion_recognition: bool = Field(default=False)
    enable_semantic_sentence_detection: bool = Field(default=False)


class ASRCallback(RecognitionCallback):
    def __init__(self, result_queue, session_id):
        self.result_queue = result_queue
        self.session_id = session_id
        
    def on_open(self) -> None:
        logger.info(f'ASR RecognitionCallback open for session {self.session_id}')
        
    def on_close(self) -> None:
        logger.info(f'ASR RecognitionCallback close for session {self.session_id}')
        
    def on_complete(self) -> None:
        logger.info(f'ASR RecognitionCallback completed for session {self.session_id}')
        
    def on_error(self, message) -> None:
        logger.error(f'ASR RecognitionCallback error for session {self.session_id}: {message.message}')
        self.result_queue.put(None)
        
    def on_event(self, result: RecognitionResult) -> None:
        logger.debug(f'ASR RecognitionCallback event for session {self.session_id}')
        self.result_queue.put(result)


class ASRContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.local_session_id = 0
        self.output_audios = []
        self.audio_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=16000,
            slice_axis=0,
        )
        self.cache = {}
        self.recognition = None
        self.recognition_thread = None
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.is_processing = False
        self.current_text = ""
        self.sentence_buffer = []
        self.callback = None

        self.dump_audio = True
        self.audio_dump_file = None
        if self.dump_audio:
            dump_file_path = os.path.join(DirectoryInfo.get_project_dir(),
                                          f"dump_talk_audio_{session_id}.pcm")
            # self.audio_dump_file = open(dump_file_path, "wb")
        self.shared_states = None


class HandlerASR(HandlerBase, ABC):
    def __init__(self):
        super().__init__()

        self.model_name = 'paraformer-realtime-v2'
        self.api_key = None
        self.sample_rate = 16000
        self.format = "pcm"
        self.enable_intermediate_result = True
        self.enable_punctuation_prediction = True
        self.enable_inverse_text_normalization = True
        self.language_hints = ["zh", "en"]
        self.max_sentence_silence = 800
        self.enable_emotion_recognition = False
        self.enable_semantic_sentence_detection = False

        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        else:
            self.device = torch.device("cpu")

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="ASR_Paraformer",
            config_model=ASRConfig,
        )

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_audio_entry("avatar_audio", 1, 16000))
        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
            )
        }
        outputs = {
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT,
                definition=definition,
            )
        }
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        if isinstance(handler_config, ASRConfig):
            self.model_name = handler_config.model_name
            self.api_key = handler_config.api_key or os.getenv("DASHSCOPE_API_KEY")
            self.sample_rate = handler_config.sample_rate
            self.format = handler_config.format
            self.enable_intermediate_result = handler_config.enable_intermediate_result
            self.enable_punctuation_prediction = handler_config.enable_punctuation_prediction
            self.enable_inverse_text_normalization = handler_config.enable_inverse_text_normalization
            self.language_hints = handler_config.language_hints
            self.max_sentence_silence = handler_config.max_sentence_silence
            self.enable_emotion_recognition = handler_config.enable_emotion_recognition
            self.enable_semantic_sentence_detection = handler_config.enable_semantic_sentence_detection

        if not self.api_key:
            raise ValueError("API key is required for Paraformer ASR. Please set DASHSCOPE_API_KEY environment variable or provide api_key in config.")
        
        # 设置DashScope API密钥
        import dashscope
        dashscope.api_key = self.api_key

    def create_context(self, session_context, handler_config=None):
        if not isinstance(handler_config, ASRConfig):
            handler_config = ASRConfig()
        context = ASRContext(session_context.session_info.session_id)
        context.shared_states = session_context.shared_states
        return context
    
    def start_context(self, session_context, handler_context):
        context = cast(ASRContext, handler_context)
        
        # 创建回调
        context.callback = ASRCallback(context.result_queue, context.session_id)
        
        # 初始化识别器（但不立即启动）
        context.recognition = None
        context.is_processing = False
        
        logger.info(f"ASR context started for session {context.session_id}")

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):

        output_definition = output_definitions.get(ChatDataType.HUMAN_TEXT).definition
        context = cast(ASRContext, context)
        if inputs.type == ChatDataType.HUMAN_AUDIO:
            audio = inputs.data.get_main_data()
        else:
            return
        speech_id = inputs.data.get_meta("speech_id")
        if (speech_id is None):
            speech_id = context.session_id

        if audio is not None:
            audio = audio.squeeze()
            
            # 转换音频格式为16位PCM
            if audio.dtype != np.int16:
                audio = (audio * 32767).astype(np.int16)
            
            logger.info('audio in')
            
            # 如果是第一次音频输入，启动识别器
            if not context.is_processing:
                context.recognition = Recognition(
                    model=self.model_name,
                    format=self.format,
                    sample_rate=self.sample_rate,
                    semantic_punctuation_enabled=self.enable_semantic_sentence_detection,
                    callback=context.callback
                )
                context.recognition.start()
                context.is_processing = True
                logger.info(f"ASR recognition started for session {context.session_id}")
            
            for audio_segment in slice_data(context.audio_slice_context, audio):
                if audio_segment is None or audio_segment.shape[0] == 0:
                    continue
                context.output_audios.append(audio_segment)
                
                # 直接发送音频数据到识别器
                if context.is_processing and context.recognition:
                    context.recognition.send_audio_frame(audio_segment.tobytes())

        speech_end = inputs.data.get_meta("human_speech_end", False)
        if not speech_end:
            # 处理中间结果
            for result in self._process_intermediate_results(context, output_definition, speech_id):
                yield result
            return

        # 处理最终结果
        for result in self._process_final_results(context, output_definition, speech_id):
            yield result

    def _process_intermediate_results(self, context: ASRContext, output_definition, speech_id):
        """处理中间识别结果"""
        try:
            while not context.result_queue.empty():
                result = context.result_queue.get_nowait()
                if result is None:
                    continue
                    
                # 获取句子信息
                sentence = result.get_sentence()
                if sentence and sentence.get('text'):
                    text = sentence['text'].strip()
                    if text:
                        # 检查是否是句子结束
                        if RecognitionResult.is_sentence_end(sentence):
                            if text not in context.sentence_buffer:
                                context.sentence_buffer.append(text)
                                logger.info(f'Intermediate result: {text}')
                                
                                # 输出中间结果
                                output = DataBundle(output_definition)
                                output.set_main_data(text)
                                output.add_meta('human_text_end', False)
                                output.add_meta('speech_id', speech_id)
                                yield output
                        else:
                            # 非句子结束的中间结果
                            logger.debug(f'Partial result: {text}')
                            
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f"Error processing intermediate results: {e}")
        
        # 如果没有结果，返回空生成器
        if False:  # 确保函数是生成器
            yield

    def _process_final_results(self, context: ASRContext, output_definition, speech_id):
        """处理最终识别结果"""
        # 停止识别
        if context.recognition and context.is_processing:
            try:
                context.recognition.stop()
                logger.info(f"ASR recognition stopped for session {context.session_id}")
            except Exception as e:
                logger.debug(f"Recognition already stopped: {e}")
        
        context.is_processing = False
        context.recognition = None
        
        # 处理剩余的结果
        final_text = ""
        try:
            while not context.result_queue.empty():
                result = context.result_queue.get_nowait()
                if result is None:
                    continue
                    
                sentence = result.get_sentence()
                if sentence and sentence.get('text'):
                    text = sentence['text'].strip()
                    if text:
                        final_text += text
                        
        except queue.Empty:
            pass
        except Exception as e:
            logger.error(f"Error processing final results: {e}")
        
        # 清理音频缓存
        context.output_audios.clear()
        context.sentence_buffer.clear()
        
        # 输出最终结果
        if final_text:
            final_text = re.sub(r"<\|.*?\|>", "", final_text)
            logger.info(f'Final result: {final_text}')
            
            output = DataBundle(output_definition)
            output.set_main_data(final_text)
            output.add_meta('human_text_end', False)
            output.add_meta('speech_id', speech_id)
            yield output
        else:
            # 如果 ASR 识别结果为空，则需要重新开启vad
            if context.shared_states:
                context.shared_states.enable_vad = True
            return

        # 输出结束信号
        end_output = DataBundle(output_definition)
        end_output.set_main_data('')
        end_output.add_meta("human_text_end", True)
        end_output.add_meta("speech_id", speech_id)
        yield end_output

    def destroy_context(self, context: HandlerContext):
        context = cast(ASRContext, context)
        
        # 停止处理
        context.is_processing = False
        
        # 关闭识别器
        if context.recognition:
            try:
                context.recognition.stop()
                logger.info(f"ASR recognition stopped during destroy for session {context.session_id}")
            except Exception as e:
                logger.debug(f"Recognition already stopped during destroy: {e}")
        
        context.recognition = None
        
        # 关闭音频文件
        if context.audio_dump_file:
            context.audio_dump_file.close()
            
        logger.info(f"ASR context destroyed for session {context.session_id}")