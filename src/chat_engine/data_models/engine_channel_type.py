from enum import Enum


class EngineChannelType(str, Enum):
    NONE = "none"
    TEXT = "text"
    AUDIO = "audio"
    VIDEO = "video"
    EVENT = "event"
    MOTION_DATA = "motion_data"
    DATA = "data"  # 用于 Agent 间传递的结构化数据