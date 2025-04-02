
import os
import sys
import time

from loguru import logger
from handlers.avatar.liteavatar.avatar_processor_factory import AvatarAlgoType, AvatarProcessorFactory
from handlers.avatar.liteavatar.model import AvatarInitOption
from handlers.avatar.liteavatar.model import SpeechAudio
from src.utils.directory_info import DirectoryInfo
from src.utils.media_utils import AudioUtils
from tests.inttest.avatar.sample_output_handler import SampleOutputHandler


class AvatarDemo:
    def __init__(self):
        logger.remove()
        logger.add(sys.stdout, level="INFO")

    def run(self):
        test_input_file_path = os.path.join(
            DirectoryInfo.get_project_dir(), "resource", "audio", "ymr_48k.wav"
        )
        audio_bytes, sample_rate = AudioUtils.read_wav_to_bytes(test_input_file_path)
        
        processor = AvatarProcessorFactory.create_avatar_processor(
            "",
            AvatarAlgoType.TTS2FACE_CPU,
            AvatarInitOption(audio_sample_rate=sample_rate, video_frame_rate=25))
        processor.register_output_handler(SampleOutputHandler())
        processor.start()

        time.sleep(1)
        processor.add_audio(SpeechAudio(
            audio_data=audio_bytes,
            speech_id="1",
            end_of_speech=True,
            sample_rate=sample_rate))
        time.sleep(17)

        processor.stop()


if __name__ == "__main__":
    demo = AvatarDemo()
    demo.run()
