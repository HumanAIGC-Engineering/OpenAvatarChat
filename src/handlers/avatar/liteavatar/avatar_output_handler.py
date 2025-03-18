

from abc import ABC, abstractmethod
from handlers.avatar.liteavatar.model.algo_model import AudioResult, AvatarInitOption, AvatarStatus, VideoResult


class AvatarOutputHandler(ABC):
    @abstractmethod
    def on_audio(self, audio_result: AudioResult) -> None:
        pass

    @abstractmethod
    def on_video(self, video_result: VideoResult) -> None:
        pass

    @abstractmethod
    def on_start(self, init_option: AvatarInitOption):
        pass

    @abstractmethod
    def on_stop(self):
        pass

    @abstractmethod
    def on_avatar_status_change(self, speech_id, avatar_status: AvatarStatus):
        pass
