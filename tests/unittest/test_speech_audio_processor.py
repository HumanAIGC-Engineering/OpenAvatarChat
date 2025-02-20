import unittest
import numpy as np
from src.avatar.media.speech_audio_processor import SpeechAudioProcessor
from src.avatar.model.audio_input import SpeechAudio


class TestSpeechAudioProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = SpeechAudioProcessor(input_sample_rate=16000, output_sample_rate=8000, audio_slice_duration=1)

    def test_resample_audio(self):
        audio_data = bytearray(16000)
        resampled_audio_data = self.processor.resample_audio(audio_data, 16000, 8000)
        self.assertEqual(len(resampled_audio_data), 8000)

    def test_extend_audio_to_duration(self):
        audio_data = bytearray(16000)
        extended_audio_data = SpeechAudioProcessor.extend_audio_to_duration(audio_data, 16000, 1)
        self.assertEqual(len(extended_audio_data), 32000)

    def test_get_speech_audio_slice_no_resample(self):
        audio_data = np.array([1] * 16000, dtype=np.int16).tobytes()
        speech_audio = SpeechAudio(audio_data=audio_data, end_of_speech=False, speech_id=1, sample_rate=8000)
        slices = self.processor.get_speech_audio_slice(speech_audio)
        self.assertEqual(len(slices), 1)
        self.assertEqual(len(np.frombuffer(slices[0].algo_audio_data, dtype=np.int16)), 8000)

    def test_get_speech_audio_slice_with_resample(self):
        audio_data = np.array([1] * 16000, dtype=np.int16).tobytes()
        speech_audio = SpeechAudio(audio_data=audio_data, end_of_speech=False, speech_id=1, sample_rate=16000)
        slices = self.processor.get_speech_audio_slice(speech_audio)
        self.assertEqual(len(slices), 1)
        self.assertEqual(len(np.frombuffer(slices[0].algo_audio_data, dtype=np.int16)), 8000)

    def test_get_speech_audio_slice_end_of_speech(self):
        audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.int16).tobytes()
        speech_audio = SpeechAudio(audio_data=audio_data, end_of_speech=True, speech_id=1, sample_rate=8000)
        slices = self.processor.get_speech_audio_slice(speech_audio)
        self.assertEqual(len(slices), 1)
        self.assertEqual(len(np.frombuffer(slices[0].algo_audio_data, dtype=np.int16)), 8000)
        
    def test_get_speech_audio_slice_short_audio(self):
        audio_data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=np.int16).tobytes()
        speech_audio = SpeechAudio(audio_data=audio_data, end_of_speech=False, speech_id=1, sample_rate=8000)
        slices = self.processor.get_speech_audio_slice(speech_audio)
        self.assertEqual(len(slices), 0)

    def test_get_speech_audio_slice_long_audio(self):
        audio_data = np.array([1] * 32000, dtype=np.int16).tobytes()
        speech_audio = SpeechAudio(audio_data=audio_data, end_of_speech=False, speech_id=1, sample_rate=8000)
        slices = self.processor.get_speech_audio_slice(speech_audio)
        self.assertEqual(len(slices), 2)
        self.assertEqual(len(np.frombuffer(slices[0].algo_audio_data, dtype=np.int16)), 8000)
        self.assertEqual(len(np.frombuffer(slices[1].algo_audio_data, dtype=np.int16)), 8000)


if __name__ == '__main__':
    unittest.main()
