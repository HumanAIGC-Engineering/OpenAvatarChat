import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional, Dict

from loguru import logger

from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo
from chat_engine.contexts.session_context import SessionContext
from chat_engine.core.chat_session import ChatSession
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel, \
    EngineChannelType
from chat_engine.data_models.session_info_data import SessionInfoData, IOQueueType
from utils.directory_info import DirectoryInfo


@dataclass
class HandlerRegistry:
    base_info: Optional[HandlerBaseInfo] = field(default=None)
    handler: Optional[HandlerBase] = field(default=None)
    handler_config: Optional[HandlerBaseConfigModel] = field(default=None)


class ChatEngine(object):
    def __init__(self):
        self.inited = False
        self.engine_config: Optional[ChatEngineConfigModel] = None
        self.handler_registries: Dict[str, HandlerRegistry] = {}

        self.sessions: Dict[str, ChatSession] = {}

    def register_handler(self, handler: HandlerBase):
        base_info = handler.get_handler_info()
        self.handler_registries[base_info.name] = HandlerRegistry(
            base_info=base_info,
            handler=handler
        )
        logger.info(f"Registered handler {base_info.name}")

    def initialize(self, engine_config: ChatEngineConfigModel):
        if self.inited:
            return
        self.engine_config = engine_config
        if not os.path.isabs(engine_config.model_root):
            engine_config.model_root = os.path.join(DirectoryInfo.get_project_dir(), engine_config.model_root)

        for handler_name, registry in self.handler_registries.items():
            config_model = registry.base_info.config_model \
                if registry.base_info.config_model else HandlerBaseConfigModel
            raw_config = engine_config.handler_configs.get(handler_name, {})
            logger.info(f"Check handler registry for {handler_name} with config {raw_config}")
            registry.handler_config = config_model.model_validate(raw_config)
            if not registry.handler_config.enabled:
                logger.info(f"Handler {handler_name} is disabled by config, skipped.")
                continue
            load_start = time.monotonic()
            registry.handler.load(engine_config, registry.handler_config)
            dur_load = time.monotonic() - load_start
            logger.info(f"Handler {handler_name} loaded in {round(dur_load * 1e3)} milliseconds")
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
        for handler_name, registry in self.handler_registries.items():
            if not registry.handler_config.enabled:
                continue
            session.prepare_handler(registry.handler, registry.base_info, registry.handler_config)
        self.sessions[session_info.session_id] = session
        return session
