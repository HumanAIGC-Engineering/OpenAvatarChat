

from enum import Enum
from typing import Any, Optional, TypeVar
import av
from pydantic import BaseModel


class AvatarStatus(Enum):
    SPEAKING = 0
    LISTENING = 1


class AvatarInitOption(BaseModel):
    audio_sample_rate: int
    video_frame_rate: int
    avatar_name: str
    debug: bool = False
    enable_fast_mode: bool = False
    use_gpu: bool = True


class AudioSlice(BaseModel):
    speech_id: Any
    play_audio_data: bytes
    play_audio_sample_rate: int
    algo_audio_data: Optional[bytes]
    algo_audio_sample_rate: int
    end_of_speech: bool
    front_padding_duration: float = 0
    end_padding_duration: float = 0

    def get_audio_duration(self) -> float:
        return len(self.play_audio_data) / self.play_audio_sample_rate / 2


SignalType = TypeVar('SignalType')


class SignalResult(BaseModel):
    speech_id: Any
    end_of_speech: bool
    avatar_status: AvatarStatus
    audio_slice: Optional[AudioSlice] = None
    frame_id: int
    global_frame_id: int = 0
    middle_data: SignalType


class MouthResult(BaseModel):
    speech_id: Any
    avatar_status: AvatarStatus
    end_of_speech: bool
    bg_frame_id: int
    mouth_image: Any
    audio_slice: Optional[AudioSlice] = None
    global_frame_id: int

    model_config = {
        "arbitrary_types_allowed": True
    }


class VideoResult(BaseModel):
    speech_id: Any
    avatar_status: AvatarStatus
    video_frame: Any | av.VideoFrame
    end_of_speech: bool
    bg_frame_id: int

    model_config = {
        "arbitrary_types_allowed": True
    }


class AudioResult(BaseModel):
    speech_id: Any
    audio_frame: bytes | av.AudioFrame

    model_config = {
        "arbitrary_types_allowed": True
    }


class AvatarAlgoConfig(BaseModel):
    input_audio_sample_rate: int
    input_audio_slice_duration: float     # input audio duration in second
