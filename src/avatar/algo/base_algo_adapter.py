from abc import ABC, abstractmethod
from typing import List

import numpy as np

from src.avatar.model.algo_model import (
    AvatarInitOption, AudioSlice, AvatarAlgoConfig,
    AvatarStatus, SignalType)


class BaseAlgoAdapter(ABC):
    @abstractmethod
    def init(self, init_option: AvatarInitOption):
        pass

    @abstractmethod
    def audio2signal(self, audio_slice: AudioSlice) -> List[SignalType]:
        pass

    @abstractmethod
    def signal2img(self,
                   signal_data: SignalType,
                   avatar_status: AvatarStatus) -> tuple[np.ndarray, int]:
        pass

    @abstractmethod
    def mouth2full(self, mouth_image: np.ndarray, bg_frame_id: int) -> np.ndarray:
        pass

    @abstractmethod
    def get_idle_signal(self, idle_frame_count) -> List[SignalType]:
        pass

    @abstractmethod
    def get_algo_config(self) -> AvatarAlgoConfig:
        """
        return algo config, algo processor can feed algo with audio slice
        with demanded format
        """
        pass
