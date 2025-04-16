from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import numpy as np

from chat_engine.data_models.runtime_data.motion_data_descriptors import BufferDescription, MotionDataDescription


@dataclass
class EntrySerializeResult:
    buffer_descriptor: BufferDescription
    data: bytes


class BaseMotionEntrySerializer(ABC):
    @abstractmethod
    def create_context(self) -> Any:
        pass

    @abstractmethod
    def serialize(self, context: Any, motion_data_descriptor: MotionDataDescription,
               buffer_descriptor: BufferDescription,
               data: np.ndarray, force_flush: bool = False) -> EntrySerializeResult:
        pass

    @abstractmethod
    def reset(self, context: Any):
        pass
