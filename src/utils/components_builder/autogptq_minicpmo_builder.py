import glob
import os
import sys

from utils.directory_info import DirectoryInfo


class AutoGPTQMiniCPMOBuilder:
    def __init__(self):
        self.dir_name = "AutoGPTQ-MiniCPMo"
        self.build_path = os.path.join(DirectoryInfo.get_project_dir(), "build", self.dir_name)
        self.src_dir = os.path.join(self.build_path, "AutoGPTQ")

    def prepare(self):
        if not os.path.exists(self.src_dir):
            os.system(f"git clone https://github.com/OpenBMB/AutoGPTQ.git {self.src_dir} &&"
                      f"cd {self.src_dir} &&"
                      f"git checkout minicpmo")

    def build(self):
        wheel_path = os.path.join(self.src_dir, "dist", "auto_gptq-*.whl")
        files = glob.glob(wheel_path)
        if len(files) > 0:
            return files[0]
        self.prepare()
        os.system(f"cd {self.src_dir} && {sys.executable} setup.py bdist_wheel")
        wheels = glob.glob(wheel_path)
        if len(wheels) > 0:
            return wheels[0]
        return None

    def install(self):
        wheel = self.build()
        if wheel is not None:
            os.system(f"{sys.executable} -m pip install {wheel}")
