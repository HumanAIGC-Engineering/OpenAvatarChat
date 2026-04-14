import weakref
from abc import ABC, abstractmethod
from typing import Optional, List

from chat_engine.contexts.logic_context import LogicContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.core.stream_manager import ChatStreamer
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import LogicBaseConfigModel, ChatEngineConfigModel
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.internal.handler_session_data import HandlerRegistry
from chat_engine.data_models.internal.logic_definition_data import LogicBaseInfo, LogicDetail


class LogicBase(ABC):
    def __init__(self):
        self.engine: Optional[weakref.ReferenceType] = None
        self.logic_root: Optional[str] = None

    def on_before_register(self):
        pass

    @abstractmethod
    def get_logic_info(self) -> LogicBaseInfo:
        pass

    def load(self, engine_config: ChatEngineConfigModel, logic_config: Optional[LogicBaseConfigModel] = None):
        pass

    @abstractmethod
    def create_context(self, handler_registries: List[HandlerRegistry], session_context: SessionContext,
                       logic_config: Optional[LogicBaseConfigModel] = None) -> LogicContext:
        pass

    @abstractmethod
    def get_logic_detail(self, session_context: SessionContext,
                         context: LogicContext) -> LogicDetail:
        pass

    def warmup_context(self, session_context: SessionContext, logic_context: LogicContext):
        pass

    def start_context(self, session_context: SessionContext, logic_context: LogicContext):
        pass

    def on_signal_distribute(self, context: LogicContext, signal: ChatSignal, targets: List):
        pass

    def on_chat_data_distribute(self, context: LogicContext, streamer: ChatStreamer, chat_data: ChatData,
                     targets: List):
        pass

    @abstractmethod
    def destroy_context(self, context: LogicContext):
        pass

    def destroy(self):
        pass
