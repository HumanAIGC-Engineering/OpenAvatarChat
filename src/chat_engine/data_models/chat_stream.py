from dataclasses import dataclass, field
from typing import Optional, NamedTuple

from chat_engine.data_models.chat_data_type import ChatDataType


class StreamKey(NamedTuple):
    """Stream key identifying a stream uniquely by builder_id and stream_id"""
    builder_id: int
    stream_id: int
    
    def __str__(self) -> str:
        """String representation: stream_{builder_id}_{stream_id}"""
        return f"stream_{self.builder_id}_{self.stream_id}"


@dataclass
class ChatStreamIdentity:
    data_type: ChatDataType
    builder_id: int = -1
    stream_id: int = -1
    name: Optional[str] = field(default=None)
    producer_name: Optional[str] = field(default=None)

    @property
    def key(self):
        if self.builder_id < 0 or self.stream_id < 0:
            return None
        return StreamKey(self.builder_id, self.stream_id)
    
    @property
    def stream_key_str(self) -> Optional[str]:
        """Get string representation of stream_key, returns None if key is None"""
        key = self.key
        if key is None:
            return None
        return str(key)