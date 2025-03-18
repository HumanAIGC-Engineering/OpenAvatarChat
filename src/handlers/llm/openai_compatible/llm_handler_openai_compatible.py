

import base64
from io import BytesIO
import os
import re
from typing import Dict, Optional, cast
import PIL
import numpy as np
from loguru import logger
from pydantic import BaseModel, Field
from abc import ABC
from openai import OpenAI
import torch
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry


class LLMConfig(HandlerBaseConfigModel, BaseModel):
    model_name: str = Field(default="qwen-plus")
    system_prompt: str = Field(default="你是个AI对话数字人，你要用简短的对话来回答我的问题，并在合理的地方插入标点符号")
    api_key: str = Field(default=os.getenv("DASHSCOPE_API_KEY"))
    api_url: str = Field(default=None)


class LLMContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.local_session_id = 0
        self.output_texts = ""
        self.current_image = None


class HandlerLLM(HandlerBase, ABC):
    def __init__(self):
        super().__init__()

        self.model_name = None
        self.system_prompt = None
        self.api_key = None
        self.api_url = None
        self.client = None
        if torch.cuda.is_available():
            self.device = torch.device("cuda:0")
        elif torch.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="LLM_Bailian",
            config_model=LLMConfig,
        )

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry.create_text_entry("avatar_text"))
        inputs = {
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT,
            ),
            ChatDataType.CAMERA_VIDEO: HandlerDataInfo(
                type=ChatDataType.CAMERA_VIDEO,
            ),
        }
        outputs = {
            ChatDataType.AVATAR_TEXT: HandlerDataInfo(
                type=ChatDataType.AVATAR_TEXT,
                definition=definition,
            )
        }
        return HandlerDetail(
            inputs=inputs, outputs=outputs,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        if isinstance(handler_config, LLMConfig):
            self.model_name = handler_config.model_name
            self.system_prompt = {'role': 'system', 'content': handler_config.system_prompt}
            self.api_key = handler_config.api_key
            self.api_url = handler_config.api_url
            if self.api_key is None or len(self.api_key) == 0:
                error_message = 'api_key is required in config/sample.yaml, when use handler_llm'
                logger.error(error_message)
                raise ValueError(error_message)
            self.client = OpenAI(
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=self.api_key,
                base_url=self.api_url,
            )

    @staticmethod
    def _create_message(text: str):
        if text is None:
            return None
        msg = {"role": "user", "content": text}
        return msg

    def create_context(self, session_context, handler_config=None):
        if not isinstance(handler_config, LLMConfig):
            handler_config = LLMConfig()
        context = LLMContext(session_context.session_info.session_id)
        return context
    
    def start_context(self, session_context, handler_context):
        pass

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_TEXT).definition
        context = cast(LLMContext, context)
        text = None
        if inputs.type == ChatDataType.CAMERA_VIDEO:
            context.current_image = inputs.data.get_main_data()
            return
        elif inputs.type == ChatDataType.HUMAN_TEXT:
            text = inputs.data.get_main_data()
        else:
            return
        speech_id = inputs.data.get_meta("speech_id")
        if (speech_id is None):
            speech_id = context.session_id

        if text is not None:
            context.output_texts += text

        text_end = inputs.data.get_meta("human_text_end", False)
        if not text_end:
            return

        chat_text = context.output_texts
        chat_text = re.sub(r"<\|.*?\|>", "", chat_text)
        if len(chat_text) < 1:
            return

        current_image = self.numpy2base64(context.current_image) if context.current_image is not None else None
        current_content = [
            # 如果有图片，则添加图片信息；否则只保留文本内容
            {"type": "text", "text": chat_text},  # 纯文本部分
            {"type": "image_url", "image_url": {"url": current_image}}  # 图片 URL 部分（如果有图片）
        ] if current_image is not None else [
            {"type": "text", "text": chat_text}
        ]
        logger.info(f'llm input {self.model_name} {chat_text} ')
        completion = self.client.chat.completions.create(
            model=self.model_name,  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                self.system_prompt,
                {'role': 'user', 'content': current_content}
            ],
            stream=True,
            stream_options={"include_usage": True}
        )
        context.current_image = None
        context.output_texts = ''
        for chunk in completion:
            if (chunk and chunk.choices and chunk.choices[0] and chunk.choices[0].delta.content):
                output_text = chunk.choices[0].delta.content
                logger.info(output_text)
                output = DataBundle(output_definition)
                output.set_main_data(output_text)
                output.add_meta("avatar_text_end", False)
                output.add_meta("speech_id", speech_id)
                yield output
        logger.info('avatar text end')
        end_output = DataBundle(output_definition)
        end_output.set_main_data('')
        end_output.add_meta("avatar_text_end", True)
        end_output.add_meta("speech_id", speech_id)
        yield end_output

    def destroy_context(self, context: HandlerContext):
        pass

    def numpy2base64(self, video_frame, format="JPEG"):
        # if video_frame.dtype != np.uint8:
        #     video_frame = (video_frame * 255).astype(np.uint8)

        # 将 NumPy 数组转换为 PIL 图像对象
        image = PIL.Image.fromarray(np.squeeze(video_frame))

        # 创建一个内存缓冲区
        buffered = BytesIO()

        # 将图像保存到内存缓冲区中
        image.save(buffered, format=format)

        # 获取二进制数据并编码为 Base64
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # 添加 Base64 数据头（可选）
        data_url = f"data:image/{format.lower()};base64,{base64_image}"

        return data_url
