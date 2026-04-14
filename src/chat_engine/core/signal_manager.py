import queue
import threading
from typing import Optional, Dict, List, Callable

from chat_engine.contexts.session_clock import SessionClock
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule


class SignalEmitter:
    def __init__(self, signal_queue: queue.Queue, session_clock: SessionClock, source_name: Optional[str] = None):
        self.source_name = source_name
        self.session_clock = session_clock
        self.signal_queue = signal_queue

    def emit(self, signal: ChatSignal):
        signal.source_name = self.source_name
        self.signal_queue.put_nowait(signal)


class SignalManager:
    def __init__(self, session_clock: SessionClock):
        self.session_clock = session_clock
        self.running_flags = [False]
        self.signal_queue = queue.Queue()
        self.signal_distribute_thread: Optional[threading.Thread] = None
        self.signal_listeners: Dict[SignalFilterRule, List[Callable[[ChatSignal], None]]] = {}

    def get_clock(self):
        return self.session_clock

    def init(self):
        if self.signal_distribute_thread is not None:
            raise RuntimeError("SignalManager has been initialized")
        self.running_flags[0] = True
        self.signal_distribute_thread = threading.Thread(
            target=self.signal_distribute_thread_func,
            args=(self.running_flags, self.signal_queue, self.signal_listeners))
        self.signal_distribute_thread.start()

    def shutdown(self):
        self.running_flags[0] = False
        if self.signal_distribute_thread is not None:
            try:
                self.signal_distribute_thread.join()
            except RuntimeError:
                pass
        self.signal_distribute_thread = None

    def get_emitter(self, source_name: Optional[str] = None):
        emitter = SignalEmitter(self.signal_queue, self.session_clock, source_name)
        return emitter

    def register_listener(self, listener: Callable[[ChatSignal], None],
                          signal_filter: SignalFilterRule = SignalFilterRule(None, None, None)):
        listener_list = self.signal_listeners.setdefault(signal_filter, [])
        if listener not in listener_list:
            listener_list.append(listener)

    def clear_listeners(self):
        self.signal_listeners.clear()

    @classmethod
    def signal_distribute_thread_func(cls, running_flags, signal_queue: queue.Queue,
                                      signal_listeners: Dict[SignalFilterRule, List[Callable[[ChatSignal], None]]]):
        while running_flags[0]:
            try:
                signal: ChatSignal = signal_queue.get(block=True, timeout=0.5)
            except queue.Empty:
                continue
            signal_stream_type = signal.related_stream.data_type if signal.related_stream is not None else None
            filter_keys = [
                SignalFilterRule(signal.type, signal.source_type, None),
                SignalFilterRule(None, signal.source_type, None),
                SignalFilterRule(signal.type, None, None),
                SignalFilterRule(None, None, None),
            ]
            if signal_stream_type is not None:
                filter_keys += [
                    SignalFilterRule(signal.type, signal.source_type, signal_stream_type),
                    SignalFilterRule(None, signal.source_type, signal_stream_type),
                    SignalFilterRule(signal.type, None, signal_stream_type),
                    SignalFilterRule(None, None, signal_stream_type),
                ]
            for filter_key in filter_keys:
                for listener in signal_listeners.get(filter_key, []):
                    listener(signal)
