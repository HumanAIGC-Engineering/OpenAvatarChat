
from loguru import logger


class VideoAudioAligner:

    def __init__(self, fps):
        self._fps = fps

        self._current_speech_id = ""
        self._audio_byte_length_current_speech = 0
        self._audio_data_current_speech = bytearray()
        self._total_frame_count_current_speech = 0
        self._audio_start_idx = 0
        self._returned_audio_length_current_speech = 0

    def get_aligned_audio(self):
        pass

    def get_speech_level_algined_audio(self, audio_data, origin_sample_rate,
                                       frame_count, speech_id, end_of_speech):
        if speech_id != self._current_speech_id:
            self._audio_byte_length_current_speech = 0
            self._audio_data_current_speech = bytearray()
            self._current_speech_id = speech_id
            self._total_frame_count_current_speech = 0
            self._audio_start_idx = 0
            self._returned_audio_length_current_speech = 0
        self._audio_data_current_speech += audio_data
        self._total_frame_count_current_speech += frame_count

        audio_length_per_frame = origin_sample_rate / self._fps * 2
        assert audio_length_per_frame.is_integer()

        total_audio_length = int(self._total_frame_count_current_speech *
                                 audio_length_per_frame)

        if not end_of_speech:
            ret_audio = audio_data
        else:
            diff = total_audio_length - len(self._audio_data_current_speech)
            if diff > 0:
                logger.info(
                    f"align video: add extra audio of length {diff}")
                self._audio_data_current_speech += bytearray(diff)
            else:
                logger.info(
                    f"align video: remove tail audio of length {diff}")
                self._audio_data_current_speech = self._audio_data_current_speech[:
                                                                                  total_audio_length]
            ret_audio = self._audio_data_current_speech[self._audio_start_idx:]
        self._returned_audio_length_current_speech += len(ret_audio)
        logger.info(
            "audio of speech {}, end of speech {}, total returned audio length {}, "
            "actual audio length {}, start index {}",
            speech_id, end_of_speech,
            self._returned_audio_length_current_speech, total_audio_length, self._audio_start_idx)
        self._audio_start_idx += len(ret_audio)
        return ret_audio
