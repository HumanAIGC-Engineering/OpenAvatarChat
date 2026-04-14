import typing

from typing import List, Optional, Callable

from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_stream import ChatStreamIdentity
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.data_models.internal.chat_data_endpoints import DataSink

if typing.TYPE_CHECKING:
    from chat_engine.core.stream_manager import ChatStream, ChatStreamer


class StreamFilter:
    def __init__(self):
        self.new_stream_callback: Optional[
            Callable[[ChatStreamer, ChatStreamConfig, ChatStreamIdentity, Optional[List[ChatStreamIdentity]]], bool]
        ] = None
        self.distribute_callback: Optional[Callable[[ChatStreamer, ChatData, List[DataSink]], bool]] = None
        self.finish_stream_callback: Optional[Callable[[ChatStream], bool]] = None
        self.cancel_stream_callback: Optional[Callable[[ChatStream], bool]] = None

    def new_stream(self, streamer: ChatStreamer, config: ChatStreamConfig, new_stream_id: ChatStreamIdentity,
                   source_streams: Optional[List[ChatStreamIdentity]]):
        if self.new_stream_callback:
            return self.new_stream_callback(streamer, config, new_stream_id, source_streams)
        return True

    def distribute(self, streamer: ChatStreamer, chat_data: ChatData, targets: List[DataSink]):
        if self.distribute_callback:
            return self.distribute_callback(streamer, chat_data, targets)
        return True

    def finish_stream(self, stream: ChatStream):
        if self.finish_stream_callback:
            return self.finish_stream_callback(stream)
        return True

    def cancel_stream(self, stream: ChatStream):
        if self.cancel_stream_callback:
            return self.cancel_stream_callback(stream)
        return True
