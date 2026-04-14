"""
Interrupt Handler

A dedicated handler for processing INTERRUPT signals and performing stream cancellation.
Decouples the "when to interrupt" decision (made by SemanticTurnDetector, client, etc.)
from the "how to cancel streams" execution (performed here).

Responsibilities:
- Listen for INTERRUPT signals from any source (CLIENT, HANDLER, etc.)
- Cancel the appropriate stream chains via StreamManager
- Record interrupt events in session history
"""
from typing import Optional, Dict, cast

from loguru import logger

from chat_engine.common.handler_base import HandlerBase, HandlerDataInfo, HandlerDetail, HandlerBaseInfo
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel


class InterruptHandlerConfig(HandlerBaseConfigModel):
    """Configuration for Interrupt Handler"""
    pass


class InterruptHandler(HandlerBase):
    """
    Interrupt Handler - centralized stream cancellation on INTERRUPT signals.

    Listens for INTERRUPT signals from any source and cancels the relevant
    stream chains. This decouples interrupt decision-making (in other handlers)
    from stream lifecycle management.

    Signal semantics:
    - related_stream set → targeted cancel via cancel_stream_chain
    - related_stream absent → broad cancel via cancel_streams_by_type(CLIENT_PLAYBACK)
    """

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="InterruptHandler",
            config_model=InterruptHandlerConfig
        )

    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[HandlerBaseConfigModel] = None):
        pass

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        return HandlerContext(session_context.session_info.session_id)

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        pass

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        signal_filters = [
            # Listen for INTERRUPT from any source (HANDLER, CLIENT, etc.)
            SignalFilterRule(ChatSignalType.INTERRUPT, None, None),
        ]

        return HandlerDetail(
            inputs=[],
            outputs=[],
            signal_filters=signal_filters
        )

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        pass

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        """Handle INTERRUPT signals by cancelling the appropriate streams."""
        if signal.type != ChatSignalType.INTERRUPT:
            return

        logger.info(
            f"InterruptHandler: Received INTERRUPT signal, "
            f"source_type={signal.source_type}, source_name={signal.source_name}, "
            f"related_stream={signal.related_stream}"
        )

        target_stream = signal.related_stream

        # If no related_stream specified, try to find active playback streams
        if target_stream is None and context.stream_manager:
            active_playback = [
                s for s in context.stream_manager.get_active_streams()
                if s.identity.data_type == ChatDataType.CLIENT_PLAYBACK
            ]
            if len(active_playback) == 1:
                target_stream = active_playback[0].identity
            elif len(active_playback) == 0:
                logger.debug("InterruptHandler: No active playback streams to cancel")
                return

        # Cancel streams via StreamManager
        cancelled = []
        if context.stream_manager:
            if target_stream:
                cancelled = context.stream_manager.cancel_stream_chain(target_stream)
                logger.info(
                    f"InterruptHandler: cancel_stream_chain({target_stream.stream_key_str}) "
                    f"cancelled {len(cancelled)} streams"
                )
            else:
                cancelled = context.stream_manager.cancel_streams_by_type(ChatDataType.CLIENT_PLAYBACK)
                logger.info(
                    f"InterruptHandler: cancel_streams_by_type cancelled {len(cancelled)} streams"
                )

        # Record interrupt event in history
        if context.session_history is not None:
            signal_data = signal.signal_data or {}
            context.session_history.create_and_add_event(
                signal_type=ChatSignalType.INTERRUPT,
                data={
                    "reason": signal_data.get("reason", "interrupt"),
                    "trigger_text": signal_data.get("trigger_text", ""),
                    "cancelled_count": len(cancelled),
                    "source_type": signal.source_type.value if signal.source_type else None,
                    "source_name": signal.source_name,
                },
                owner=context.owner,
            )

    def destroy_context(self, context: HandlerContext):
        pass


# Export the handler class
handler_class = InterruptHandler
