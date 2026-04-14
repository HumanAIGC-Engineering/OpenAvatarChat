from pydantic import BaseModel, Field
from loguru import logger

from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel


class FlashHeadConfig(HandlerBaseConfigModel, BaseModel):
    """Configuration class for FlashHead avatar handler (Lite mode)."""

    ckpt_dir: str = Field(
        default="models/SoulX-FlashHead-1_3B",
        description="Path to the FlashHead model checkpoint directory.",
    )
    wav2vec_dir: str = Field(
        default="models/wav2vec2-base-960h",
        description="Path to the wav2vec2 model directory (shared with LAM).",
    )
    model_type: str = Field(
        default="lite",
        description="Model type: 'lite' (single GPU real-time) or 'pro' (higher quality).",
    )
    cond_image_path: str = Field(
        default="",
        description="Path to the condition image for the talking head. Required.",
    )
    fps: int = Field(default=25, description="Target video frame rate.")
    algo_audio_sample_rate: int = Field(
        default=16000,
        description="Audio sample rate expected by FlashHead (wav2vec2 input).",
    )
    output_audio_sample_rate: int = Field(
        default=24000,
        description="Audio sample rate from TTS, passed through to client.",
    )
    base_seed: int = Field(default=42, description="Random seed for reproducibility.")
    use_face_crop: bool = Field(
        default=False,
        description="Enable automatic face detection and cropping on the condition image.",
    )
    cached_audio_duration: int = Field(
        default=8,
        description="Audio context window in seconds for streaming inference.",
    )
    color_correction_strength: float = Field(
        default=1.0,
        description="Strength of color correction applied to generated frames.",
    )
    idle_noise_amplitude: float = Field(
        default=0.003,
        description="Peak amplitude of the breathing-patterned noise used for idle "
                    "audio. A 4-second breathing cycle modulates the noise envelope "
                    "to give wav2vec2 richer temporal structure. "
                    "~0.003 corresponds to ambient room tone (approx -50 dBFS). "
                    "Set to 0.0 to use pure silence.",
    )
    debug: bool = Field(default=False, description="Enable debug logging.")
    # concurrent_limit is inherited from HandlerBaseConfigModel and auto-injected by ChatEngine
