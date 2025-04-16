import os
import uuid
from typing import Optional, Dict

from loguru import logger

from chat_engine.common.client_handler_base import ClientHandlerBase
from chat_engine.contexts.session_context import SessionContext
from chat_engine.core.chat_session import ChatSession
from chat_engine.core.handler_manager import HandlerManager
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, EngineChannelType
from chat_engine.data_models.session_info_data import SessionInfoData, IOQueueType
from engine_utils.directory_info import DirectoryInfo
from dotenv import load_dotenv


class ChatEngine(object):
    def __init__(self):
        self.inited = False
        self.engine_config: Optional[ChatEngineConfigModel] = None
        self.handler_manager: HandlerManager = HandlerManager(self)

        self.sessions: Dict[str, ChatSession] = {}

    def initialize(self, engine_config: ChatEngineConfigModel, app=None, ui=None, parent_block=None):
        if self.inited:
            return

        load_dotenv()

        self.engine_config = engine_config
        if not os.path.isabs(engine_config.model_root):
            engine_config.model_root = os.path.join(DirectoryInfo.get_project_dir(), engine_config.model_root)
        self.handler_manager.initialize(engine_config)
        self.handler_manager.load_handlers(engine_config, app, ui, parent_block)
        self.inited = True

    def _create_session(self, session_info: SessionInfoData,
                        input_queues: Dict[EngineChannelType, IOQueueType],
                        output_queues: Dict[EngineChannelType, IOQueueType]):
        if not session_info.session_id:
            session_info.session_id = str(uuid.uuid4())
        if session_info.session_id in self.sessions:
            raise RuntimeError(f"session {session_info.session_id} already exists")

        session_context = SessionContext(session_info=session_info,
                                         input_queues=input_queues,
                                         output_queues=output_queues)

        session = ChatSession(session_context, self.engine_config)
        handlers = self.handler_manager.get_enabled_handler_registries()
        for registry in handlers:
            if isinstance(registry.handler, ClientHandlerBase):
                # client create_context and data_sink creation of handler is not called here,
                # they are created by its internal logic after every other handlers are ready.
                continue
            session.prepare_handler(registry.handler, registry.base_info, registry.handler_config)
        self.sessions[session_info.session_id] = session
        return session

    def create_client_session(self, session_info: SessionInfoData, client_handler: ClientHandlerBase):
        # TODO currently multi client in one session is not allowed.
        if session_info.session_id in self.sessions:
            msg = f"Session {session_info.session_id} already exists."
            raise RuntimeError(msg)

        session = self._create_session(session_info, {}, {})

        registry = self.handler_manager.find_client_handler(client_handler)
        if registry is None:
            raise RuntimeError(f"client handler {client_handler} not found")

        handler_env = session.prepare_handler(client_handler, registry.base_info, registry.handler_config)
        return session, handler_env

    def stop_session(self, session_id: str):
        session = self.sessions.pop(session_id)
        if session is None:
            logger.error(f"Session {session_id} is not found.")
            return
        session.stop()
