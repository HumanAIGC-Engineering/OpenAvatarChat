
import math
import time
from typing import List
from src.avatar.model.algo_model import AvatarStatus, SignalResult


class Audio2SignalSpeedLimiter:
    
    def __init__(self, fps):
        self._start_time = 0
        self._total_bs_count = 0
        self._fps = fps
        
    def start(self):
        if self._start_time == 0:
            self._start_time = time.time()
    
    def adjust_generate_speed(self,
                              bs_results: List[SignalResult],
                              avatar_status: AvatarStatus):
        """
        sleep to control bs generate speed
        """
        assert self._start_time != 0
        self._total_bs_count += len(bs_results)
        target_time = self._total_bs_count / self._fps
        actual_time = time.time() - self._start_time
        if actual_time < target_time:
            sleep_time = target_time - actual_time
            sleep_time = self._get_sleep_time(sleep_time)
            time.sleep(sleep_time)

    @staticmethod
    def _get_sleep_time(sleep_time):
        sleep_time = math.floor((sleep_time) * 100) / 100
        return sleep_time
