from pydantic import BaseModel, Field

from chat_engine.data_models.chat_signal_type import ChatSignalSourceType


class ChatStreamConfig(BaseModel):
    forward_cancel_signal: bool = Field(default=True)
    source_type: ChatSignalSourceType = Field(default=ChatSignalSourceType.HANDLER)
    # Whether this stream can be cancelled by interrupt.
    # Set to False for streams that should not be interrupted (e.g., client audio/video input).
    cancelable: bool = Field(default=True)
    # Whether the streamer should automatically inherit upstream input streams as
    # ancestors when creating new output streams.  Set to False for output types
    # that are logically independent of the handler's inputs (e.g., AVATAR_VIDEO
    # is a continuous render loop unrelated to per-turn AVATAR_AUDIO input, and
    # client-originated MIC_AUDIO should not inherit server-side ancestors).
    auto_link_input: bool = Field(default=True)