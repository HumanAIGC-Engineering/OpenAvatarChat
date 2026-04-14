from enum import Enum
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
from pydantic import BaseModel


class MuseTalkAvatarStatus(Enum):
    SPEAKING = 0
    LISTENING = 1


class MuseTalkSpeechAudio(BaseModel):
    speech_id: Any = ""
    end_of_speech: bool = False
    sample_rate: int = 16000
    audio_data: Any = b""  # bytes or np.ndarray

    model_config = {"arbitrary_types_allowed": True}

    def get_audio_duration(self) -> float:
        if isinstance(self.audio_data, bytes):
            return len(self.audio_data) / self.sample_rate / 4  # float32 = 4 bytes
        elif isinstance(self.audio_data, np.ndarray):
            return len(self.audio_data) / self.sample_rate
        return 0.0


@dataclass
class MuseTalkProcessorCallbacks:
    """Callback interface injected into Processor by Context at creation time."""
    on_video_frame: Optional[Callable[[np.ndarray], None]] = None
    on_audio_frame: Optional[Callable[[np.ndarray], None]] = None
    on_speech_end: Optional[Callable[[str], None]] = None


# ---------------------------------------------------------------------------
# Internal pipeline queue item models
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class AudioQueueItem:
    """_audio_queue: add_audio() -> _feature_extractor_worker"""
    audio_data: Any  # np.ndarray float32
    speech_id: Any = ""
    end_of_speech: bool = False
    generation_id: int = 0


@dataclass(slots=True)
class WhisperQueueItem:
    """_whisper_queue: _feature_extractor_worker -> _frame_generator_worker"""
    whisper_chunks: Any  # torch.Tensor [1, 50, 384]
    speech_id: Any = ""
    end_of_speech: bool = False
    audio_data: Any = None  # np.ndarray, single frame's audio


@dataclass(slots=True)
class UNetQueueItem:
    """_unet_queue: _frame_generator_unet_worker -> _frame_generator_vae_worker"""
    pred_latents: Any  # torch.Tensor [B, 4, 32, 32]
    speech_id: Any = ""  # List[str] for batch
    avatar_status: MuseTalkAvatarStatus = MuseTalkAvatarStatus.SPEAKING
    end_of_speech: Any = False  # List[bool] for batch
    audio_data: Any = None  # List[np.ndarray] for batch
    valid_num: int = 0
    idx_list: Any = None  # List[int]
    timestamp: float = 0.0


@dataclass(slots=True)
class ComposeQueueItem:
    """_compose_queue: _frame_generator_*_worker -> _compose_worker
       _output_queue:  _compose_worker -> _frame_collector_worker (with frame field set)"""
    recon: Any = None  # np.ndarray, reconstructed face crop
    idx: int = 0
    speech_id: Any = ""
    avatar_status: MuseTalkAvatarStatus = MuseTalkAvatarStatus.SPEAKING
    end_of_speech: bool = False
    audio_segment: Any = None  # np.ndarray
    frame_id: int = 0
    timestamp: float = 0.0
    frame: Any = None  # np.ndarray, set after res2combined in _compose_worker
