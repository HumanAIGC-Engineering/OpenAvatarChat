from typing import Optional, List
from loguru import logger

from chat_engine.common.logic_base import LogicBase, LogicDetail, LogicBaseInfo
from chat_engine.contexts.logic_context import LogicContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.core.stream_manager import ChatStreamer
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_engine_config_data import LogicBaseConfigModel


class LatencyProfileContext(LogicContext):
    def __init__(self, session_id: str):
        super().__init__(session_id)


class LatencyProfileLogic(LogicBase):
    def __init__(self):
        super().__init__()

    def get_logic_info(self) -> LogicBaseInfo:
        return LogicBaseInfo()

    def create_context(self, session_context: SessionContext,
                       logic_config: Optional[LogicBaseConfigModel] = None) -> LogicContext:
        return LatencyProfileContext(session_context.session_info.session_id)

    def get_logic_detail(self, session_context: SessionContext, context: LogicContext) -> LogicDetail:
        return LogicDetail()

    def on_chat_data_distribute(self, context: LogicContext, streamer: ChatStreamer, chat_data: ChatData,
                     targets: List):
        logger.info(f"Got chat data {chat_data.type} from streamer {streamer.producer_name} to {targets}")
        pass

    def destroy_context(self, context: LogicContext):
        pass
