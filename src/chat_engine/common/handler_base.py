from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict

from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition


@dataclass
class HandlerBaseInfo:
    name: str
    config_model: Optional[type[HandlerBaseConfigModel]] = None


@dataclass
class HandlerDataInfo:
    type: ChatDataType = ChatDataType.NONE
    definition: Optional[DataBundleDefinition] = None


@dataclass
class HandlerDetail:
    inputs: Dict[ChatDataType, HandlerDataInfo] = field(default_factory=dict)
    outputs: Dict[ChatDataType, HandlerDataInfo] = field(default_factory=dict)


class HandlerBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_handler_info(self) -> HandlerBaseInfo:
        pass

    @abstractmethod
    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        pass

    @abstractmethod
    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        pass

    @abstractmethod
    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        pass

    @abstractmethod
    def handle(self, context: HandlerContext, inputs: ChatData,
                     output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        pass

    @abstractmethod
    def destroy_context(self, context: HandlerContext):
        pass
