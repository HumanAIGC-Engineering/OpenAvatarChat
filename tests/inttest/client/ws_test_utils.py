"""WebSocket 测试工具函数"""
import json
import struct
import wave
from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image


ROOT_DIR = Path(__file__).resolve().parents[3]
TEST_AUDIO_PATH = ROOT_DIR / "tests" / "inttest" / "client" / "test_16k_int16_mono.wav"


def load_test_audio_bytes() -> bytes:
    """载入测试音频 PCM 数据（16kHz mono int16）"""
    if not TEST_AUDIO_PATH.exists():
        raise FileNotFoundError(f"测试音频未找到: {TEST_AUDIO_PATH}")
    with wave.open(str(TEST_AUDIO_PATH), "rb") as wf:
        if wf.getsampwidth() != 2 or wf.getnchannels() != 1 or wf.getframerate() != 16000:
            raise ValueError("测试音频格式应为 16kHz mono int16")
        frames = wf.readframes(wf.getnframes())
    return frames


def parse_jbin_motion_data(binary_data: bytes) -> dict:
    """
    解析 Motion Data 二进制片段。
    
    现在只支持完整包格式（Welcome/完整包）:
    - 12字节头部 + JSON + 二进制
    
    拆分包现在没有头部，只是纯二进制数据，需要由调用者按顺序组装。
    """
    # 检查是否为完整包格式（12字节头部 + JSON + 二进制）
    if len(binary_data) >= 12:
        # 检查是否为 JBIN 格式
        if binary_data[0:4] == b"JBIN":
            json_size = struct.unpack("<I", binary_data[4:8])[0]
            binary_size = struct.unpack("<I", binary_data[8:12])[0]
            total_size = 12 + json_size + binary_size
            if 0 <= json_size and 0 <= binary_size and total_size <= len(binary_data):
                json_bytes = binary_data[12:12 + json_size]
                try:
                    description = json.loads(json_bytes.decode("utf-8"))
                except UnicodeDecodeError:
                    description = None
                else:
                    payload = binary_data[12 + json_size:12 + json_size + binary_size]
                    return {
                        "type": "container",
                        "description": description,
                        "binary_data": payload,
                        "json_size": json_size,
                        "binary_size": binary_size,
                    }
    
    # 如果不是完整包格式，可能是拆分包（纯二进制数据，没有头部）
    # 这种情况下，调用者应该直接使用这些二进制数据，按接收顺序组装
    raise ValueError("Binary data is not a complete container (expected JBIN format with 12-byte header)")


def generate_test_image(width: int = 640,
                        height: int = 480,
                        format: str = "JPEG") -> bytes:
    """生成测试图像（纯色或渐变）"""
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (i % 256, j % 256, (i + j) % 256)
    
    buffer = BytesIO()
    img.save(buffer, format=format, quality=80)
    return buffer.getvalue()


async def wait_for_message(ws, msg_type: str, timeout: float = 5.0) -> Optional[dict]:
    """
    等待特定类型的消息
    
    Args:
        ws: WebSocket 连接
        msg_type: 消息类型（如 "AvatarSessionInitialized"）
        timeout: 超时时间
    
    Returns:
        消息字典，如果超时返回 None
    """
    import asyncio
    
    try:
        async with asyncio.timeout(timeout):
            while True:
                message = await ws.recv()
                if isinstance(message, str):
                    data = json.loads(message)
                    if data.get("header", {}).get("name") == msg_type:
                        return data
    except asyncio.TimeoutError:
        return None

