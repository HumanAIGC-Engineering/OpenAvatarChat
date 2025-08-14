from typing import Dict, Optional, List, Union

from pydantic import BaseModel, Field

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.common.engine_channel_type import EngineChannelType


class HandlerBaseConfigModel(BaseModel):
    enabled: bool = Field(default=True)
    module: Optional[str] = Field(default=None)
    concurrent_limit: int = Field(default=1)


class ChatEngineOutputSource(BaseModel):
    handler: Optional[Union[str, List[str]]]
    type: ChatDataType


class ChatEngineConfigModel(BaseModel):
    model_root: str = ""
    concurrent_limit: int = Field(default=1)
    handler_search_path: List[str] = Field(default_factory=list)
    handler_configs: Optional[Dict[str, Dict]] = None
    outputs: Dict[EngineChannelType, ChatEngineOutputSource] = Field(default_factory=dict)
    turn_config: Optional[Dict] = Field(default=None)
