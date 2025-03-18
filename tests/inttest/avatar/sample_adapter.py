

import numpy as np
from handlers.avatar.liteavatar.algo.base_algo_adapter import BaseAlgoAdapter
from handlers.avatar.liteavatar.model import (
    AvatarInitOption, AudioSlice, AvatarAlgoConfig,
    AvatarStatus, SignalType)


class SampleAdapter(BaseAlgoAdapter):
    
    def init(self, init_option: AvatarInitOption):
        self._init_option = init_option
    
    def audio2signal(self, audio_slice: AudioSlice) -> list[SignalType]:
        len_audio = audio_slice.get_audio_duration()
        out_bs_count = int(len_audio * self._init_option.video_frame_rate)
        bs_results = []
        for _ in range(out_bs_count):
            bs_result = np.zeros((52))
            bs_results.append(bs_result)
        return bs_results

    def signal2img(self, bs_data, avatar_status: AvatarStatus) -> np.ndarray:
        if avatar_status == AvatarStatus.LISTENING:
            image_data = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            image_data = np.ones((480, 640, 3), dtype=np.uint8) * 255

        return image_data

    def get_idle_signal(self, idle_frame_count) -> list[SignalType]:
        bs_results = []
        for _ in range(idle_frame_count):
            bs_result = np.zeros((52))
            bs_results.append(bs_result)
        return bs_results

    def get_algo_config(self):
        return AvatarAlgoConfig(
            input_audio_sample_rate=16000,
            input_audio_slice_duration=1
        )
