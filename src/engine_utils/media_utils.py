

import base64
from io import BytesIO
import os
import time
from typing import Union
import wave

import PIL
from loguru import logger
import numpy as np

from src.engine_utils.directory_info import DirectoryInfo


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


class ImageUtils:
    
    @staticmethod
    def format_image(image: Union[str, np.ndarray]):
        if isinstance(image, np.ndarray):
            return ImageUtils.numpy2base64(image)
        return image
    
    # 注意rgb顺序
    @staticmethod
    def numpy2base64(video_frame, format="JPEG"):
        # if video_frame.dtype != np.uint8:
        #     video_frame = (video_frame * 255).astype(np.uint8)

        # 将 NumPy 数组转换为 PIL 图像对象
        image = PIL.Image.fromarray(np.squeeze(video_frame)[..., ::-1])

        # 创建一个内存缓冲区
        buffered = BytesIO()

        # 将图像保存到内存缓冲区中
        image.save(buffered, format=format)

        # 获取二进制数据并编码为 Base64
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        # 添加 Base64 数据头（可选）
        data_url = f"data:image/{format.lower()};base64,{base64_image}"
        dump_image = False
        if dump_image:
            from engine_utils.directory_info import DirectoryInfo
            ImageUtils.save_base64_image(base64_image, f"{DirectoryInfo.get_project_dir()}/temp/{time.localtime().tm_min}_{time.localtime().tm_sec}.jpg")
        return data_url
    
    @staticmethod
    def save_base64_image(base64_data, output_path):
        """
        将 Base64 编码的图片保存为本地文件。

        :param base64_data: Base64 编码的图片字符串（不包括头部信息）
        :param output_path: 保存图片的本地路径（包含文件名和扩展名）
        """
        try:
            # 去掉可能存在的 Base64 头部信息（如 "data:image/png;base64,"）
            if ',' in base64_data:
                _, base64_data = base64_data.split(',', 1)
            
            # 解码 Base64 数据
            image_data = base64.b64decode(base64_data)

            # 将解码后的数据写入文件
            with open(output_path, 'wb') as f:
                f.write(image_data)
            
            logger.debug(f"图片已成功保存至 {output_path}")
        
        except Exception as e:
            logger.debug(f"保存图片时出错: {e}")
