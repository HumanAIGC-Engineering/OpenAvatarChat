from enum import Enum


class ChatSignalType(str, Enum):
    # START = "start"
    BEGIN = "begin"
    END = "end"
    # CANCEL = "cancel"
    INTERRUPT = "interrupt"
    # RESET = "reset"
    # ERROR = "error"
    # STOP = "stop"


class ChatSignalSourceType(str, Enum):
    CLIENT = "client"
    # LOGIC = "logic"
    # HANDLER = "handler"
    # ENGINE = "engine"
