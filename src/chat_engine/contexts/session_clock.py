import time
from typing import Tuple


class SessionClock:
    def __init__(self, timestamp_base: int = 16000):
        self.start_time: float = -1.0
        self.timestamp_base: int = timestamp_base

    def start(self):
        if self.start_time < 0:
            now = time.monotonic()
            self.start_time = now

    def get_timestamp(self) -> Tuple[int, int]:
        now = time.monotonic()
        if self.start_time < 0:
            return -1, 0
        else:
            return (
                round((now - self.start_time) * self.timestamp_base),
                self.timestamp_base
            )
