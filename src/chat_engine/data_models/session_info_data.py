import asyncio
import queue
from typing import Union

from pydantic import BaseModel

IOQueueType = Union[queue.Queue, asyncio.Queue]

class SessionInfoData(BaseModel):
    session_id: str
