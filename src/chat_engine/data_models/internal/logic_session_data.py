from dataclasses import dataclass
from typing import Optional

from chat_engine.common.logic_base import LogicBase
from chat_engine.contexts.logic_context import LogicContext
from chat_engine.data_models.chat_engine_config_data import LogicBaseConfigModel
from chat_engine.data_models.internal.logic_definition_data import LogicBaseInfo


@dataclass
class LogicEnv:
    logic_info: LogicBaseInfo
    logic: LogicBase
    config: LogicBaseConfigModel
    context: Optional[LogicContext] = None


@dataclass
class LogicRecord:
    env: LogicEnv

