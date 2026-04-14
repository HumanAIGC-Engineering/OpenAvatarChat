import time
import weakref
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.internal.handler_definition_data import HandlerBaseInfo, HandlerDetail, HandlerDataInfo, ChatDataConsumeMode


class HandlerBase(ABC):
    def __init__(self):
        self.engine: Optional[weakref.ReferenceType] = None
        self.handler_root: Optional[str] = None

    def on_before_register(self):
        pass

    @abstractmethod
    def get_handler_info(self) -> HandlerBaseInfo:
        pass

    @abstractmethod
    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        pass

    @abstractmethod
    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        pass

    def warmup_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    @abstractmethod
    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    @abstractmethod
    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        pass

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        pass

    @abstractmethod
    def handle(self, context: HandlerContext, inputs: ChatData,
                     output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        pass

    @abstractmethod
    def destroy_context(self, context: HandlerContext):
        pass

    def destroy(self):
        pass

    # === History recording methods (can be overridden by subclasses) ===

    def on_history_record(
        self,
        context: HandlerContext,
        signal_type: ChatSignalType,
        data_type: ChatDataType,
        data: Any = None,
        related_event_id: Optional[str] = None,
        source_stream_key: Optional[str] = None,
    ) -> Optional[str]:
        """
        Default history recording handler. Override in subclasses to customize.
        
        This method is called automatically by the engine for stream lifecycle events
        when should_auto_record_history() returns True for the data type.
        
        Args:
            context: Handler context
            signal_type: Signal type (STREAM_BEGIN, STREAM_END, etc.)
            data_type: Data type (HUMAN_TEXT, AVATAR_AUDIO, etc.)
            data: Data to record (text content, metadata, etc.)
            related_event_id: Related event ID (e.g., STREAM_END -> STREAM_BEGIN)
            source_stream_key: Stream key snapshot (format: "stream_{builder_id}_{stream_id}")
            
        Returns:
            Created event ID, or None if not recorded
        """
        if context.session_history is None:
            return None
        
        return context.session_history.create_and_add_event(
            data_type=data_type,
            signal_type=signal_type,
            data=data,
            owner=context.owner,
            parent_event_id=related_event_id,
            source_stream_key=source_stream_key,
        )

    def should_auto_record_history(self, data_type: ChatDataType) -> bool:
        """
        Determine if history should be automatically recorded for this data type.
        
        Override in subclasses to disable auto-recording for specific types.
        
        Args:
            data_type: The data type to check
            
        Returns:
            True if auto-recording should be enabled, False otherwise
        """
        # Default: auto-record for TEXT types (dialog content) and HUMAN_DUPLEX_AUDIO (for user speech timing)
        # Note: AVATAR_AUDIO playback is tracked via CLIENT_PLAYBACK lifecycle streams (auto-recorded by engine)
        return data_type in (
            ChatDataType.HUMAN_TEXT,
            ChatDataType.AVATAR_TEXT,
            ChatDataType.HUMAN_DUPLEX_TEXT,
            ChatDataType.HUMAN_DUPLEX_AUDIO, # Required for user speech start time detection
        )
