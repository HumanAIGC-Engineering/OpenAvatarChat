"""
PendingConfirmationsManager — tracks items that need user confirmation.

Inspired by the TodoWrite pattern (learn-claude-code s03) but repurposed:
instead of planning tasks, this tracks items the agent has presented to the
user that still await a yes/no decision (exec approvals, scheduled-task
confirmations, etc.).

The manager is owned by ``ChatAgentContext`` and ticked every agent-loop round.
After *N* rounds without progress on any ``pending`` item, ``get_nag_reminder``
returns a ``<reminder>`` block that gets injected into the LLM messages so the
agent re-asks the user.
"""

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from loguru import logger

VALID_STATUSES = {"pending", "confirmed", "denied", "expired"}
NAG_INTERVAL_ROUNDS = 3


@dataclass
class PendingItem:
    id: str
    text: str
    status: str = "pending"
    source: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)


class PendingConfirmationsManager:
    """Thread-safe tracker for items awaiting user confirmation."""

    def __init__(self, nag_interval: int = NAG_INTERVAL_ROUNDS):
        self._items: Dict[str, PendingItem] = {}
        self._lock = threading.Lock()
        self._rounds_since_reminded: int = 0
        self._nag_interval = nag_interval

    def upsert(self, items: List[dict]) -> str:
        """Create or update pending items (called by the ``pending_confirmations`` tool).

        Each dict must contain ``id``; optional keys: ``text``, ``status``, ``source``.
        Returns the current list rendered as text.
        """
        with self._lock:
            now = time.time()
            for raw in items:
                item_id = raw.get("id", "").strip()
                if not item_id:
                    continue
                status = raw.get("status", "pending")
                if status not in VALID_STATUSES:
                    status = "pending"

                existing = self._items.get(item_id)
                if existing:
                    if "text" in raw:
                        existing.text = raw["text"]
                    existing.status = status
                    if "source" in raw:
                        existing.source = raw["source"]
                    existing.updated_at = now
                else:
                    self._items[item_id] = PendingItem(
                        id=item_id,
                        text=raw.get("text", ""),
                        status=status,
                        source=raw.get("source", ""),
                        created_at=now,
                        updated_at=now,
                    )
                logger.info(
                    f"[PendingConfirm] upsert id={item_id} status={status}"
                )
            self._rounds_since_reminded = 0
        return self.render()

    def render(self) -> str:
        """Return a human-readable summary of all items."""
        with self._lock:
            if not self._items:
                return "(无待确认项)"

            lines = []
            for item in self._items.values():
                marker = {
                    "pending": "⏳",
                    "confirmed": "✅",
                    "denied": "❌",
                    "expired": "⌛",
                }.get(item.status, "?")
                line = f"  {marker} [{item.id}] {item.text} ({item.status})"
                if item.status == "pending":
                    line += (
                        f' → 需调用 exec_approve'
                        f'(approval_id="{item.id}", '
                        f'decision="allow-once"/"allow-always"/"deny")'
                    )
                lines.append(line)
            return "待确认列表:\n" + "\n".join(lines)

    def has_pending(self) -> bool:
        with self._lock:
            return any(i.status == "pending" for i in self._items.values())

    def get_pending_items(self) -> List[PendingItem]:
        with self._lock:
            return [i for i in self._items.values() if i.status == "pending"]

    def purge_resolved(self, max_age: float = 120.0):
        """Remove resolved (non-pending) items older than *max_age* seconds.

        Called periodically so the internal dict doesn't grow unbounded and
        ``has_pending`` / ``render`` stay accurate after approvals.
        """
        with self._lock:
            now = time.time()
            stale = [
                k for k, v in self._items.items()
                if v.status != "pending" and (now - v.updated_at) > max_age
            ]
            for k in stale:
                del self._items[k]
            if stale:
                logger.debug(f"[PendingConfirm] purged {len(stale)} resolved items")

    def tick_round(self):
        """Called once per agent-loop round.

        Also purges old resolved entries to keep the dict clean.
        """
        with self._lock:
            self._rounds_since_reminded += 1
        self.purge_resolved()

    def get_nag_reminder(self) -> Optional[str]:
        """If pending items exist and enough rounds have passed, return a
        ``<reminder>`` block for injection into messages."""
        with self._lock:
            if not any(i.status == "pending" for i in self._items.values()):
                return None
            if self._rounds_since_reminded < self._nag_interval:
                return None
            self._rounds_since_reminded = 0

        pending_list = self.render()
        return (
            f"<reminder>\n"
            f"你有未完成的待确认事项，请提醒用户处理：\n"
            f"{pending_list}\n"
            f"</reminder>"
        )

    def to_serializable(self) -> List[dict]:
        """Serialize items for frontend / API consumption."""
        with self._lock:
            return [
                {
                    "id": i.id,
                    "text": i.text,
                    "status": i.status,
                    "source": i.source,
                    "created_at": i.created_at,
                    "updated_at": i.updated_at,
                }
                for i in self._items.values()
            ]
