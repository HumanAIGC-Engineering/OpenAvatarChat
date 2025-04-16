
import os
import shutil
import sys
from typing import Optional
import subprocess as sp

from loguru import logger

from handlers.avatar.liteavatar.algo.base_algo_adapter import BaseAlgoAdapter
from handlers.avatar.liteavatar.algo.bg_frame_counter import BgFrameCounter
from handlers.avatar.liteavatar.algo.liteavatar.lite_avatar import liteAvatar
from handlers.avatar.liteavatar.model.algo_model import AvatarAlgoConfig, AvatarInitOption, AvatarStatus
from engine_utils.directory_info import DirectoryInfo
from engine_utils.time_utils import timeit
from engine_utils.inspect_utils import InspectUtils


class Tts2faceCpuAdapter(BaseAlgoAdapter):

    TARGET_FPS = 30

    def __init__(self, handler_root: Optional[str] = None):
        super().__init__()
        self.tts2face = None
        self._bg_counter = None
        self.handler_root = handler_root
        if self.handler_root is None:
            self.handler_root = os.path.join(DirectoryInfo.get_project_dir(),
                                             "src", "handlers", "avatar", "liteavatar")

    def init(self, init_option: AvatarInitOption):
        self.change_to_algo_dir()
        data_dir = self._get_avatar_data_dir(init_option.avatar_name)
        if InspectUtils.has_init_param(liteAvatar, "use_gpu"):
            self.tts2face = liteAvatar(
                data_dir=data_dir,
                fps=init_option.video_frame_rate,
                use_gpu=init_option.use_gpu
            )
        else:
            self.tts2face = liteAvatar(
                data_dir=data_dir,
                fps=init_option.video_frame_rate
            )
        bg_step = self.TARGET_FPS // init_option.video_frame_rate
        self.tts2face.load_dynamic_model(data_dir)
        self._bg_counter = BgFrameCounter(len(self.tts2face.ref_img_list), bg_step)
        self.warm_up()
        return super().init(init_option)

    @timeit
    def audio2signal(self, audio_slice):
        signal_list = self.tts2face.audio2param(
            input_audio_byte=audio_slice.algo_audio_data,
            prefix_padding_size=0,
            is_complete=audio_slice.end_of_speech,
        )
        return signal_list

    @timeit
    def signal2img(self, signal_data, avatar_status: AvatarStatus):
        bg_frame_id = self._bg_counter.get_and_update_bg_index()
        mouth_img = self.tts2face.param2img(signal_data, bg_frame_id)
        return mouth_img, bg_frame_id

    @timeit
    def mouth2full(self, mouth_image, bg_frame_id, use_bg=False):
        full_img, _ = self.tts2face.merge_mouth_to_bg(mouth_image, bg_frame_id, use_bg)
        return full_img

    def get_idle_signal(self, idle_frame_count):
        idle_param = self.tts2face.get_idle_param()
        idle_signal_list = []
        for _ in range(idle_frame_count):
            idle_signal_list.append(idle_param)
        return idle_signal_list

    def get_algo_config(self):
        return AvatarAlgoConfig(
            input_audio_sample_rate=16000,
            input_audio_slice_duration=1
        )

    def _get_avatar_data_dir(self, avatar_name):
        logger.info("use avatar name {}", avatar_name)
        avatar_zip_path = self._download_from_modelscope(avatar_name)
        avatar_dir = self.get_avatar_dir()
        extract_dir = os.path.join(avatar_dir, os.path.dirname(avatar_name))
        avatar_data_dir = os.path.join(avatar_dir, avatar_name)
        if not os.path.exists(avatar_data_dir):
            # extract avatar data to dir
            logger.info("extract avatar data to dir {}", extract_dir)
            assert os.path.exists(avatar_zip_path)
            shutil.unpack_archive(avatar_zip_path, extract_dir)
        assert os.path.exists(avatar_data_dir)
        return avatar_data_dir
    
    def _download_from_modelscope(self, avatar_name: str) -> str:
        """
        download avatar data from modelscope to resource/avatar/liteavatar
        return avatar_zip_path
        """
        if not avatar_name.endswith(".zip"):
            avatar_name = avatar_name + ".zip"
        avatar_dir = self.get_avatar_dir()
        avatar_zip_path = os.path.join(avatar_dir, avatar_name)
        if not os.path.exists(avatar_zip_path):
            cmd = [
                "modelscope", "download", "--model", "HumanAIGC-Engineering/LiteAvatarGallery", avatar_name,
                "--local_dir", avatar_dir
                ]
            logger.info("download avatar data from modelscope, cmd: {}", " ".join(cmd))
            sp.run(cmd)
        return avatar_zip_path

    @staticmethod
    def get_avatar_dir():
        return os.path.join(DirectoryInfo.get_project_dir(), "resource", "avatar", "liteavatar")

    def change_to_algo_dir(self):
        algo_dir = os.path.join(self.handler_root, "algo", "liteavatar")
        sys.path.insert(0, algo_dir)
        os.chdir(algo_dir)
        
    def warm_up(self):
        for i in range(5):
            self.tts2face.audio2param(bytes(16000 * 2))
