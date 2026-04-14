from collections import namedtuple
from typing import Optional, Dict

from pydantic import BaseModel, Field

from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
from chat_engine.data_models.chat_stream import ChatStreamIdentity


SignalFilterRule = namedtuple("SignalFilter",
                              ["signal_type", "source_type", "stream_type"],
                              defaults=[None, None, None])


class ChatSignal(BaseModel):
    type: Optional[ChatSignalType] = Field(default=None)
    source_type: Optional[ChatSignalSourceType] = Field(default=None)
    related_stream: Optional[ChatStreamIdentity] = Field(default=None)
    signal_data: Optional[Dict] = Field(default=None)
    source_name: Optional[str] = Field(default=None)

    @property
    def is_candidate(self) -> bool:
        """
        判断信号是否为候选信号（建议性信号）。
        如果信号来源不是 stream 的 owner，则为候选信号。
        Stream owner 可以选择是否遵从候选信号。
        """
        if self.related_stream is None or self.source_name is None:
            return True  # 无法确定归属，视为候选
        return self.source_name != self.related_stream.producer_name
