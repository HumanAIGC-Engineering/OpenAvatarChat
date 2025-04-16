from dataclasses import dataclass
from typing import Tuple, Optional

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.runtime_data.data_bundle import DataBundle


@dataclass
class ChatData:
    source: Optional[str] = None
    type: ChatDataType = ChatDataType.NONE
    timestamp: Tuple[int, int] = (0, 0)
    data: Optional[DataBundle] = None

    def is_timestamp_valid(self) -> bool:
        return self.timestamp[0] >= 0 and self.timestamp[1] > 0
