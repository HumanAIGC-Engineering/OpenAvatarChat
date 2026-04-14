# handlers/llm/dify/llm_handler_dify.py

import os
import re
import json
import PIL
import numpy as np
import requests
from typing import Dict, Optional, Set, cast
from loguru import logger
from pydantic import BaseModel, Field
from abc import ABC
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.chat_stream import StreamKey
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry

# only support chatflow
class DifyConfig(HandlerBaseConfigModel, BaseModel):
    api_key: str = Field(default=os.getenv("DIFY_API_KEY"))
    api_url: str = Field(default="https://api.dify.ai/v1")
    enable_video_input: bool = Field(default=False)
    response_mode: str = Field(default="streaming")  # streaming or blocking
    timeout: int = Field(default=30)


class DifyContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config = None
        self.api_key = None
        self.api_url = None
        self.response_mode = None
        self.timeout = None
        self.input_texts = ""
        self.output_texts = ""
        self.current_image = None
        self.enable_video_input = False
        self.conversation_id = None  # Dify 特有的对话ID
        self.active_stream_keys: Set[StreamKey] = set()


class HandlerDify(HandlerBase, ABC):
    def __init__(self):
        super().__init__()

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=DifyConfig,
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
            signal_filters=[
                SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, None)
            ]
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        if isinstance(handler_config, DifyConfig):
            if handler_config.api_key is None or len(handler_config.api_key) == 0:
                error_message = 'api_key is required in config/xxx.yaml, when use handler_dify'
                logger.error(error_message)
                raise ValueError(error_message)

    def create_context(self, session_context, handler_config=None):
        if not isinstance(handler_config, DifyConfig):
            handler_config = DifyConfig()
        context = DifyContext(session_context.session_info.session_id)
        context.api_key = handler_config.api_key
        context.api_url = handler_config.api_url
        context.response_mode = handler_config.response_mode
        context.timeout = handler_config.timeout
        context.enable_video_input = handler_config.enable_video_input
        return context

    def start_context(self, session_context, handler_context):
        pass

    def _upload_image_to_dify(self, context: DifyContext, image_data):
        """
        上传图像到 Dify 并返回文件信息
        """
        upload_url = f"{context.api_url}/files/upload"
        headers = {
            "Authorization": f"Bearer {context.api_key}"
        }

        # 假设 image_data 是 PIL 图像或 numpy 数组，需先保存为临时文件
        from io import BytesIO
        buffered = BytesIO()

        image = PIL.Image.fromarray(np.squeeze(image_data)[..., ::-1])
        image.save(buffered, format="JPEG")  # 可根据需要调整格式
        img_bytes = buffered.getvalue()

        files = {
            'file': ('image.jpg', img_bytes, 'image/jpeg'),
        }

        response = requests.post(upload_url, headers=headers, files=files, data={'user': context.session_id})
        if response.status_code < 400:
            result = response.json()
            return result.get("id")  # 返回文件 ID
        else:
            logger.error(f"Failed to upload image:{response.status_code} {response.text}")
            return None

    def _send_dify_request(self, context: DifyContext, chat_text: str, images=None):
        """
        发送请求到 Dify API
        """
        url = f"{context.api_url}/chat-messages"
        headers = {
            "Authorization": f"Bearer {context.api_key}",
            "Content-Type": "application/json"
        }

        # 构建消息内容
        query = chat_text
        inputs = {"query": query}

        # 如果有图片，需要特殊处理
        files = []
        if images and len(images) > 0:
            for img in images:
                if img is not None:
                    file_id = self._upload_image_to_dify(context, img)
                    if file_id:
                        files.append({
                            "type": "image",
                            "transfer_method": "local_file",  
                            "upload_file_id": file_id  # 使用上传后的文件 ID
                        })

        payload = {
            "inputs": inputs,
            "query": query,
            "response_mode": context.response_mode,
            "conversation_id": context.conversation_id,
            "user": context.session_id
        }

        if files and len(files) > 0:
            payload["files"] = files
            # payload["inputs"]['files'] = files

        logger.info(f"payload: {payload}")
        try:
            if context.response_mode == "streaming":
                with requests.post(url, headers=headers, json=payload, stream=True, timeout=context.timeout) as response:
                    if response.status_code != 200:
                        error_text = response.text
                        logger.error(f"Dify API error: {response.status_code} - {error_text}")
                        yield f"Error: {response.status_code} - {error_text}"
                        return

                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith("data: "):
                                data = line_str[6:]  # 移除 "data: " 前缀
                                if data.strip() == "[DONE]":
                                    break
                                try:
                                    json_data = json.loads(data)
                                    if "answer" in json_data:
                                        yield json_data["answer"]
                                    elif "conversation_id" in json_data and json_data["conversation_id"]:
                                        context.conversation_id = json_data["conversation_id"]
                                except json.JSONDecodeError:
                                    logger.warning(f"Failed to parse JSON: {data}")
            else:  # blocking mode
                response = requests.post(url, headers=headers, json=payload, timeout=context.timeout)
                if response.status_code != 200:
                    error_text = response.text
                    logger.error(f"Dify API error: {response.status_code} - {error_text}")
                    yield f"Error: {response.status_code} - {error_text}"
                    return

                json_data = response.json()
                if "answer" in json_data:
                    yield json_data["answer"]
                if "conversation_id" in json_data and json_data["conversation_id"]:
                    context.conversation_id = json_data["conversation_id"]

        except requests.exceptions.Timeout:
            logger.error("Dify API timeout")
            yield "Error: Request to Dify API timed out"
        except requests.exceptions.RequestException as e:
            logger.error(f"Dify API request error: {str(e)}")
            yield f"Error: Failed to connect to Dify API: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error when calling Dify API: {str(e)}")
            yield f"Error: Unexpected error occurred: {str(e)}"

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        output_definition = output_definitions.get(ChatDataType.AVATAR_TEXT).definition
        context = cast(DifyContext, context)
        streamer = context.data_submitter.get_streamer(ChatDataType.AVATAR_TEXT)
        stream = streamer.new_stream(
            sources=[inputs.stream_id], name="dify", config=ChatStreamConfig(cancelable=True))
        stream_key = stream.stream_key_str
        text = None
        if inputs.type == ChatDataType.CAMERA_VIDEO and context.enable_video_input:
            context.current_image = inputs.data.get_main_data()
            return
        elif inputs.type == ChatDataType.HUMAN_TEXT:
            text = inputs.data.get_main_data()
        else:
            return

        if text is not None:
            context.input_texts += text

        text_end = inputs.is_last_data
        if not text_end:
            return

        chat_text = context.input_texts
        chat_text = re.sub(r"<\|.*?\|>", "", chat_text)
        if len(chat_text) < 1:
            end_output = DataBundle(output_definition)
            end_output.set_main_data('')
            streamer.stream_data(end_output, finish_stream=True)
            return

        logger.info(f'Dify input: {chat_text}')
        if stream_key:
            context.active_stream_keys.add(stream_key)

        try:
            context.output_texts = ''
            cancelled = False
            for output_text in self._send_dify_request(context, chat_text,
                                                       [context.current_image] if context.current_image is not None else []):
                if stream_key and stream_key not in context.active_stream_keys:
                    logger.info(f"Dify: Stream {stream_key} no longer active, stopping output")
                    cancelled = True
                    break
                if output_text:
                    context.output_texts += output_text
                    logger.info(output_text)
                    output = DataBundle(output_definition)
                    output.set_main_data(output_text)
                    streamer.stream_data(output)
        except Exception as e:
            logger.error(f"Error processing Dify response: {str(e)}")
            error_message = f"Error: {str(e)}"
            output = DataBundle(output_definition)
            output.set_main_data(error_message)
            streamer.stream_data(output, finish_stream=True)
            cancelled = False

        context.input_texts = ''
        context.current_image = None
        if cancelled:
            return
        if stream_key:
            context.active_stream_keys.discard(stream_key)
        logger.info('avatar text end')
        end_output = DataBundle(output_definition)
        end_output.set_main_data('')
        streamer.stream_data(end_output, finish_stream=True)

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        context = cast(DifyContext, context)
        if signal.type == ChatSignalType.STREAM_CANCEL and signal.related_stream:
            stream_key = signal.related_stream.stream_key_str
            if stream_key is not None and stream_key in context.active_stream_keys:
                context.active_stream_keys.discard(stream_key)
                logger.info(f"Dify: Removed stream {stream_key} from active set")

    def destroy_context(self, context: HandlerContext):
        pass
