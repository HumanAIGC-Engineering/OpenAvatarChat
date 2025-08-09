import asyncio
import json
import os.path
from typing import Dict, Optional, cast

import gradio
from fastapi import FastAPI
from loguru import logger

from pydantic import BaseModel, Field
from starlette.responses import JSONResponse, FileResponse
from starlette.websockets import WebSocket, WebSocketState

from chat_engine.common.client_handler_base import ClientHandlerInfo, ClientSessionDelegate
from chat_engine.common.engine_channel_type import EngineChannelType
from chat_engine.common.handler_base import HandlerDataInfo, HandlerDetail, HandlerBaseInfo
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel, ChatEngineConfigModel
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalSourceType, ChatSignalType
from chat_engine.data_models.runtime_data.motion_data import MotionDataSerializer
from engine_utils.directory_info import DirectoryInfo
from handlers.client.rtc_client.client_handler_rtc import RtcClientSessionDelegate, ClientHandlerRtc, \
    ClientRtcConfigModel, ClientRtcContext


class LamClientSessionDelegate(RtcClientSessionDelegate):
    def __init__(self):
        super().__init__()
        self.output_queues[EngineChannelType.MOTION_DATA] = asyncio.Queue()
        self.quit = asyncio.Event()

    async def _ws_output_task(self, websocket: WebSocket):
        logger.warning(f"Send task started on {websocket}")
        self.motion_data_serializer = MotionDataSerializer()
        self.motion_data_serializer.register_audio_data("avatar_audio")
        self.motion_data_serializer.register_data(
            "arkit_face",
            "arkit_face",
            "float32"
        )
        welcome_message_sent = False
        while not self.quit.is_set():
            try:
                chat_data: ChatData = await asyncio.wait_for(self.get_data(EngineChannelType.MOTION_DATA), timeout=0.1)
                logger.info(f"Got chat data {str(chat_data)}")
            except asyncio.TimeoutError:
                continue
            if not welcome_message_sent:
                welcome_message = self.motion_data_serializer.serialize(chat_data.data.definition)
                await websocket.send_bytes(welcome_message)
                welcome_message_sent = True
            if chat_data.type == ChatDataType.AVATAR_MOTION_DATA:
                msg = self.motion_data_serializer.serialize(chat_data.data)
                await websocket.send_bytes(msg)

    async def _ws_input_task(self, websocket: WebSocket):
        while not self.quit.is_set() and websocket.client_state != WebSocketState.DISCONNECTED:
            try:
                raw_msg = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
            except asyncio.TimeoutError:
                continue
            logger.info(f"Received websocket message {raw_msg}")
            try:
                msg = json.loads(raw_msg)
                msg_type = msg.get("header", {}).get("name")
                if msg_type == "EndSpeech":
                    signal = ChatSignal(
                        source_type=ChatSignalSourceType.CLIENT,
                        type=ChatSignalType.END,
                    )
                    self.emit_signal(signal)
            except Exception as e:
                logger.error(f"Error occurs while processing client message: {e}")
                continue

    def emit_signal(self, signal):
        # TODO: this is temp implementation a full signal infrastructure is needed.
        super().emit_signal(signal)
        logger.info(signal)
        if signal.source_type == ChatSignalSourceType.CLIENT and signal.type == ChatSignalType.END:
            self.shared_states.enable_vad = True

    async def serve_websocket(self, websocket: WebSocket):
        logger.warning(f"Ready to serve websocket {websocket}")
        logger.warning(f"send task created")
        receive_task = asyncio.create_task(self._ws_input_task(websocket))
        send_task = asyncio.create_task(self._ws_output_task(websocket))
        await asyncio.gather(receive_task, send_task)
        send_task.cancel()
        receive_task.cancel()


class ClientLamConfigModel(ClientRtcConfigModel, BaseModel):
    asset_path: Optional[str] = Field(default=None)


class ClientLamContext(ClientRtcContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[ClientLamConfigModel] = None
        self.client_session_delegate: Optional[RtcClientSessionDelegate] = None


class ClientHandlerLam(ClientHandlerRtc):
    def __init__(self):
        super().__init__()
        self.asset_path = None
        self.asset_name = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=ClientLamConfigModel,
            client_session_delegate_class=LamClientSessionDelegate,
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        self.engine_config = engine_config
        self.handler_config = cast(ClientLamConfigModel, handler_config)
        self.prepare_rtc_definitions()

        candidate_path = []
        asset_path = self.handler_config.asset_path
        if os.path.isabs(asset_path):
            candidate_path.append(asset_path)
        else:
            candidate_path.append(os.path.abspath(asset_path))
            candidate_path.append(os.path.join(self.handler_root, asset_path))
            candidate_path.append(os.path.join(DirectoryInfo.get_project_dir(), asset_path))

        for asset_path in candidate_path:
            if os.path.isfile(asset_path):
                self.asset_path, self.asset_name = os.path.split(asset_path)
                break
        if self.asset_path is None or self.asset_name is None:
            msg = f"Asset file {self.handler_config.asset_path} not found."
            raise ValueError(msg)

    def on_setup_app(self, app: FastAPI, ui: gradio.blocks.Block, parent_block: Optional[gradio.blocks.Block] = None):
        asset_route = "/download/lam_asset"
        motion_data_route = "/ws/lam_data_stream"

        @app.websocket(motion_data_route + "/{rtc_id}")
        async def motion_data_stream(websocket: WebSocket, rtc_id: str):
            await websocket.accept()
            logger.info(f"Got websocket connection {websocket} for rtc_id {rtc_id}.")
            session_delegate = self.handler_delegate.find_session_delegate(rtc_id)
            if session_delegate is None:
                msg = f"RTC stream {rtc_id} not found."
                logger.error(msg)
                await websocket.close(4503, msg)
            await session_delegate.serve_websocket(websocket)

        @app.get(asset_route + "/{file_name}")
        async def get_asset(file_name: str):
            file_path = os.path.join(self.asset_path, file_name)
            if not os.path.isfile(file_path):
                logger.error(f"Failed to get lam asset file: {file_path}")
                return JSONResponse(status_code=404, content={"message": "File not found"})
            logger.info(f"Return lam asset file: {file_path}")
            response = FileResponse(file_path)
            return response
        
        avatar_config = {
            "avatar_type": 'lam',
            "avatar_ws_route": motion_data_route,
            "avatar_assets_path": f"{asset_route}/{self.asset_name}",
        }

        self.setup_rtc_ui(
            ui=ui,
            parent_block=parent_block,
            fastapi=app,
            avatar_config=avatar_config,
        )

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        if not isinstance(handler_config, ClientLamConfigModel):
            handler_config = ClientLamConfigModel()
        context = ClientLamContext(session_context.session_info.session_id)
        context.config = handler_config
        return context

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def on_setup_session_delegate(self, session_context: SessionContext, handler_context: HandlerContext,
                                  session_delegate: ClientSessionDelegate):
        super().on_setup_session_delegate(session_context, handler_context, session_delegate)

    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        handler_detail = self.create_handler_detail(session_context, context)
        handler_detail.inputs[ChatDataType.AVATAR_MOTION_DATA] = HandlerDataInfo(
            type=ChatDataType.AVATAR_MOTION_DATA
        )
        return handler_detail

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        super().handle(context, inputs, output_definitions)

    def destroy_context(self, context: HandlerContext):
        context = cast(ClientLamContext, context)
        client_session_delegate = cast(LamClientSessionDelegate, context.client_session_delegate)
        client_session_delegate.quit.set()
