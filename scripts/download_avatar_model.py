#!/usr/bin/env python3
"""
模型文件下载脚本

参考 Tts2faceCpuAdapter._get_avatar_data_dir 功能实现

功能特性:
- 下载LiteAvatar模型文件
- 自动生成musetalk兼容的bg_video_silence.mp4文件
- 列出已下载的模型及其路径信息

使用示例:
    # 下载模型
    python scripts/download_avatar_model.py --model "20250612/P1rcvIW8H6kvcYWNkEnBWPfg"

    # 查看已下载的模型列表
    # 输出格式: avatar_name（for LiteAvatar config）    avatar_video_path（for Musetalk config）
    python scripts/download_avatar_model.py --downloaded

    # 查看帮助
    python scripts/download_avatar_model.py --help

输出示例 (--downloaded):
    已下载模型列表:
    avatar_name（for LiteAvatar config）    avatar_video_path（for Musetalk config）
    --------------------------------------------------------------------------------
    20250408/P1lXrpJL507-PZ4hMPutyF7A       resource/avatar/liteavatar/20250408/P1lXrpJL507-PZ4hMPutyF7A/bg_video_silence.mp4
    20250612/P1rcvIW8H6kvcYWNkEnBWPfg       resource/avatar/liteavatar/20250612/P1rcvIW8H6kvcYWNkEnBWPfg/bg_video_silence.mp4

Avatar Model Download Script

Reference Tts2faceCpuAdapter._get_avatar_data_dir implementation

Features:
- Download LiteAvatar model files
- Auto-generate musetalk compatible bg_video_silence.mp4 file
- List downloaded models and their path information

Usage Examples:
    # Download model
    python scripts/download_avatar_model.py --model "20250612/P1rcvIW8H6kvcYWNkEnBWPfg"

    # List downloaded models
    # Output format: avatar_name（for LiteAvatar config）    avatar_video_path（for Musetalk config）
    python scripts/download_avatar_model.py --downloaded

    # Show help
    python scripts/download_avatar_model.py --help

Output Example (--downloaded):
    Downloaded Models List:
    avatar_name（for LiteAvatar config）    avatar_video_path（for Musetalk config）
    --------------------------------------------------------------------------------
    20250408/P1lXrpJL507-PZ4hMPutyF7A       resource/avatar/liteavatar/20250408/P1lXrpJL507-PZ4hMPutyF7A/bg_video_silence.mp4
    20250612/P1rcvIW8H6kvcYWNkEnBWPfg       resource/avatar/liteavatar/20250612/P1rcvIW8H6kvcYWNkEnBWPfg/bg_video_silence.mp4"""

import os
import shutil
import sys
import subprocess as sp
import argparse
from typing import Optional

from loguru import logger


