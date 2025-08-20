#!/usr/bin/env python3
"""
模型文件下载脚本
参考 Tts2faceCpuAdapter._get_avatar_data_dir 功能实现

使用示例:
    # 下载模型
    python scripts/download_avatar_model.py --model "20250612/P1rcvIW8H6kvcYWNkEnBWPfg"
    
    # 查看已下载的模型
    python scripts/download_avatar_model.py --downloaded
    
    # 查看帮助
    python scripts/download_avatar_model.py --help
"""

import os
import shutil
import sys
import subprocess as sp
import argparse
from typing import Optional

from loguru import logger


class AvatarModelDownloader:
    """头像模型下载器"""
    
    def __init__(self, project_root: Optional[str] = None):
        """
        初始化下载器
        
        Args:
            project_root: 项目根目录，如果为None则自动检测
        """
        if project_root is None:
            # 获取脚本所在目录的上级目录作为项目根目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
        
        self.project_root = project_root
        self.avatar_dir = self.get_avatar_dir()
        
        # 确保目录存在
        os.makedirs(self.avatar_dir, exist_ok=True)
    
    def get_avatar_dir(self) -> str:
        """获取头像模型存储目录"""
        return os.path.join(self.project_root, "resource", "avatar", "liteavatar")
    
    def download_avatar_model(self, avatar_name: str, generate_musetalk_compat: bool = True) -> str:
        """
        下载头像模型
        
        Args:
            avatar_name: 头像模型名称
            generate_musetalk_compat: 是否生成 musetalk 兼容的 bg_video_silence.mp4 文件
            
        Returns:
            str: 头像数据目录路径
        """
        logger.info("开始下载头像模型: {}", avatar_name)
        
        # 下载模型文件
        avatar_zip_path = self._download_from_modelscope(avatar_name)
        
        # 解压模型文件
        avatar_data_dir = self._extract_avatar_data(avatar_name, avatar_zip_path)
        
        # 生成 musetalk 兼容的 bg_video_silence.mp4 文件
        if generate_musetalk_compat:
            self._generate_silence_video(avatar_data_dir)
        
        logger.info("头像模型下载完成: {}", avatar_data_dir)
        return avatar_data_dir
    
    def _generate_silence_video(self, avatar_data_dir: str) -> None:
        """
        为模型生成 musetalk 兼容的 bg_video_silence.mp4 文件（前4.8秒的视频）
        
        Args:
            avatar_data_dir: 模型数据目录路径
        """
        bg_video_path = os.path.join(avatar_data_dir, "bg_video.mp4")
        silence_video_path = os.path.join(avatar_data_dir, "bg_video_silence.mp4")
        
        # 如果 bg_video_silence.mp4 已存在，跳过生成
        if os.path.exists(silence_video_path):
            logger.info("musetalk 兼容的 bg_video_silence.mp4 已存在，跳过生成")
            return
        
        # 检查 bg_video.mp4 是否存在
        if not os.path.exists(bg_video_path):
            logger.warning("bg_video.mp4 不存在，无法生成 musetalk 兼容的 bg_video_silence.mp4")
            return
        
        logger.info("开始生成 musetalk 兼容的 bg_video_silence.mp4（前4.8秒）")
        
        try:
            # 使用 ffmpeg 截取前4.8秒的视频
            cmd = [
                "ffmpeg", "-i", bg_video_path,
                "-t", "4.8",  # 截取4.8秒
                "-c", "copy",  # 复制编码，不重新编码
                "-y",  # 覆盖输出文件
                silence_video_path
            ]
            
            logger.info("执行命令: {}", " ".join(cmd))
            result = sp.run(cmd, check=True, capture_output=True, text=True)
            logger.info("musetalk 兼容的 bg_video_silence.mp4 生成成功")
            
        except sp.CalledProcessError as e:
            logger.error("生成 musetalk 兼容的 bg_video_silence.mp4 失败: {}", e.stderr)
            raise RuntimeError(f"生成 musetalk 兼容视频失败: {e.stderr}")
        except FileNotFoundError:
            logger.error("ffmpeg 命令未找到，请确保已安装 ffmpeg")
            raise RuntimeError("ffmpeg 命令未找到，请确保已安装 ffmpeg")
    
    def _download_from_modelscope(self, avatar_name: str) -> str:
        """
        从ModelScope下载头像数据
        
        Args:
            avatar_name: 头像模型名称
            
        Returns:
            str: 下载的zip文件路径
        """
        if not avatar_name.endswith(".zip"):
            avatar_name = avatar_name + ".zip"
        
        avatar_zip_path = os.path.join(self.avatar_dir, avatar_name)
        
        if not os.path.exists(avatar_zip_path):
            logger.info("开始从ModelScope下载模型文件: {}", avatar_name)
            
            cmd = [
                "modelscope", "download", 
                "--model", "HumanAIGC-Engineering/LiteAvatarGallery", 
                avatar_name,
                "--local_dir", self.avatar_dir
            ]
            
            logger.info("执行下载命令: {}", " ".join(cmd))
            
            try:
                result = sp.run(cmd, check=True, capture_output=True, text=True)
                logger.info("下载成功")
            except sp.CalledProcessError as e:
                logger.error("下载失败: {}", e.stderr)
                raise RuntimeError(f"模型下载失败: {e.stderr}")
        else:
            logger.info("模型文件已存在: {}", avatar_zip_path)
        
        return avatar_zip_path
    
    def _extract_avatar_data(self, avatar_name: str, avatar_zip_path: str) -> str:
        """
        解压头像数据
        
        Args:
            avatar_name: 头像模型名称
            avatar_zip_path: zip文件路径
            
        Returns:
            str: 解压后的数据目录路径
        """
        extract_dir = os.path.join(self.avatar_dir, os.path.dirname(avatar_name))
        avatar_data_dir = os.path.join(self.avatar_dir, avatar_name)
        
        if not os.path.exists(avatar_data_dir):
            logger.info("开始解压模型文件到目录: {}", extract_dir)
            
            if not os.path.exists(avatar_zip_path):
                raise FileNotFoundError(f"模型文件不存在: {avatar_zip_path}")
            
            try:
                shutil.unpack_archive(avatar_zip_path, extract_dir)
                logger.info("解压完成")
            except Exception as e:
                logger.error("解压失败: {}", str(e))
                raise RuntimeError(f"模型解压失败: {str(e)}")
        else:
            logger.info("模型数据目录已存在: {}", avatar_data_dir)
        
        if not os.path.exists(avatar_data_dir):
            raise FileNotFoundError(f"解压后模型数据目录不存在: {avatar_data_dir}")
        
        return avatar_data_dir
    
    def list_available_models(self) -> list:
        """
        列出可用的模型（从ModelScope获取）
        
        Returns:
            list: 可用模型列表
        """
        logger.info("获取可用模型列表...")
        logger.warning("ModelScope CLI 不支持 list 命令，无法获取可用模型列表")
        logger.info("请访问 https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery 查看可用模型")
        logger.info("或者使用 --downloaded 参数查看已下载的模型")
        return []
    
    def list_downloaded_models(self) -> list:
        """
        列出已下载的模型
        
        Returns:
            list: 已下载模型列表
        """
        if not os.path.exists(self.avatar_dir):
            return []
        
        models = []
        # 遍历所有子目录
        for item in os.listdir(self.avatar_dir):
            item_path = os.path.join(self.avatar_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # 检查子目录中是否有真正的模型（包含模型ID的目录）
                subdir_path = os.path.join(self.avatar_dir, item)
                if os.path.exists(subdir_path):
                    for subitem in os.listdir(subdir_path):
                        subitem_path = os.path.join(subdir_path, subitem)
                        # 真正的模型目录通常包含模型ID（长字符串）且包含模型文件
                        if (os.path.isdir(subitem_path) and 
                            not subitem.endswith('.zip') and
                            self._is_model_directory(subitem_path)):
                            model_name = f"{item}/{subitem}"
                            models.append(model_name)
        
        return models
    
    def _is_model_directory(self, dir_path: str) -> bool:
        """
        判断目录是否为模型目录
        
        Args:
            dir_path: 目录路径
            
        Returns:
            bool: 是否为模型目录
        """
        if not os.path.isdir(dir_path):
            return False
        
        # 检查是否包含模型文件
        model_files = ['net.pth', 'net_encode.pt', 'net_decode.pt', 'bg_video.mp4']
        ref_frames_dir = os.path.join(dir_path, 'ref_frames')
        
        # 检查是否有模型文件或参考帧目录
        has_model_files = any(os.path.exists(os.path.join(dir_path, f)) for f in model_files)
        has_ref_frames = os.path.isdir(ref_frames_dir)
        
        # 排除一些明显不是模型的目录
        excluded_names = ['preload', '._____temp']
        dir_name = os.path.basename(dir_path)
        
        return (has_model_files or has_ref_frames) and dir_name not in excluded_names


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="头像模型下载工具")
    parser.add_argument("--model", "-m", type=str, help="要下载的模型名称")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用模型（需要访问ModelScope网站）")
    parser.add_argument("--downloaded", "-d", action="store_true", help="列出已下载的模型")
    parser.add_argument("--project-root", type=str, help="项目根目录路径")
    parser.add_argument("--no-musetalk-compat", action="store_true", help="不生成 musetalk 兼容的 bg_video_silence.mp4 文件")
    
    args = parser.parse_args()
    
    # 配置日志
    logger.remove()
    logger.add(sys.stderr, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    try:
        downloader = AvatarModelDownloader(args.project_root)
        
        if args.list:
            models = downloader.list_available_models()
            if models:
                print("可用模型列表:")
                for model in models:
                    print(f"  - {model}")
            else:
                print("无法获取可用模型列表，请访问 https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery")
        
        elif args.downloaded:
            models = downloader.list_downloaded_models()
            if models:
                print("已下载模型列表:")
                for model in models:
                    print(f"  - {model}")
            else:
                print("暂无已下载的模型")
        
        elif args.model:
            generate_musetalk_compat = not args.no_musetalk_compat
            avatar_data_dir = downloader.download_avatar_model(args.model, generate_musetalk_compat)
            print(f"模型下载完成: {avatar_data_dir}")
        
        else:
            parser.print_help()
    
    except Exception as e:
        logger.error("操作失败: {}", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 