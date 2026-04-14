from loguru import logger
from pydantic import BaseModel, Field, field_validator, model_validator
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel

class AvatarMuseTalkConfig(HandlerBaseConfigModel, BaseModel):
    """Configuration class for MuseTalk avatar handler."""
    fps: int = Field(default=25)
    batch_size: int = Field(default=5, ge=2)
    avatar_video_path: str = Field(default="")
    avatar_model_dir: str = Field(default="models/musetalk/avatar_model")
    force_create_avatar: bool = Field(default=False)
    debug: bool = Field(default=False)
    algo_audio_sample_rate: int = Field(default=16000)
    output_audio_sample_rate: int = Field(default=24000)
    model_dir: str = Field(default="models/musetalk")
    multi_thread_inference: bool = Field(default=True, description="Split UNet and VAE into separate threads for pipelined inference")
    # concurrent_limit is inherited from HandlerBaseConfigModel and auto-injected by ChatEngine from YAML config

    @field_validator("batch_size")
    @classmethod
    def _check_batch_size(cls, v: int) -> int:
        if v < 2:
            logger.error("=" * 70)
            logger.error("  [INVALID CONFIG] AvatarMusetalk batch_size must be >= 2")
            logger.error(f"  Got batch_size={v}")
            logger.error(f"  Reason: UNet/VAE inference requires batch_size >= 2 for correct padding logic.")
            logger.error(f"  Please update your YAML config: AvatarMusetalk.batch_size >= 2")
            logger.error("=" * 70)
            raise ValueError(
                f"AvatarMusetalk batch_size must be >= 2, got {v}. "
                f"Please fix your YAML config."
            )
        return v

    @model_validator(mode="after")
    def _align_fps_to_sample_rate(self) -> "AvatarMuseTalkConfig":
        """Auto-correct fps so that output_audio_sample_rate is evenly divisible by fps.

        Processor splits audio into fixed-length per-frame segments using integer
        division (samples_per_frame = sample_rate // fps).  If sample_rate % fps != 0
        the remainder samples are silently lost every second.  To avoid this, snap
        fps to the nearest divisor of sample_rate.
        """
        sr = self.output_audio_sample_rate
        if sr % self.fps == 0:
            return self
        original_fps = self.fps
        best_fps = self.fps
        for delta in range(1, self.fps):
            for candidate in (original_fps + delta, original_fps - delta):
                if candidate > 0 and sr % candidate == 0:
                    best_fps = candidate
                    break
            if sr % best_fps == 0:
                break
        self.fps = best_fps
        logger.warning("=" * 70)
        logger.warning("  [FPS AUTO-CORRECTION]")
        logger.warning(f"  Configured fps={original_fps} is NOT a divisor of output_audio_sample_rate={sr}")
        logger.warning(f"  Auto-corrected: fps {original_fps} -> {best_fps}  (samples_per_frame={sr // best_fps})")
        logger.warning(f"  Reason: processor requires sample_rate % fps == 0 for precise audio-frame alignment")
        logger.warning("=" * 70)
        return self
