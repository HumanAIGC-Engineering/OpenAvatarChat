"""
TaskNotificationQueue — buffers async task completion notifications from OC.

When OC completes a background task, the notification is pushed here.
ChatAgent drains the queue each turn and injects <background-results> into
the dialogue history.  Multiple notifications sharing the same ``merge_key``
(typically ``tool_call_id`` or ``oc_session_id``) are coalesced into a single
entry before prompt injection so the LLM sees one concise summary per logical
task rather than N raw callbacks.
"""

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from loguru import logger


@dataclass
class TaskNotification:
    task_id: str
    status: str  # "completed", "failed", "progress"
    result_summary: str = ""
    timestamp: float = field(default_factory=time.time)
    merge_key: str = ""


class TaskNotificationQueue:
    """Thread-safe queue for background task notifications."""

    def __init__(self, max_size: int = 100):
        self._queue: List[TaskNotification] = []
        self._lock = threading.Lock()
        self._max_size = max_size

    def push(self, notification: TaskNotification):
        with self._lock:
            self._queue.append(notification)
            if len(self._queue) > self._max_size:
                dropped = self._queue.pop(0)
                logger.warning(
                    f"[TaskNotifQueue] Dropped oldest notification: {dropped.task_id}"
                )
        logger.info(
            f"[TaskNotifQueue] Pushed: {notification.task_id} ({notification.status})"
        )

    def drain(self) -> List[TaskNotification]:
        """Drain all pending notifications. Returns list and clears the queue."""
        with self._lock:
            items = list(self._queue)
            self._queue.clear()
        if items:
            logger.info(f"[TaskNotifQueue] Drained {len(items)} notifications")
        return items

    def drain_merged(self) -> List[TaskNotification]:
        """Drain and merge notifications that share the same ``merge_key``.

        Notifications without a ``merge_key`` pass through unmodified.
        When multiple notifications share a key their ``result_summary``
        texts are concatenated chronologically and the latest ``status``
        wins (terminal statuses "completed"/"failed" take precedence).
        """
        raw = self.drain()
        if not raw:
            return []
        return self._merge(raw)

    def peek(self) -> List[TaskNotification]:
        with self._lock:
            return list(self._queue)

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._queue)

    def format_for_prompt(self, notifications: Optional[List[TaskNotification]] = None) -> str:
        """Format notifications as <background-results> block for prompt injection."""
        items = notifications if notifications is not None else self.drain()
        if not items:
            return ""

        lines = []
        for n in items:
            lines.append(f"[task:{n.task_id}] {n.status}: {n.result_summary}")

        return "<background-results>\n" + "\n".join(lines) + "\n</background-results>"

    # ── merge helpers ──

    _TERMINAL_STATUSES = {"completed", "failed"}

    @classmethod
    def _merge(cls, items: List[TaskNotification]) -> List[TaskNotification]:
        """Merge items sharing the same non-empty ``merge_key``."""
        no_key: List[TaskNotification] = []
        groups: Dict[str, List[TaskNotification]] = defaultdict(list)

        for n in items:
            if n.merge_key:
                groups[n.merge_key].append(n)
            else:
                no_key.append(n)

        merged: List[TaskNotification] = list(no_key)
        for key, group in groups.items():
            group.sort(key=lambda n: n.timestamp)
            combined_text = "\n".join(
                g.result_summary for g in group if g.result_summary
            )
            best_status = group[-1].status
            for g in group:
                if g.status in cls._TERMINAL_STATUSES:
                    best_status = g.status
                    break

            merged.append(TaskNotification(
                task_id=group[0].task_id,
                status=best_status,
                result_summary=combined_text,
                timestamp=group[-1].timestamp,
                merge_key=key,
            ))
            if len(group) > 1:
                logger.info(
                    f"[TaskNotifQueue] Merged {len(group)} notifications "
                    f"for merge_key={key}"
                )

        merged.sort(key=lambda n: n.timestamp)
        return merged
