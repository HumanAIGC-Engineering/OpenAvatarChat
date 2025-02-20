from typing import Dict, Optional

from pydantic import BaseModel, Field

from chat_engine.common.chat_data_type import ChatDataType
from chat_engine.common.engine_channel_type import EngineChannelType


class HandlerBaseConfigModel(BaseModel):
    enabled: bool = Field(default=True)


class ChatEngineOutputSource(BaseModel):
    handler: str
    type: ChatDataType


class ChatEngineConfigModel(BaseModel):
    model_root: str = ""
    handler_configs: Optional[Dict[str, Dict]] = None
    outputs: Dict[EngineChannelType, ChatEngineOutputSource] = Field(default_factory=dict)
