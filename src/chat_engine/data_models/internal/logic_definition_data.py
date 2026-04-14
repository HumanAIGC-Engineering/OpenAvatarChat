from dataclasses import dataclass, field
from typing import Optional, List, Union, Dict

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import LogicBaseConfigModel
from chat_engine.data_models.chat_signal import SignalFilterRule
from chat_engine.data_models.internal.handler_definition_data import HandlerDataInfo


@dataclass
class LogicBaseInfo:
    name: Optional[str] = None
    config_model: type[LogicBaseConfigModel] = LogicBaseConfigModel
    load_priority: int = 0


@dataclass
class LogicDetail:
    inspected_streamers: List = field(default_factory=list)
    inspected_signals: List[SignalFilterRule] = field(default_factory=list)
    outputs: Union[Dict[ChatDataType, HandlerDataInfo], List[HandlerDataInfo]] = field(default_factory=dict)

    @classmethod
    def _validate_data_info_list(cls, list_data: List[HandlerDataInfo]):
        result = {}
        for info in list_data:
            if info.type in result:
                raise ValueError(f"Duplicate data type: {info.type}")
            result[info.type] = info
        return result

    def validate(self):
        if isinstance(self.outputs, List):
            self.outputs = self._validate_data_info_list(self.outputs)
