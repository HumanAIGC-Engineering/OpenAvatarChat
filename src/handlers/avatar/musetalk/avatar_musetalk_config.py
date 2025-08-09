from pydantic import BaseModel, Field
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel

class AvatarMuseTalkConfig(HandlerBaseConfigModel, BaseModel):
    """Configuration class for MuseTalk avatar handler."""
    fps: int = Field(default=25)  # Video frames per second
    batch_size: int = Field(default=5, ge=2)  # Batch size for processing audio and video frames, must be greater than 2
    avatar_video_path: str = Field(default="")  # Path to the initialization video
    avatar_model_dir: str = Field(default="models/musetalk/avatar_model")  # Directory for output results 
    force_create_avatar: bool = Field(default=False)  # Whether to force data regeneration
    debug: bool = Field(default=False)  # Enable debug mode
    debug_save_handler_audio: bool = Field(default=False)  # Enable debug mode
    debug_replay_speech_id: str = Field(default="")  # Enable debug mode
    algo_audio_sample_rate: int = Field(default=16000)  # Internal algorithm sample rate, fixed at 16000, used for input audio resampling
    output_audio_sample_rate: int = Field(default=24000)  # Output audio sample rate (for resampling)
    model_dir: str = Field(default="models/musetalk")  # Root directory for models
    multi_thread_inference: bool = Field(default=True)  # Whether to use multi-thread inference
