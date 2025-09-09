from threading import Lock

from handlers.avatar.liteavatar.model.algo_model import AudioSlice
from loguru import logger


class SpeechAudioAligner:
    
    def __init__(self, fps, audio_sample_rate):
        self._speech_id = ""
        self._audio_data = bytearray()
        self._audio_start_idx = 0
        self._audio_sample_rate = audio_sample_rate
        self._fps = fps
        self._audio_length_per_frame = audio_sample_rate / fps * 2
        self._audio_lock = Lock()
        logger.info("SpeechAudioAligner init fps: {}, audio_sample_rate: {}, audio_length_per_frame: {}", fps, audio_sample_rate, self._audio_length_per_frame)

    def add_audio(self, audio_data, speech_id):
        with self._audio_lock:
            if speech_id != self._speech_id:
                # new speech
                self._speech_id = speech_id
                self._audio_data = bytearray()
                self._audio_start_idx = 0
            self._audio_data += audio_data
    
    def get_speech_level_algined_audio(self, video_frame_count = 1, end_of_speech = False) -> AudioSlice:
        audio_duration = int(video_frame_count * self._audio_length_per_frame)
        audio_end_idx = self._audio_start_idx + audio_duration
        audio_data = self._audio_data[self._audio_start_idx:audio_end_idx]
        if len(audio_data) < audio_duration:
            audio_data = audio_data + bytearray(audio_duration - len(audio_data))
        self._audio_start_idx = audio_end_idx
        return AudioSlice(
            speech_id=self._speech_id,
            play_audio_data=audio_data,
            play_audio_sample_rate=self._audio_sample_rate,
            algo_audio_data=None,
            algo_audio_sample_rate=0,
            end_of_speech=end_of_speech,
            front_padding_duration=0,
            end_padding_duration=0
        )