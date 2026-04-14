from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union, Dict, List

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel
from chat_engine.data_models.chat_signal import SignalFilterRule
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.data_models.runtime_data.data_bundle import DataBundleDefinition


class ChatDataConsumeMode(Enum):
    ONCE = -1
    DEFAULT = 0


@dataclass
class HandlerBaseInfo:
    name: Optional[str] = None
    config_model: Optional[type[HandlerBaseConfigModel]] = None
    client_session_delegate_class: Optional[type] = None
    # Handler load priority, the smaller, the higher
    load_priority: int = 0


@dataclass
class HandlerDataInfo:
    data_name: Optional[str] = None
    type: ChatDataType = ChatDataType.NONE
    definition: Optional[DataBundleDefinition] = None
    input_priority: int = 0
    input_consume_mode: ChatDataConsumeMode = ChatDataConsumeMode.DEFAULT
    output_stream_config: Optional[ChatStreamConfig] = None

    def __lt__(self, other):
        if self.input_priority == other.input_priority:
            return self.type.value < other.type.value
        return self.input_priority < other.input_priority


@dataclass
class HandlerDetail:
    inputs: Union[Dict[ChatDataType, HandlerDataInfo], List[HandlerDataInfo]] = field(default_factory=dict)
    outputs: Union[Dict[ChatDataType, HandlerDataInfo], List[HandlerDataInfo]] = field(default_factory=dict)
    signal_filters: List[SignalFilterRule] = field(default_factory=list)

    @classmethod
    def _validate_data_info_list(cls, list_data: List[HandlerDataInfo]):
        result = {}
        for info in list_data:
            if info.type in result:
                raise ValueError(f"Duplicate data type: {info.type}")
            result[info.type] = info
        return result

    def validate(self):
        if isinstance(self.inputs, List):
            self.inputs = self._validate_data_info_list(self.inputs)
        if isinstance(self.outputs, List):
            self.outputs = self._validate_data_info_list(self.outputs)