class AvatarModelDownloader:
    """Avatar model downloader"""

    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize the downloader

        Args:
            project_root: Project root directory, auto-detected if None
        """
        if project_root is None:
            # Get the parent directory of script location as project root
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)

        self.project_root = project_root
        self.avatar_dir = self.get_avatar_dir()

        # Ensure directory exists
        os.makedirs(self.avatar_dir, exist_ok=True)

    def get_avatar_dir(self) -> str:
        """Get avatar model storage directory"""
        return os.path.join(self.project_root, "resource", "avatar", "liteavatar")
    
    def download_avatar_model(self, avatar_name: str, generate_musetalk_compat: bool = True) -> str:
        """
        Download avatar model

        Args:
            avatar_name: Avatar model name
            generate_musetalk_compat: Whether to generate musetalk compatible bg_video_silence.mp4 file

        Returns:
            str: Avatar data directory path
        """
        logger.info("Starting avatar model download: {}", avatar_name)

        # Download model file
        avatar_zip_path = self._download_from_modelscope(avatar_name)

        # Extract model file
        avatar_data_dir = self._extract_avatar_data(avatar_name, avatar_zip_path)

        # Generate musetalk compatible bg_video_silence.mp4 file
        if generate_musetalk_compat:
            self._generate_silence_video(avatar_data_dir)

        logger.info("Avatar model download completed: {}", avatar_data_dir)
        return avatar_data_dir
    
    def _generate_silence_video(self, avatar_data_dir: str) -> None:
        """
        Generate musetalk compatible bg_video_silence.mp4 file (first 4.8 seconds of video)

        Args:
            avatar_data_dir: Model data directory path
        """
        bg_video_path = os.path.join(avatar_data_dir, "bg_video.mp4")
        silence_video_path = os.path.join(avatar_data_dir, "bg_video_silence.mp4")

        # Skip generation if bg_video_silence.mp4 already exists
        if os.path.exists(silence_video_path):
            logger.info("Musetalk compatible bg_video_silence.mp4 already exists, skipping generation")
            return

        # Check if bg_video.mp4 exists
        if not os.path.exists(bg_video_path):
            logger.warning("bg_video.mp4 not found, cannot generate musetalk compatible bg_video_silence.mp4")
            return

        logger.info("Starting generation of musetalk compatible bg_video_silence.mp4 (first 4.8 seconds)")
        
        try:
            # Use ffmpeg to extract first 4.8 seconds of video
            cmd = [
                "ffmpeg", "-i", bg_video_path,
                "-t", "4.8",  # Extract 4.8 seconds
                "-c", "copy",  # Copy encoding without re-encoding
                "-y",  # Overwrite output file
                silence_video_path
            ]

            logger.info("Executing command: {}", " ".join(cmd))
            result = sp.run(cmd, check=True, capture_output=True, text=True)
            logger.info("Musetalk compatible bg_video_silence.mp4 generated successfully")

        except sp.CalledProcessError as e:
            logger.error("Failed to generate musetalk compatible bg_video_silence.mp4: {}", e.stderr)
            raise RuntimeError(f"Failed to generate musetalk compatible video: {e.stderr}")
        except FileNotFoundError:
            logger.error("ffmpeg command not found, please ensure ffmpeg is installed")
            raise RuntimeError("ffmpeg command not found, please ensure ffmpeg is installed")
    
    def _download_from_modelscope(self, avatar_name: str) -> str:
        """
        Download avatar data from ModelScope

        Args:
            avatar_name: Avatar model name

        Returns:
            str: Downloaded zip file path
        """
        if not avatar_name.endswith(".zip"):
            avatar_name = avatar_name + ".zip"
        
        avatar_zip_path = os.path.join(self.avatar_dir, avatar_name)
        
        if not os.path.exists(avatar_zip_path):
            logger.info("Starting download from ModelScope: {}", avatar_name)

            cmd = [
                "modelscope", "download",
                "--model", "HumanAIGC-Engineering/LiteAvatarGallery",
                avatar_name,
                "--local_dir", self.avatar_dir
            ]

            logger.info("Executing download command: {}", " ".join(cmd))

            try:
                result = sp.run(cmd, check=True, capture_output=True, text=True)
                logger.info("Download successful")
            except sp.CalledProcessError as e:
                logger.error("Download failed: {}", e.stderr)
                raise RuntimeError(f"Model download failed: {e.stderr}")
        else:
            logger.info("Model file already exists: {}", avatar_zip_path)
        
        return avatar_zip_path
    
    def _extract_avatar_data(self, avatar_name: str, avatar_zip_path: str) -> str:
        """
        Extract avatar data

        Args:
            avatar_name: Avatar model name
            avatar_zip_path: Zip file path

        Returns:
            str: Extracted data directory path
        """
        extract_dir = os.path.join(self.avatar_dir, os.path.dirname(avatar_name))
        avatar_data_dir = os.path.join(self.avatar_dir, avatar_name)
        
        if not os.path.exists(avatar_data_dir):
            logger.info("Starting extraction of model file to directory: {}", extract_dir)

            if not os.path.exists(avatar_zip_path):
                raise FileNotFoundError(f"Model file does not exist: {avatar_zip_path}")

            try:
                shutil.unpack_archive(avatar_zip_path, extract_dir)
                logger.info("Extraction completed")
            except Exception as e:
                logger.error("Extraction failed: {}", str(e))
                raise RuntimeError(f"Model extraction failed: {str(e)}")
        else:
            logger.info("Model data directory already exists: {}", avatar_data_dir)

        if not os.path.exists(avatar_data_dir):
            raise FileNotFoundError(f"Model data directory does not exist after extraction: {avatar_data_dir}")
        
        return avatar_data_dir
    
    def list_available_models(self) -> list:
        """
        List available models (from ModelScope)

        Returns:
            list: Available models list
        """
        logger.info("Getting available models list...")
        logger.warning("ModelScope CLI does not support list command, cannot get available models list")
        logger.info("Please visit https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery to view available models")
        logger.info("Or use --downloaded parameter to view downloaded models")
        return []

    def list_downloaded_models(self) -> list:
        """
        List downloaded models

        Returns:
            list: Downloaded models list, each element is a tuple (avatar_name, musetalk_video_path)
        """
        if not os.path.exists(self.avatar_dir):
            return []

        models = []
        # Traverse all subdirectories
        for item in os.listdir(self.avatar_dir):
            item_path = os.path.join(self.avatar_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # Check if subdirectories contain actual models (directories with model IDs)
                subdir_path = os.path.join(self.avatar_dir, item)
                if os.path.exists(subdir_path):
                    for subitem in os.listdir(subdir_path):
                        subitem_path = os.path.join(subdir_path, subitem)
                        # Actual model directories usually contain model IDs (long strings) and model files
                        if (os.path.isdir(subitem_path) and
                            not subitem.endswith('.zip') and
                            self._is_model_directory(subitem_path)):
                            model_name = f"{item}/{subitem}"
                            musetalk_video_path = self._get_musetalk_video_path(model_name)
                            models.append((model_name, musetalk_video_path))

        return models
    
    def _is_model_directory(self, dir_path: str) -> bool:
        """
        Check if directory is a model directory

        Args:
            dir_path: Directory path

        Returns:
            bool: Whether it is a model directory
        """
        if not os.path.isdir(dir_path):
            return False

        # Check if contains model files
        model_files = ['net.pth', 'net_encode.pt', 'net_decode.pt', 'bg_video.mp4']
        ref_frames_dir = os.path.join(dir_path, 'ref_frames')

        # Check if has model files or reference frames directory
        has_model_files = any(os.path.exists(os.path.join(dir_path, f)) for f in model_files)
        has_ref_frames = os.path.isdir(ref_frames_dir)

        # Exclude directories that are obviously not models
        excluded_names = ['preload', '._____temp']
        dir_name = os.path.basename(dir_path)

        return (has_model_files or has_ref_frames) and dir_name not in excluded_names

    def _get_musetalk_video_path(self, model_id: str) -> str:
        """
        Generate musetalk video path based on model ID

        Args:
            model_id: Model ID (usually a long string)

        Returns:
            str: Musetalk video path
        """
        # Build complete path relative to project root, pointing to bg_video_silence.mp4 in downloaded model directory
        relative_path = f"resource/avatar/liteavatar/{model_id}/bg_video_silence.mp4"
        return relative_path


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Avatar model download tool")
    parser.add_argument("--model", "-m", type=str, help="Model name to download")
    parser.add_argument("--list", "-l", action="store_true", help="List available models (requires visiting ModelScope website)")
    parser.add_argument("--downloaded", "-d", action="store_true", help="List downloaded models")
    parser.add_argument("--project-root", type=str, help="Project root directory path")
    parser.add_argument("--no-musetalk-compat", action="store_true", help="Do not generate musetalk compatible bg_video_silence.mp4 file")
    
    args = parser.parse_args()
    
    # Configure logging
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    try:
        downloader = AvatarModelDownloader(args.project_root)

        if args.list:
            models = downloader.list_available_models()
            if models:
                print("Available models list:")
                for model in models:
                    print(f"  - {model}")
            else:
                print("Cannot get available models list, please visit https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery")

        elif args.downloaded:
            models = downloader.list_downloaded_models()
            if models:
                print("Downloaded models list:")
                print("avatar_name（for LiteAvatar config）\tavatar_video_path（for Musetalk config）")
                print("-" * 80)
                for avatar_name, musetalk_video_path in models:
                    print(f"{avatar_name}\t{musetalk_video_path}")
            else:
                print("No downloaded models yet")

        elif args.model:
            generate_musetalk_compat = not args.no_musetalk_compat
            avatar_data_dir = downloader.download_avatar_model(args.model, generate_musetalk_compat)
            print(f"Model download completed: {avatar_data_dir}")

        else:
            parser.print_help()

    except Exception as e:
        logger.error("Operation failed: {}", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 