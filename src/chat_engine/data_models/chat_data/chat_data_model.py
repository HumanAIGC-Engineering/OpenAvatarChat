from dataclasses import dataclass
from typing import Tuple, Optional, Union

import numpy as np

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_stream import ChatStreamIdentity
from chat_engine.data_models.runtime_data.data_bundle import DataBundle


@dataclass
class ChatData:
    stream_id: Optional[ChatStreamIdentity] = None
    source: Optional[str] = None
    type: ChatDataType = ChatDataType.NONE
    timestamp: Tuple[int, int] = (0, 0)
    data: Optional[DataBundle] = None
    is_first_data: bool = False
    is_last_data: bool = False

    def is_timestamp_valid(self) -> bool:
        return self.timestamp[0] >= 0 and self.timestamp[1] > 0


StreamableData = Union[
    ChatData,
    DataBundle,
    np.ndarray,
]
