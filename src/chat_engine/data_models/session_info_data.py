import asyncio
import queue
from typing import Union

from pydantic import BaseModel, Field

IOQueueType = Union[queue.Queue, asyncio.Queue]

class SessionInfoData(BaseModel):
    session_id: str
    timestamp_base: int = Field(default=16000)
