from enum import Enum

from chat_engine.data_models.engine_channel_type import EngineChannelType


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
    # Duplex mode data types - for full-duplex conversation with interruption support
    HUMAN_DUPLEX_AUDIO = ("human_duplex_audio", EngineChannelType.AUDIO)
    HUMAN_DUPLEX_TEXT = ("human_duplex_text", EngineChannelType.TEXT)
    # Partial data types for early interrupt detection
    HUMAN_DUPLEX_AUDIO_PARTIAL = ("human_duplex_audio_partial", EngineChannelType.AUDIO)
    HUMAN_DUPLEX_TEXT_PARTIAL = ("human_duplex_text_partial", EngineChannelType.TEXT)
    # Lifecycle-only stream type for tracking client playback of avatar audio.
    # No actual data flows through this type; it only carries STREAM_BEGIN/END lifecycle.
    CLIENT_PLAYBACK = ("client_playback", EngineChannelType.EVENT)
    # Agent system data types
    PERCEPTION_CONTEXT = ("perception_context", EngineChannelType.DATA)
    ENVIRONMENT_EVENT = ("environment_event", EngineChannelType.EVENT)
