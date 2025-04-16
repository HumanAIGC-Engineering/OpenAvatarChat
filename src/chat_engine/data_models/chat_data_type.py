from enum import Enum

from chat_engine.common.engine_channel_type import EngineChannelType


class ChatDataType(Enum):

    def __init__(self, value: str, channel_type: EngineChannelType):
        self._value_ = value
        self.channel_type = channel_type

    NONE = ("none", EngineChannelType.NONE)
    HUMAN_TEXT = ("human_text", EngineChannelType.TEXT)
    AVATAR_TEXT = ("avatar_text", EngineChannelType.TEXT)
    HUMAN_VOICE_ACTIVITY = ("human_vad", EngineChannelType.EVENT)
    MIC_AUDIO = ("mic_audio", EngineChannelType.AUDIO)
    HUMAN_AUDIO = ("human_audio", EngineChannelType.AUDIO)
    AVATAR_AUDIO = ("avatar_audio", EngineChannelType.AUDIO)
    CAMERA_VIDEO = ("camera_video", EngineChannelType.VIDEO)
    AVATAR_VIDEO = ("avatar_video", EngineChannelType.VIDEO)
    AVATAR_MOTION_DATA = ("avatar_motion_data", EngineChannelType.MOTION_DATA)
