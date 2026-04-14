from typing import Optional, Dict

import numpy as np
from pydantic import BaseModel, Field

from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel
from chat_engine.core.stream_manager import StreamManager


class DataToolConfig(HandlerBaseConfigModel, BaseModel):
    """
    Configuration for the data tool handler.
    """

    buffer_limit: int = Field(default=200, description="Max records kept per session")
    preview_bytes: int = Field(default=4096, description="Binary preview size for ndarray data")
    preview_chars: int = Field(default=512, description="Preview size for text payload")
    include_binary_preview: bool = Field(
        default=False, description="Whether to include base64 preview for ndarray data"
    )


class DataToolContext(HandlerContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[DataToolConfig] = None
        self.audio_buffers: Dict[str, list[np.ndarray]] = {}
        self.video_buffers: Dict[str, list[np.ndarray]] = {}
        # Stream manager is set only for manager handlers in ChatSession.
        self.stream_manager: Optional[StreamManager] = None
        # Registered interrupt callback for cleanup.
        self.interrupt_handler = None
        # Throttle MIC_AUDIO publishing
        self.last_mic_audio_push_ts: float = 0.0

