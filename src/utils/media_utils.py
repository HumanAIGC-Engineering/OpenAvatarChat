

import os
import wave

from loguru import logger

from src.utils.directory_info import DirectoryInfo


class AudioUtils:

    @staticmethod
    def read_wav_to_bytes(file_path) -> tuple[bytes, int]:
        try:
            # 打开WAV文件
            with wave.open(file_path, 'rb') as wav_file:
                # 获取WAV文件的参数
                params = wav_file.getparams()
                logger.info("Channels: {}, Sample Width: {}, Frame Rate: {}, Number of Frames: {}",
                            params.nchannels, params.sampwidth, params.framerate, params.nframes)

                # 读取所有帧
                frames = wav_file.readframes(params.nframes)
                return frames, params.framerate
        except wave.Error as e:
            logger.info("Error reading WAV file: {}", e)
            return None, None

    @classmethod
    def get_test_audio(cls) -> tuple[bytes, int]:
        audio_path = os.path.join(
            DirectoryInfo.get_project_dir(), "resource", "audio", "ymr_48k.wav"
        )
        return cls.read_wav_to_bytes(audio_path)


class VideoUtils:
    pass
