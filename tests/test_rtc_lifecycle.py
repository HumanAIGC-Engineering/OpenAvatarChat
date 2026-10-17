import asyncio
from types import SimpleNamespace as NS


def test_actual_rtc_cancel_clears_media_queues():
    from handlers.client.rtc_client.client_handler_rtc import (
        ClientHandlerRtc,
        RtcClientSessionDelegate,
    )
    from chat_engine.data_models.chat_signal import ChatSignal
    from chat_engine.data_models.chat_signal_type import ChatSignalType, ChatSignalSourceType
    from chat_engine.data_models.chat_data_type import ChatDataType
    from chat_engine.data_models.engine_channel_type import EngineChannelType

    delegate = RtcClientSessionDelegate()
    for queue in delegate.output_queues.values():
        queue.put_nowait("stale")
    handler = ClientHandlerRtc()
    handler._send_message_to_chat_channel = lambda *args: True
    stream = NS(data_type=ChatDataType.CLIENT_PLAYBACK, producer_name="FlashHead", stream_key_str="playback")
    signal = NS(
        type=ChatSignalType.STREAM_CANCEL,
        related_stream=stream,
        source_type=ChatSignalSourceType.HANDLER,
        signal_data=None,
    )
    context = NS(client_session_delegate=delegate, session_id="test", stream_manager=NS(find_stream=lambda _: None))
    handler.on_signal(context, signal)
    assert all(queue.empty() for queue in delegate.output_queues.values())


def test_scheduled_send_survives_channel_close():
    from handlers.client.rtc_client.client_handler_rtc import ClientHandlerRtc
    from handlers.client.ws_client.ws_message_protocol import BaseMessage, MessageHeader, MessageType

    async def run():
        loop = asyncio.get_running_loop()
        errors = []
        loop.set_exception_handler(lambda _, event: errors.append(event))
        channel = NS(readyState="open", send=lambda _: (_ for _ in ()).throw(RuntimeError("closed")))
        stream = NS(chat_channel=channel, chat_channel_loop=loop)
        handler = ClientHandlerRtc()
        handler._get_chat_channel = lambda _: stream
        message = BaseMessage(header=MessageHeader(name=MessageType.CHAT_SIGNAL, request_id="test"))
        assert handler._send_message_to_chat_channel("test", message)
        channel.readyState = "closed"
        await asyncio.sleep(0.01)
        assert not errors
        channel.readyState = "open"
        assert handler._send_message_to_chat_channel("test", message)
        await asyncio.sleep(0.01)
        assert not errors

    asyncio.run(run())
