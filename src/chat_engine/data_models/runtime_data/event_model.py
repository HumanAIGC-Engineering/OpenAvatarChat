from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    EVT_START_AVATAR_SPEAKING = "start_avatar_speaking"
    EVT_END_AVATAR_SPEAKING = "end_avatar_speaking"
    EVT_START_HUMAN_SPEAKING = "start_human_speaking"
    EVT_END_HUMAN_SPEAKING = "end_human_speaking"
    EVT_HUMAN_TEXT = "human_speech_text"
    EVT_HUMAN_TEXT_END = "human_speech_text_end"
    EVT_AVATAR_TEXT = "avatar_speech_text"
    EVT_AVATAR_TEXT_END = "avatar_speech_text_end"
    EVT_SESSION_START = "session_start"
    EVT_SESSION_STOP = "session_stop"
    EVT_INTERRUPT_SPEECH = "interrupt_speech"
    EVT_SERVER_ERROR = "server_error"


class EventEmbeddingDataType(str, Enum):
    NOT_SET = "not_set"
    TEXT = "text"
    JSON = "json"
    BASE64 = "base64"


class EventData(BaseModel):
    event_type: Optional[EventType] = Field(default=None)
    event_subtype: Optional[str] = Field(default=None)
    event_data_type: Optional[EventEmbeddingDataType] = Field(default=None)
    event_data: Optional[str] = Field(default=None)
    # None means instant event, -1 means event time need to be determined by receiver
    event_time: Optional[int] = Field(default=None)
    event_time_unit: Optional[int] = Field(default=None)

    def is_valid(self):
        return self.event_type is not None
