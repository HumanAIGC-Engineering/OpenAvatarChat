from typing import Any

import numpy as np

from chat_engine.data_models.runtime_data.motion_data_descriptors import MotionDataDescription, BufferDescription
from chat_engine.data_models.runtime_data.motion_entry_serializer_base import BaseMotionEntrySerializer, \
    EntrySerializeResult


class MotionEntryAudioInt16Serializer(BaseMotionEntrySerializer):
    def __init__(self):
        pass

    def create_context(self) -> Any:
        return None

    def serialize(self, _context, motion_data_descriptor: MotionDataDescription,
               buffer_descriptor: BufferDescription,
               data: np.ndarray, force_flush: bool = False) -> EntrySerializeResult:
        if str(data.dtype) == "int16":
            return EntrySerializeResult(
                data=data.tobytes(),
                buffer_descriptor=buffer_descriptor,
            )
        out_descriptor = BufferDescription.model_validate(buffer_descriptor.model_dump())
        out_data = data
        if data.dtype in (np.float16, np.float32, np.float64):
            out_data = data * 32767
        out_data = out_data.astype(np.int16)
        out_descriptor.data_type = str(out_data.dtype)
        result = EntrySerializeResult(
            data=out_data.tobytes(),
            buffer_descriptor=out_descriptor,
        )
        return result

    def reset(self, context: Any):
        pass
