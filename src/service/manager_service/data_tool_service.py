import asyncio
import contextlib
import copy
import json
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect
from loguru import logger


class ManagerDataToolService:
    """
    Light-weight hub to fan out context data to websocket clients.

    The hub keeps a bounded history per session so late subscribers
    can fetch recent events without unbounded memory growth.
    """

    def __init__(self, buffer_limit: int = 200, max_sessions: int = 50, expire_seconds: float = 300.0):
        self.buffer_limit = max(1, buffer_limit)
        self.max_sessions = max(1, max_sessions)
        self.expire_seconds = expire_seconds
        self._buffers: Dict[str, Deque[dict]] = {}
        # session_id -> expire_timestamp (None means not expired / active)
        self._expire_times: Dict[str, Optional[float]] = {}
        self._queues: Set[asyncio.Queue] = set()
        self._lock = threading.Lock()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._routes_registered = False
        # session_id -> set(callback(payload: Optional[dict]))
        self._interrupt_handlers: Dict[str, Set[Callable[[Optional[dict]], None]]] = {}
        # latest engine config snapshot used by runtime
        self._current_config: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _set_loop_if_needed(self, loop: asyncio.AbstractEventLoop):
        with self._lock:
            if self._loop is None:
                self._loop = loop

    def _ensure_context(self, session_id: str):
        with self._lock:
            if session_id not in self._buffers:
                self._buffers[session_id] = deque(maxlen=self.buffer_limit)
                self._expire_times[session_id] = None  # Active session, no expiration
            elif self._expire_times.get(session_id) is not None:
                # Reactivate expired session
                self._expire_times[session_id] = None

    def _shrink_buffers(self):
        with self._lock:
            for key, buffer in list(self._buffers.items()):
                if buffer.maxlen != self.buffer_limit:
                    self._buffers[key] = deque(buffer, maxlen=self.buffer_limit)

    def _cleanup_expired_sessions_if_needed(self):
        """
        Clean up expired sessions when buffer count exceeds max_sessions.
        Must be called with self._lock held.
        """
        if len(self._buffers) <= self.max_sessions:
            return

        current_time = time.time()
        # Collect expired sessions with their expire times
        expired_sessions = [
            (sid, exp_time)
            for sid, exp_time in self._expire_times.items()
            if exp_time is not None and exp_time <= current_time
        ]
        # Sort by expire time (oldest first)
        expired_sessions.sort(key=lambda x: x[1])

        # Remove oldest expired sessions until we're under the limit
        for sid, _ in expired_sessions:
            if len(self._buffers) <= self.max_sessions:
                break
            self._buffers.pop(sid, None)
            self._expire_times.pop(sid, None)

        # If still over limit, remove oldest pending-expired sessions (not yet expired but marked for expiration)
        if len(self._buffers) > self.max_sessions:
            pending_expired = [
                (sid, exp_time)
                for sid, exp_time in self._expire_times.items()
                if exp_time is not None and exp_time > current_time
            ]
            pending_expired.sort(key=lambda x: x[1])
            for sid, _ in pending_expired:
                if len(self._buffers) <= self.max_sessions:
                    break
                self._buffers.pop(sid, None)
                self._expire_times.pop(sid, None)

    def update_buffer_limit(self, new_limit: int):
        if new_limit <= 0:
            return
        self.buffer_limit = new_limit
        self._shrink_buffers()

    def register_routes(self, app):
        """
        Register websocket endpoint for data tool consumers.
        Idempotent: multiple calls will only register once.
        """
        if self._routes_registered:
            return
        self._routes_registered = True

        @app.websocket("/ws/manager/data_tool")
        async def data_tool_ws(websocket: WebSocket):
            await websocket.accept()
            self._set_loop_if_needed(asyncio.get_running_loop())
            queue: asyncio.Queue = asyncio.Queue()

            def _register_queue():
                with self._lock:
                    self._queues.add(queue)

            def _unregister_queue():
                with self._lock:
                    if queue in self._queues:
                        self._queues.remove(queue)

            _register_queue()
            try:
                sender = asyncio.create_task(self._sender_loop(websocket, queue))
                receiver = asyncio.create_task(self._receiver_loop(websocket))
                done, pending = await asyncio.wait(
                    {sender, receiver}, return_when=asyncio.FIRST_EXCEPTION
                )
                for task in pending:
                    task.cancel()
                    with contextlib.suppress(Exception):
                        await task
                for task in done:
                    if task.cancelled():
                        continue
                    exc = task.exception()
                    if exc and not isinstance(exc, (asyncio.CancelledError, WebSocketDisconnect, RuntimeError)):
                        raise exc
            except WebSocketDisconnect:
                pass
            except Exception as e:  # pragma: no cover - defensive
                logger.opt(exception=e).warning("Data tool websocket error for session")
            finally:
                _unregister_queue()

    # ------------------------------------------------------------------ #
    # Public surface for handler
    # ------------------------------------------------------------------ #
    def ensure_context(self, session_id: str):
        self._ensure_context(session_id)

    def get_all_snapshots(self):
        with self._lock:
            all_items = []
            for buffer in self._buffers.values():
                all_items.extend(list(buffer))
            return all_items

    def get_snapshot(self, session_id: str):
        with self._lock:
            buffer = self._buffers.get(session_id, None)
            if buffer is None:
                return []
            return list(buffer)

    def set_current_config(self, config: Optional[Dict[str, Any]]):
        with self._lock:
            self._current_config = copy.deepcopy(config) if config is not None else None

    def get_current_config(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            return copy.deepcopy(self._current_config) if self._current_config is not None else None

    def push_event(self, session_id: str, event: Dict[str, Any]):
        """
        Store and broadcast an event. Safe to call from non-async threads.
        """
        self._ensure_context(session_id)
        with self._lock:
            buffer = self._buffers[session_id]
            event_copy = copy.deepcopy(event)
            if event_copy.get("data", {}).get("kind") != "heartbeat":
                # heartbeat events are not stored in buffer
                buffer.append(event_copy)
            queues = list(self._queues)
            loop = self._loop
        if loop and queues:
            for q in queues:
                try:
                    loop.call_soon_threadsafe(q.put_nowait, event_copy)
                except RuntimeError as e:  # pragma: no cover - loop may be closing
                    logger.warning(f"Failed to schedule data tool event broadcast: {e}")

    def destroy_context(self, session_id: str):
        with self._lock:
            # Set expiration time instead of immediately removing buffer
            if session_id in self._buffers:
                self._expire_times[session_id] = time.time() + self.expire_seconds
            # Cleanup expired sessions if we exceed max_sessions
            self._cleanup_expired_sessions_if_needed()
            # Interrupt handlers should be removed immediately
            self._interrupt_handlers.pop(session_id, None)
            loop = self._loop
            queues = list(self._queues)
        if loop and queues:
            for q in queues:
                try:
                    loop.call_soon_threadsafe(
                        q.put_nowait, {"event": "context_closed", "session_id": session_id}
                    )
                except RuntimeError:
                    pass

    # ------------------------------------------------------------------ #
    # Manager -> engine callbacks (interrupt)
    # ------------------------------------------------------------------ #
    def register_interrupt_handler(self, session_id: str, handler: Callable[[Optional[dict]], None]):
        with self._lock:
            handlers = self._interrupt_handlers.setdefault(session_id, set())
            handlers.add(handler)

    def unregister_interrupt_handler(self, session_id: str, handler: Callable[[Optional[dict]], None]):
        with self._lock:
            handlers = self._interrupt_handlers.get(session_id)
            if not handlers:
                return
            if handler in handlers:
                handlers.remove(handler)
            if not handlers:
                self._interrupt_handlers.pop(session_id, None)

    def _fire_interrupt(self, session_id: str, payload: Optional[dict]):
        with self._lock:
            handlers = list(self._interrupt_handlers.get(session_id, ()))
        for cb in handlers:
            try:
                cb(payload)
            except Exception as e:  # pragma: no cover - defensive
                logger.warning(f"Interrupt handler error for {session_id}: {e}")

    # ------------------------------------------------------------------ #
    # Internal: websocket loops
    # ------------------------------------------------------------------ #
    async def _sender_loop(self, websocket: WebSocket, queue: asyncio.Queue):
        snapshot = self.get_all_snapshots()
        if snapshot:
            await websocket.send_json({"event": "snapshot", "items": snapshot})
        current_config = self.get_current_config()
        if current_config is not None:
            await websocket.send_json({"event": "current_config", "config": current_config})
        while True:
            try:
                item = await queue.get()
            except asyncio.CancelledError:
                return
            await websocket.send_json(item)

    async def _receiver_loop(self, websocket: WebSocket):
        while True:
            try:
                msg = await websocket.receive()
            except (WebSocketDisconnect, RuntimeError):
                return
            try:
                if "text" in msg and msg["text"]:
                    payload = json.loads(msg["text"])
                elif "bytes" in msg and msg["bytes"]:
                    payload = json.loads(msg["bytes"].decode("utf-8"))
                else:
                    continue
            except Exception:
                logger.warning("Failed to parse manager data_tool message, skip.")
                continue
            self._handle_incoming_payload(payload)

    def _handle_incoming_payload(self, payload: Any):
        """
        Accept messages from manager clients.
        Currently supports interrupt event:
        { "event": "interrupt", "session_id": "<id>", ... }
        """
        if not isinstance(payload, dict):
            return
        event = payload.get("event")
        if event != "interrupt":
            return
        session_id = payload.get("session_id")
        if not session_id:
            logger.warning("Interrupt payload missing session_id.")
            return
        self._fire_interrupt(session_id, payload)

