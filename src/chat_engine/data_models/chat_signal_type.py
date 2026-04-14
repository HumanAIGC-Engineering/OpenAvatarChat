from enum import Enum


class ChatSignalType(str, Enum):
    SESSION_START = "session_start"
    STREAM_BEGIN = "stream_begin"
    STREAM_END = "stream_end"
    STREAM_CANCEL = "stream_cancel"
    INTERRUPT = "interrupt"
    ERROR = "error"
    SESSION_STOP = "session_stop"
    # Semantic turn detection signals
    SEMANTIC_WAIT = "semantic_wait"  # Utterance incomplete, request extended wait
    # Agent system signal
    ENVIRONMENT_EVENT = "environment_event"


class ChatSignalSourceType(str, Enum):
    CLIENT = "client"
    LOGIC = "logic"
    HANDLER = "handler"
    # ENGINE = "engine"
