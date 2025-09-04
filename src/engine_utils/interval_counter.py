
from collections import defaultdict
import json
import time

from loguru import logger


class IntervalCounter:
    def __init__(self, name, interval: int = 10):
        self._name = name
        self._last_log_time = 0
        self._start_time = 0
        self._interval = interval
        self._interval_counter = 0
        self._total_counter = 0
        
        self._counter_dict = defaultdict(int)

    def add(self, val=1):
        self._interval_counter += val
        self._total_counter += val
        now = time.time()
        if self._last_log_time == 0:
            self._start_time = now
            self._last_log_time = now
        if now - self._last_log_time > self._interval:
            if isinstance(self._total_counter, float):
                logger.info(
                    "[{}] total: {:.3f}, interval: {:.3f}, avg_per_second: {:.3f}",
                    self._name, self._total_counter, self._interval_counter,
                    self._total_counter / (now - self._start_time)
                )
            else:
                logger.info(
                    "[{}] total: {}, interval: {}, avg_per_second: {:.3f}",
                    self._name, self._total_counter, self._interval_counter,
                    self._total_counter / (now - self._start_time)
                )
            self._interval_counter = 0
            self._last_log_time = now

    def add_property(self, key: str, val=1):
        if key.startswith("total"):
            raise RuntimeError("key should not start with 'total'")
        interval_key = key
        total_key = f"{key}_total"
        self._counter_dict[interval_key] += val
        self._counter_dict[total_key] += val
        now = time.time()
        if self._last_log_time == 0:
            self._start_time = now
            self._last_log_time = now
        if now - self._last_log_time > self._interval:
            print_obj = dict()
            for k, v in self._counter_dict.items():
                if isinstance(v, float):
                    print_obj[k] = round(v, 3)
                else:
                    print_obj[k] = v
                if k.endswith("total"):
                    avg_key = k.replace("total", "per_second")
                    print_obj[avg_key] = round(v / (now - self._start_time), 3)
                else:
                    self._counter_dict[k] = 0
            logger.info("[{}] {}", self._name, json.dumps(print_obj, indent=4))
            self._last_log_time = now

    def reset(self):
        self._interval_counter = 0
        self._total_counter = 0
        self._last_log_time = 0
        self._start_time = 0
        logger.info("[{}] reset", self._name)
