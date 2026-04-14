from enum import Enum


class ChatStreamStatus(str, Enum):
    NOT_STARTED = "not_started"
    STARTED = "started"
    ENDED = "ended"
    CANCELLED = "cancelled"
