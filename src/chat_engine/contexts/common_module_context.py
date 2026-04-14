from typing import Optional, TYPE_CHECKING
from loguru import logger

from chat_engine.data_models.chat_data.chat_data_model import StreamableData
from chat_engine.data_models.chat_signal import ChatSignal

if TYPE_CHECKING:
    from chat_engine.core.signal_manager import SignalEmitter
    from chat_engine.core.stream_manager import ChatDataSubmitter, StreamManager
    from chat_engine.contexts.session_history import SessionHistory


class CommonModuleContext(object):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.owner: Optional[str] = None
        self.signal_emitter: Optional["SignalEmitter"] = None
        self.data_submitter: Optional["ChatDataSubmitter"] = None
        self.session_history: Optional["SessionHistory"] = None
        self.stream_manager: Optional["StreamManager"] = None

    def submit_data(self, data: StreamableData, finish_stream: Optional[bool] = None):
        if self.data_submitter is None:
            logger.error("Session is not started, data submitter not ready.")
            return
        self.data_submitter.submit(data, finish_stream=finish_stream)

    def emit_signal(self, signal: ChatSignal):
        if self.signal_emitter is None:
            logger.error("Session is not started, signal emitter not ready.")
            return
        self.signal_emitter.emit(signal)
