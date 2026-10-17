"""FIFO storage for worker-thread producers and one asyncio consumer loop."""

import asyncio
from collections import deque
import threading


class ThreadSafeAsyncQueue:
    def __init__(self):
        self._items = deque()
        self._lock = threading.Lock()
        self._loop = None
        self._available = None
        self._wake_pending = False
        self._closed = False

    @property
    def maxsize(self):
        return 0

    def qsize(self):
        with self._lock:
            return len(self._items)

    def empty(self):
        return self.qsize() == 0

    def _schedule_wake_locked(self):
        if self._loop is not None and not self._wake_pending:
            self._wake_pending = True
            try:
                self._loop.call_soon_threadsafe(self._wake)
            except RuntimeError:
                self._wake_pending = False

    def put_nowait(self, item):
        with self._lock:
            if self._closed:
                return
            self._items.append(item)
            self._schedule_wake_locked()

    def _wake(self):
        with self._lock:
            self._wake_pending = False
            if self._closed or self._items:
                self._available.set()

    def get_nowait(self):
        with self._lock:
            if not self._items:
                raise asyncio.QueueEmpty
            return self._items.popleft()

    async def get(self):
        loop = asyncio.get_running_loop()
        with self._lock:
            if self._loop is None:
                self._loop = loop
                self._available = asyncio.Event()
            elif self._loop is not loop:
                raise RuntimeError("RTC output queue belongs to a different event loop")
        while True:
            with self._lock:
                if self._closed:
                    raise asyncio.CancelledError("RTC output queue is closed")
                if self._items:
                    return self._items.popleft()
                self._available.clear()
            await self._available.wait()

    def clear(self):
        with self._lock:
            self._items.clear()

    def close(self):
        with self._lock:
            self._closed = True
            self._items.clear()
            self._schedule_wake_locked()
