"""
SchedulerLayer — framework for registering and running periodic/scheduled jobs.

Replaces scattered threading.Timer and _idle_trigger_loop patterns
with a unified, configurable job scheduler.
"""

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from loguru import logger


@dataclass
class ScheduledJob:
    """Definition of a scheduled periodic task."""
    name: str
    interval: float
    handler: Callable[[], Any]
    active_hours: Optional[Tuple[int, int]] = None  # (start_hour, end_hour) local time
    enabled: bool = True

    # Runtime state (managed by SchedulerLayer)
    _last_run: float = field(default=0.0, repr=False)
    _run_count: int = field(default=0, repr=False)
    _paused: bool = field(default=False, repr=False)


class SchedulerLayer:
    """Manages and runs scheduled jobs in a single background thread."""

    def __init__(self, tick_interval: float = 1.0):
        self._tick_interval = tick_interval
        self._jobs: Dict[str, ScheduledJob] = {}
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._running = False

    def register(self, job: ScheduledJob):
        """Register a new scheduled job."""
        with self._lock:
            if job.name in self._jobs:
                logger.warning(f"[Scheduler] Job '{job.name}' already registered, replacing")
            self._jobs[job.name] = job
            logger.info(
                f"[Scheduler] Registered job '{job.name}' "
                f"(interval={job.interval}s, active_hours={job.active_hours})"
            )

    def unregister(self, name: str) -> bool:
        with self._lock:
            if name in self._jobs:
                del self._jobs[name]
                logger.info(f"[Scheduler] Unregistered job '{name}'")
                return True
            return False

    def pause(self, name: str) -> bool:
        with self._lock:
            job = self._jobs.get(name)
            if job:
                job._paused = True
                logger.info(f"[Scheduler] Paused job '{name}'")
                return True
            return False

    def resume(self, name: str) -> bool:
        with self._lock:
            job = self._jobs.get(name)
            if job:
                job._paused = False
                logger.info(f"[Scheduler] Resumed job '{name}'")
                return True
            return False

    def start(self):
        """Start the scheduler background thread."""
        if self._running:
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="scheduler-layer"
        )
        self._running = True
        self._thread.start()
        logger.info(f"[Scheduler] Started with {len(self._jobs)} jobs")

    def stop(self):
        """Stop the scheduler and wait for the thread to finish."""
        if not self._running:
            return
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=self._tick_interval * 3)
        self._running = False
        logger.info("[Scheduler] Stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get status of all registered jobs."""
        with self._lock:
            return {
                "running": self._running,
                "jobs": {
                    name: {
                        "enabled": job.enabled,
                        "paused": job._paused,
                        "interval": job.interval,
                        "run_count": job._run_count,
                        "last_run": job._last_run,
                        "active_hours": job.active_hours,
                    }
                    for name, job in self._jobs.items()
                },
            }

    @property
    def job_names(self) -> List[str]:
        with self._lock:
            return list(self._jobs.keys())

    def _run_loop(self):
        """Main scheduler loop — checks and runs due jobs each tick."""
        while not self._stop_event.is_set():
            self._tick()
            self._stop_event.wait(timeout=self._tick_interval)

    def _tick(self):
        """Check all jobs and run those that are due."""
        now = time.time()
        current_hour = datetime.now().hour

        with self._lock:
            jobs_snapshot = list(self._jobs.values())

        for job in jobs_snapshot:
            if not job.enabled or job._paused:
                continue
            if job.active_hours:
                start_h, end_h = job.active_hours
                if start_h <= end_h:
                    if not (start_h <= current_hour < end_h):
                        continue
                else:  # wraps midnight, e.g. (22, 6)
                    if not (current_hour >= start_h or current_hour < end_h):
                        continue
            if (now - job._last_run) < job.interval:
                continue

            try:
                job.handler()
                job._run_count += 1
                job._last_run = now
            except Exception as e:
                logger.error(f"[Scheduler] Job '{job.name}' failed: {e}")
                job._last_run = now
