import queue
from dataclasses import dataclass
from typing import List, Optional

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.session_info_data import IOQueueType
from chat_engine.data_models.internal.handler_definition_data import HandlerDataInfo


@dataclass
class DataSource:
    owner: str = ""
    source_queue: IOQueueType = None
    target_types: List[ChatDataType] = None


@dataclass
class DataSink:
    owner: str = ""
    sink_queue: queue.Queue = None
    consume_info: Optional[HandlerDataInfo] = None
