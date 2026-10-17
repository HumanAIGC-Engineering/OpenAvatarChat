import asyncio
import threading
from types import SimpleNamespace as NS

import pytest

from handlers.client.rtc_client.thread_safe_queue import ThreadSafeAsyncQueue


def test_concurrent_producers_preserve_each_producers_order():
    q = ThreadSafeAsyncQueue()
    threads = [
        threading.Thread(target=lambda key=key: [q.put_nowait((key, i)) for i in range(500)]) for key in range(4)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(3)
        assert not thread.is_alive()
    rows = [q.get_nowait() for _ in range(2000)]
    assert len(set(rows)) == 2000
    for key in range(4):
        assert [i for k, i in rows if k == key] == list(range(500))


def test_clear_cannot_reinsert_old_payloads_from_delayed_wakeup():
    async def run():
        asyncio.get_running_loop().set_debug(True)
        q = ThreadSafeAsyncQueue()
        pending = asyncio.create_task(q.get())
        await asyncio.sleep(0)
        producer = threading.Thread(target=lambda: (q.put_nowait("old"), q.clear(), q.clear()))
        producer.start()
        producer.join(1)
        await asyncio.sleep(0.01)
        assert q.empty() and not pending.done()
        q.put_nowait("new")
        assert await asyncio.wait_for(pending, 1) == "new"

    asyncio.run(run())


def test_cancelled_reader_does_not_lose_next_item():
    async def run():
        q = ThreadSafeAsyncQueue()
        pending = asyncio.create_task(q.get())
        await asyncio.sleep(0)
        pending.cancel()
        with pytest.raises(asyncio.CancelledError):
            await pending
        q.put_nowait("next")
        assert await q.get() == "next"

    asyncio.run(run())


def test_close_wakes_all_pending_readers_and_drops_late_frames():
    async def run():
        q = ThreadSafeAsyncQueue()
        tasks = [asyncio.create_task(q.get()) for _ in range(8)]
        await asyncio.sleep(0)
        closer = threading.Thread(target=lambda: (q.close(), q.close(), q.put_nowait("late")))
        closer.start()
        closer.join(1)
        results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
        assert all(isinstance(result, asyncio.CancelledError) for result in results)
        assert q.empty()

    asyncio.run(run())


def test_queue_rejects_a_different_event_loop():
    q = ThreadSafeAsyncQueue()
    q.put_nowait(1)
    assert asyncio.run(q.get()) == 1
    with pytest.raises(RuntimeError, match="different event loop"):
        asyncio.run(q.get())
    q.close()
    q.put_nowait("late")
    assert q.empty()


@pytest.mark.parametrize("owns_session", [False, True])
def test_disconnect_releases_only_owned_session_and_is_idempotent(owns_session):
    from handlers.client.rtc_client.client_handler_rtc import RtcClientSessionDelegate
    from chat_engine.data_models.engine_channel_type import EngineChannelType
    from service.rtc_service.rtc_stream import RtcStream

    async def run():
        stopped = []
        stream = object.__new__(RtcStream)
        stream.quit = asyncio.Event()
        stream.client_session_delegate = delegate = RtcClientSessionDelegate()
        stream.owns_session = owns_session
        stream.session_id = "test"
        stream.chat_channel = NS()
        stream.chat_channel_loop = asyncio.get_running_loop()
        factory = NS(streams={"test": stream}, client_handler_delegate=NS(stop_session=lambda key: stopped.append(key)))
        stream.weak_factory = lambda: factory
        pending = asyncio.create_task(delegate.get_data(EngineChannelType.AUDIO, timeout=None))
        await asyncio.sleep(0)
        stream.shutdown()
        stream.shutdown()
        assert stream.quit.is_set()
        assert stream.chat_channel is None and stream.client_session_delegate is None
        assert not factory.streams
        if owns_session:
            with pytest.raises(asyncio.CancelledError):
                await asyncio.wait_for(pending, 1)
            assert stopped == ["test"]
            for queue in delegate.output_queues.values():
                queue.put_nowait("late")
                assert queue.empty()
        else:
            assert stopped == []
            delegate.output_queues[EngineChannelType.AUDIO].put_nowait("shared")
            assert await asyncio.wait_for(pending, 1) == "shared"

    asyncio.run(run())


def test_repeated_cancel_is_safe():
    from handlers.client.rtc_client.client_handler_rtc import RtcClientSessionDelegate

    delegate = RtcClientSessionDelegate()
    for _ in range(20):
        for q in delegate.output_queues.values():
            q.put_nowait("old")
        delegate.clear_data()
        delegate.clear_data()
        assert all(q.empty() for q in delegate.output_queues.values())


def test_shutdown_does_not_remove_a_replacement_stream():
    from service.rtc_service.rtc_stream import RtcStream

    stream = object.__new__(RtcStream)
    replacement = object()
    stream.quit = asyncio.Event()
    stream.client_session_delegate = None
    stream.owns_session = False
    stream.session_id = "test"
    factory = NS(streams={"test": replacement}, client_handler_delegate=None)
    stream.weak_factory = lambda: factory
    stream.shutdown()
    assert factory.streams["test"] is replacement


def test_late_channel_message_after_shutdown_is_ignored(monkeypatch):
    import json
    from service.rtc_service import rtc_stream

    monkeypatch.setattr(rtc_stream.AsyncAudioVideoStreamHandler, "set_channel", lambda *args: None)
    callbacks = {}

    def on(name):
        def register(callback):
            callbacks[name] = callback

        return register

    stream = object.__new__(rtc_stream.RtcStream)
    stream.quit = asyncio.Event()
    stream.owns_session = False
    stream.session_id = "test"
    stream.client_session_delegate = NS(emit_signal=lambda signal: pytest.fail("late dispatch"))
    factory = NS(streams={"test": stream}, client_handler_delegate=None)
    stream.weak_factory = lambda: factory
    stream.set_channel(NS(on=on))
    stream.shutdown()
    callbacks["message"](json.dumps({"header": {"name": "Interrupt"}}))


def test_stop_session_error_still_leaves_shutdown_idempotent():
    from handlers.client.rtc_client.client_handler_rtc import RtcClientSessionDelegate
    from service.rtc_service.rtc_stream import RtcStream

    stopped = []

    def stop(key):
        stopped.append(key)
        raise RuntimeError("synthetic teardown failure")

    stream = object.__new__(RtcStream)
    stream.quit = asyncio.Event()
    stream.owns_session = True
    stream.session_id = "test"
    stream.client_session_delegate = delegate = RtcClientSessionDelegate()
    factory = NS(streams={"test": stream}, client_handler_delegate=NS(stop_session=stop))
    stream.weak_factory = lambda: factory
    with pytest.raises(RuntimeError, match="teardown failure"):
        stream.shutdown()
    stream.shutdown()
    assert stopped == ["test"]
    assert stream.client_session_delegate is None
    for queue in delegate.output_queues.values():
        queue.put_nowait("late")
        assert queue.empty()
