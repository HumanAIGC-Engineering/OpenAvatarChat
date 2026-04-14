"""
TaskMirror — persistent local mirror of OC task states.

JSON file on disk that survives OAC restarts and is not affected by
auto-compact dialogue compression. Provides active task summaries for L4.
"""

import json
import os
import threading
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

from loguru import logger


@dataclass
class TaskEntry:
    task_id: str
    title: str
    status: str  # "running", "completed", "failed", "pending"
    submitted_at: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    brief: str = ""
    result_summary: str = ""


class TaskMirror:
    """Persistent JSON-based task state mirror."""

    def __init__(self, mirror_path: str = ".oac_tasks/mirror.json", max_completed: int = 10):
        self._path = mirror_path
        self._max_completed = max_completed
        self._lock = threading.Lock()
        self._tasks: Dict[str, TaskEntry] = {}
        self._load()

    def update_task(self, task_id: str, **kwargs):
        """Create or update a task entry."""
        with self._lock:
            if task_id in self._tasks:
                entry = self._tasks[task_id]
                for k, v in kwargs.items():
                    if hasattr(entry, k):
                        setattr(entry, k, v)
                entry.last_update = time.time()
            else:
                self._tasks[task_id] = TaskEntry(task_id=task_id, **kwargs)
            self._save_locked()

    def complete_task(self, task_id: str, status: str = "completed", result_summary: str = ""):
        self.update_task(task_id, status=status, result_summary=result_summary)

    def get_active_tasks(self) -> List[TaskEntry]:
        with self._lock:
            return [
                t for t in self._tasks.values()
                if t.status in ("running", "pending")
            ]

    def get_active_brief(self) -> str:
        """Format active tasks as a brief for L4 (Task Brief)."""
        active = self.get_active_tasks()
        if not active:
            return ""
        lines = []
        for t in active:
            lines.append(f"- [{t.status}] {t.title}: {t.brief}")
        return "\n".join(lines)

    def get_recently_completed(self) -> List[TaskEntry]:
        with self._lock:
            completed = [
                t for t in self._tasks.values()
                if t.status in ("completed", "failed")
            ]
            completed.sort(key=lambda t: t.last_update, reverse=True)
            return completed[:self._max_completed]

    def cleanup_old(self, max_age_hours: float = 24.0):
        """Remove completed tasks older than max_age_hours."""
        cutoff = time.time() - max_age_hours * 3600
        with self._lock:
            to_remove = [
                tid for tid, t in self._tasks.items()
                if t.status in ("completed", "failed") and t.last_update < cutoff
            ]
            for tid in to_remove:
                del self._tasks[tid]
            if to_remove:
                self._save_locked()
                logger.info(f"[TaskMirror] Cleaned up {len(to_remove)} old tasks")

    def _load(self):
        if not os.path.isfile(self._path):
            return
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for tid, entry_data in data.get("tasks", {}).items():
                self._tasks[tid] = TaskEntry(**entry_data)
            logger.info(f"[TaskMirror] Loaded {len(self._tasks)} tasks from {self._path}")
        except Exception as e:
            logger.warning(f"[TaskMirror] Failed to load {self._path}: {e}")

    def _save_locked(self):
        """Save to disk (must be called with lock held)."""
        try:
            os.makedirs(os.path.dirname(self._path) or ".", exist_ok=True)
            data = {
                "tasks": {tid: asdict(t) for tid, t in self._tasks.items()},
                "updated_at": time.time(),
            }
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"[TaskMirror] Failed to save: {e}")
