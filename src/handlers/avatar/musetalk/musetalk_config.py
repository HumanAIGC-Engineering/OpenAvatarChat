from loguru import logger
from pydantic import BaseModel, Field, field_validator, model_validator
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel

class AvatarMuseTalkConfig(HandlerBaseConfigModel, BaseModel):
    """Configuration class for MuseTalk avatar handler."""
    # Recommended fps values (>=15, divisors of output_audio_sample_rate=24000 within [1, 49]):
    #   15, 16, 20, 24, 25, 30, 32, 40, 48
    # Any other value is auto-corrected to the nearest divisor by
    # _align_fps_to_sample_rate (see below) and will then mismatch RtcClient.output_video_fps,
    # causing server load to fail. Set fps to one of the listed values directly.
    # Trade-off: higher fps => smaller per-frame GPU budget T=1/fps (e.g. T=20.83ms at 48 vs
    # UNet ~14ms — very tight, prefer batch_size>=4 at fps>=48).
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

    @field_validator("fps")
    @classmethod
    def _check_fps_upper_bound(cls, v: int) -> int:
        # MuseTalk's whisper feature window relies on whisper_idx_multiplier = 50/fps > 1,
        # i.e. ceil(50/fps) >= 2, otherwise the right padding in
        # AudioProcessor.get_whisper_chunk is insufficient and the last frame's
        # 10-token slice goes out of bounds (assert -> exit() kills the worker silently).
        # Hard cap at 49; recommended values are around 25 (the upstream training fps).
        if v < 1 or v > 49:
            logger.error("=" * 70)
            logger.error("  [INVALID CONFIG] AvatarMusetalk fps must satisfy 1 <= fps <= 49")
            logger.error(f"  Got fps={v}")
            logger.error(f"  Reason: MuseTalk's whisper feature window requires 50/fps > 1.")
            logger.error(f"  At fps>=50 the right-padding in get_whisper_chunk is too small")
            logger.error(f"  and the last frame slice goes out of bounds (silent worker death).")
            logger.error(f"  Please update your YAML config: AvatarMusetalk.fps in [1, 49]")
            logger.error("=" * 70)
            raise ValueError(
                f"AvatarMusetalk fps must be in [1, 49], got {v}. "
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
        # Snap candidates must also stay within the algorithm's safe range (<=49),
        # otherwise auto-correction could push e.g. fps=49 -> 50 and re-trigger the
        # whisper-window out-of-bounds bug guarded by _check_fps_upper_bound.
        for delta in range(1, self.fps):
            for candidate in (original_fps + delta, original_fps - delta):
                if 0 < candidate <= 49 and sr % candidate == 0:
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
