

from typing import List

import librosa
from loguru import logger
import numpy as np
from src.avatar.model.algo_model import AudioSlice
from src.avatar.model.audio_input import SpeechAudio


class SpeechAudioProcessor:
    def __init__(self,
                 input_sample_rate: int,
                 output_sample_rate: int,
                 audio_slice_duration: int,
                 enable_fast_mode: bool = False):
        self._input_sample_rate = input_sample_rate
        self._output_sample_rate = output_sample_rate
        self._audio_slice_duration = audio_slice_duration
        self._enable_fast_mode = enable_fast_mode

        self._current_audio = SpeechAudio()

    def get_speech_audio_slice(self, speech_audio: SpeechAudio) \
            -> List[AudioSlice]:
        """
        convert input speech audio to slice with duration of
        audio_slice_duration, resample audio if needed
        """
        
        if self._current_audio.speech_id != speech_audio.speech_id:
            # new speech, extend this to audio slice duration,
            # so that algo can start immediately
            logger.info("generate first audio slice for speech {}", speech_audio.speech_id)
            self._current_audio = speech_audio.model_copy()
            if self._enable_fast_mode:
                audio_data = self._current_audio.audio_data

                target_length = int(2 * speech_audio.sample_rate * self._audio_slice_duration)
                padding_length = target_length - len(audio_data)
                audio_data = bytes(padding_length) + audio_data
                
                padding_duration = padding_length / 2 / speech_audio.sample_rate
                
                audio_slice = self._create_audio_slice(
                    speech_id=speech_audio.speech_id,
                    play_audio_data=audio_data,
                    play_audio_sample_rate=speech_audio.sample_rate,
                    end_of_speech=speech_audio.end_of_speech,
                    front_padding_duration=padding_duration
                )
                self._current_audio.audio_data = bytes()
                return [audio_slice]
        else:
            self._extend_current_audio(speech_audio)
        
        logger.info("input speech audio {}, end of speech {}, duration {:.3f}s, current audio length {}",
                    speech_audio.speech_id, speech_audio.end_of_speech, speech_audio.get_audio_duration(),
                    len(self._current_audio.audio_data))

        output_audio_list = []
        while self._current_audio.get_audio_duration() >= self._audio_slice_duration:
            play_audio_data_length = int(2 * self._input_sample_rate *
                                         self._audio_slice_duration)
            play_audio_data = self._current_audio.audio_data[:play_audio_data_length]
            self._current_audio.audio_data = self._current_audio.audio_data[play_audio_data_length:]
            end_of_speech = len(self._current_audio.audio_data) == 0 and speech_audio.end_of_speech
            audio_slice = self._create_audio_slice(
                speech_audio.speech_id,
                play_audio_data,
                self._input_sample_rate,
                end_of_speech)
            output_audio_list.append(audio_slice)
        if self._current_audio.end_of_speech and len(self._current_audio.audio_data) > 0:
            play_audio_data, end_padding_duration = self.extend_audio_to_duration(
                self._current_audio.audio_data,
                self._input_sample_rate,
                self._audio_slice_duration,
                False
            )
            output_audio_list.append(self._create_audio_slice(
                speech_audio.speech_id,
                play_audio_data,
                self._input_sample_rate,
                True,
                end_padding_duration=end_padding_duration))
            self._current_audio = SpeechAudio()
        return output_audio_list

    def _extend_current_audio(self, speech_audio: SpeechAudio):
        assert self._current_audio.speech_id == speech_audio.speech_id
        self._current_audio.audio_data += speech_audio.audio_data
        self._current_audio.end_of_speech = speech_audio.end_of_speech

    def _create_audio_slice(self,
                            speech_id: str,
                            play_audio_data: bytes,
                            play_audio_sample_rate: int,
                            end_of_speech: bool,
                            front_padding_duration: float = 0,
                            end_padding_duration: float = 0) -> AudioSlice:
        algo_audio = self.resample_audio(play_audio_data,
                                         self._input_sample_rate,
                                         self._output_sample_rate)
        return AudioSlice(
            algo_audio_data=algo_audio,
            algo_audio_sample_rate=self._output_sample_rate,
            end_of_speech=end_of_speech,
            play_audio_data=play_audio_data,
            play_audio_sample_rate=play_audio_sample_rate,
            speech_id=speech_id,
            front_padding_duration=front_padding_duration,
            end_padding_duration=end_padding_duration
        )

    @staticmethod
    def extend_audio_to_duration(audio_data: bytes,
                                 sample_rate: int,
                                 duration: int,
                                 padding_front: bool):
        target_length = int(2 * sample_rate * duration)
        padding_length = target_length - len(audio_data)
        if padding_length < 0:
            return audio_data
        if padding_front:
            audio_data = bytes(padding_length) + audio_data
        else:
            audio_data = bytes(audio_data) + bytes(padding_length)
        return audio_data, padding_length / 2 / sample_rate

    @staticmethod
    def resample_audio(audio_data: bytes,
                       origin_sample_rate: int,
                       target_sample_rate: int) -> bytes:
        if origin_sample_rate == target_sample_rate:
            return audio_data

        origin_np_array = np.frombuffer(audio_data, np.short)
        audio_float32 = origin_np_array.astype(np.float32) / np.iinfo(
            np.int16).max
        resampled_float: np.ndarray = librosa.resample(
            audio_float32,
            orig_sr=origin_sample_rate,
            target_sr=target_sample_rate)
        resampled_pcm = (resampled_float * np.iinfo(np.short).max).astype(
            np.int16)
        resample_data = bytearray(resampled_pcm.tobytes())

        return resample_data
