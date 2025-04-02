import os
import uuid
from typing import Optional, Dict

from chat_engine.contexts.session_context import SessionContext
from chat_engine.core.chat_session import ChatSession
from chat_engine.core.handler_manager import HandlerManager
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, EngineChannelType
from chat_engine.data_models.session_info_data import SessionInfoData, IOQueueType
from utils.directory_info import DirectoryInfo


class ChatEngine(object):
    def __init__(self):
        self.inited = False
        self.engine_config: Optional[ChatEngineConfigModel] = None
        self.handler_manager: HandlerManager = HandlerManager()

        self.sessions: Dict[str, ChatSession] = {}

    def initialize(self, engine_config: ChatEngineConfigModel):
        if self.inited:
            return
        self.engine_config = engine_config
        if not os.path.isabs(engine_config.model_root):
            engine_config.model_root = os.path.join(DirectoryInfo.get_project_dir(), engine_config.model_root)
        self.handler_manager.initialize(engine_config)
        self.handler_manager.load_handlers(engine_config)
        self.inited = True

    def create_session(self, session_info: SessionInfoData,
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
            session.prepare_handler(registry.handler, registry.base_info, registry.handler_config)
        self.sessions[session_info.session_id] = session
        return session
