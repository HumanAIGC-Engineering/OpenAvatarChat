from typing import Optional, List, Dict

from pydantic import BaseModel, Field, SerializeAsAny

from chat_engine.data_models.runtime_data.event_model import EventData


class BufferDescription(BaseModel):
    data_type: str = "float32"
    data_offset: int = 0
    shape: List[int] = Field(default_factory=list)
    channel_names: Optional[List[str]] = Field(default_factory=list)
    sample_rate: Optional[float] = Field(default=None)
    metadata: Dict[str, str] = Field(default_factory=dict)
    data_id: int = -1
    timeline_axis: Optional[int] = Field(default=0)
    channel_axis: Optional[int] = Field(default=None)

    def get_sample_num(self):
        if self.shape is None or self.timeline_axis >= len(self.shape):
            return 0
        return self.shape[self.timeline_axis]

    def get_shape_from_sample_num(self, sample_num: int):
        if self.shape is None or self.timeline_axis >= len(self.shape):
            return []
        output = self.shape.copy()
        output[self.timeline_axis] = sample_num
        return output


class MotionDataDescription(BaseModel):
    data_records: Dict[str, BufferDescription] = Field(default_factory=dict)
    metadata: Optional[Dict[str, str]] = Field(default_factory=dict)
    events: Optional[List[SerializeAsAny[EventData]]] = Field(default_factory=list)
    batch_name: Optional[str] = Field(default=None)
    batch_id: Optional[int] = Field(default=None)
    start_of_batch: Optional[bool] = Field(default=None)
    end_of_batch: Optional[bool] = Field(default=False)
