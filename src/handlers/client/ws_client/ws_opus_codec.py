"""
WebSocket Opus 编解码器
提供 Opus 音频编解码功能，用于 WebSocket 音频传输
"""
import struct
from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import numpy as np
from loguru import logger

# 尝试导入 opuslib
try:
    import opuslib
    OPUS_AVAILABLE = True
except ImportError:
    OPUS_AVAILABLE = False
    logger.warning("opuslib not available, Opus codec will be disabled")


# ============================================================================
# Opus 配置常量
# ============================================================================

# Opus 支持的帧大小 (以采样点为单位，对应采样率)
# 对于 48kHz：2.5ms=120, 5ms=240, 10ms=480, 20ms=960, 40ms=1920, 60ms=2880
# 对于 24kHz：2.5ms=60, 5ms=120, 10ms=240, 20ms=480, 40ms=960, 60ms=1440
# 对于 16kHz：2.5ms=40, 5ms=80, 10ms=160, 20ms=320, 40ms=640, 60ms=960
OPUS_FRAME_DURATIONS_MS = [2.5, 5, 10, 20, 40, 60]

# 默认配置
DEFAULT_OPUS_SAMPLE_RATE = 48000  # Opus 内部采样率 (编码时会自动重采样)
DEFAULT_OPUS_CHANNELS = 1
DEFAULT_OPUS_APPLICATION = 'voip'  # 'voip', 'audio', 或 'restricted_lowdelay'
DEFAULT_OPUS_BITRATE = 32000  # 32 kbps，对于语音足够
DEFAULT_OPUS_FRAME_SIZE_MS = 20  # 每帧 20ms


@dataclass
class OpusFrameHeader:
    """
    Opus 帧头部 (4 字节)
    
    用于在二进制流中封装单个 Opus 帧:
      - frame_size: uint16 (2 bytes, Little Endian) - 帧数据大小（不含头部）
      - frame_duration_samples: uint16 (2 bytes, Little Endian) - 帧时长（采样点数）
    
    例如：对于 48kHz, 20ms 的帧，frame_duration_samples = 960
    """
    frame_size: int  # 帧数据大小（字节）
    frame_duration_samples: int  # 帧时长（采样点数）
    
    HEADER_SIZE = 4
    
    def pack(self) -> bytes:
        """打包头部为二进制数据"""
        return struct.pack("<HH", self.frame_size, self.frame_duration_samples)
    
    @classmethod
    def unpack(cls, data: bytes) -> Optional['OpusFrameHeader']:
        """从二进制数据解包头部"""
        if len(data) < cls.HEADER_SIZE:
            return None
        try:
            frame_size, frame_duration_samples = struct.unpack("<HH", data[:cls.HEADER_SIZE])
            return cls(frame_size=frame_size, frame_duration_samples=frame_duration_samples)
        except Exception as e:
            logger.error(f"Failed to unpack Opus frame header: {e}")
            return None


@dataclass
class OpusStreamHeader:
    """
    Opus 数据流头部 (8 字节)
    
    用于描述整个 Opus 数据流的参数:
      - magic: "OPUS" (4 bytes, ASCII)
      - sample_rate: uint16 (2 bytes, Little Endian) - 原始音频采样率 / 100
      - channels: uint8 (1 byte) - 通道数
      - frame_size_ms: uint8 (1 byte) - 每帧时长（毫秒）
    
    注意：sample_rate 以 100 为单位存储，例如 16000Hz 存储为 160
    """
    sample_rate: int  # 原始音频采样率 (Hz)
    channels: int  # 通道数
    frame_size_ms: int  # 每帧时长 (ms)
    
    HEADER_SIZE = 8
    MAGIC = b"OPUS"
    
    def pack(self) -> bytes:
        """打包头部为二进制数据"""
        sample_rate_encoded = self.sample_rate // 100
        return struct.pack(
            "<4sHBB",
            self.MAGIC,
            sample_rate_encoded,
            self.channels,
            self.frame_size_ms
        )
    
    @classmethod
    def unpack(cls, data: bytes) -> Optional['OpusStreamHeader']:
        """从二进制数据解包头部"""
        if len(data) < cls.HEADER_SIZE:
            return None
        try:
            magic, sample_rate_encoded, channels, frame_size_ms = struct.unpack(
                "<4sHBB", data[:cls.HEADER_SIZE]
            )
            if magic != cls.MAGIC:
                logger.warning(f"Invalid Opus stream magic: {magic}, expected {cls.MAGIC}")
                return None
            return cls(
                sample_rate=sample_rate_encoded * 100,
                channels=channels,
                frame_size_ms=frame_size_ms
            )
        except Exception as e:
            logger.error(f"Failed to unpack Opus stream header: {e}")
            return None


class OpusEncoder:
    """
    Opus 编码器
    
    将 PCM 音频数据编码为 Opus 格式
    
    注意：为了避免周期性静音问题，编码器会缓存不足一帧的残留数据，
    直到下一次编码时再处理。只有在调用 flush() 或 encode(..., flush=True) 时
    才会处理残留数据（零填充到完整帧）。
    """
    
    def __init__(
        self,
        sample_rate: int = 24000,
        channels: int = 1,
        application: str = DEFAULT_OPUS_APPLICATION,
        bitrate: int = DEFAULT_OPUS_BITRATE,
        frame_size_ms: int = DEFAULT_OPUS_FRAME_SIZE_MS
    ):
        """
        初始化 Opus 编码器
        
        Args:
            sample_rate: 输入音频采样率 (Hz)，支持 8000, 12000, 16000, 24000, 48000
            channels: 通道数 (1 或 2)
            application: 应用类型 ('voip', 'audio', 'restricted_lowdelay')
            bitrate: 目标比特率 (bps)
            frame_size_ms: 每帧时长 (ms)，支持 2.5, 5, 10, 20, 40, 60
        """
        if not OPUS_AVAILABLE:
            raise RuntimeError("opuslib is not available. Please install it with: pip install opuslib")
        
        self.sample_rate = sample_rate
        self.channels = channels
        self.application = application
        self.bitrate = bitrate
        self.frame_size_ms = frame_size_ms
        
        # 计算帧大小（采样点数）
        self.frame_size_samples = int(sample_rate * frame_size_ms / 1000)
        
        # 创建编码器
        app_map = {
            'voip': opuslib.APPLICATION_VOIP,
            'audio': opuslib.APPLICATION_AUDIO,
            'restricted_lowdelay': opuslib.APPLICATION_RESTRICTED_LOWDELAY
        }
        self._encoder = opuslib.Encoder(sample_rate, channels, app_map.get(application, opuslib.APPLICATION_VOIP))
        
        # 残留数据缓冲区 - 用于缓存不足一帧的数据
        self._residual_buffer: Optional[np.ndarray] = None
        
        # 设置比特率
        # opuslib 的 Encoder 没有直接设置 bitrate 的方法，需要通过 CTL 设置
        # 这里我们使用默认配置
        
        logger.info(
            f"Opus encoder initialized: sample_rate={sample_rate}, channels={channels}, "
            f"frame_size_ms={frame_size_ms}, frame_size_samples={self.frame_size_samples}"
        )
    
    def encode(self, pcm_data: np.ndarray, flush: bool = False) -> bytes:
        """
        将 PCM 数据编码为 Opus 流
        
        Args:
            pcm_data: PCM 音频数据，形状为 [N] 或 [channels, N]，dtype 为 int16 或 float32
            flush: 是否强制刷新残留缓冲区（在音频流结束时设为 True）
            
        Returns:
            编码后的 Opus 数据，包含流头部和帧数据
            
        注意：
            - 为避免周期性静音，不足一帧的数据会被缓存到下一次编码
            - 只有当 flush=True 时才会处理残留数据（零填充到完整帧）
            - 如果传入的数据量加上残留数据仍不足一帧，且 flush=False，将返回空的 Opus 流
        """
        # 确保数据是 1D 数组
        if pcm_data.ndim > 1:
            pcm_data = pcm_data.flatten()
        
        # 转换为 int16
        if pcm_data.dtype != np.int16:
            if np.issubdtype(pcm_data.dtype, np.floating):
                pcm_data = np.clip(pcm_data, -1.0, 1.0)
                pcm_data = (pcm_data * 32767).astype(np.int16)
            else:
                pcm_data = pcm_data.astype(np.int16)
        
        # 合并残留数据
        if self._residual_buffer is not None and len(self._residual_buffer) > 0:
            pcm_data = np.concatenate([self._residual_buffer, pcm_data])
            self._residual_buffer = None
        
        # 构建流头部
        stream_header = OpusStreamHeader(
            sample_rate=self.sample_rate,
            channels=self.channels,
            frame_size_ms=self.frame_size_ms
        )
        
        # 分帧编码
        encoded_frames = []
        total_samples = len(pcm_data)
        offset = 0
        
        while offset < total_samples:
            remaining = total_samples - offset
            
            if remaining < self.frame_size_samples:
                # 不足一帧
                if flush:
                    # 强制刷新：零填充到完整帧
                    frame_pcm = np.pad(pcm_data[offset:], (0, self.frame_size_samples - remaining))
                    encoded_data = self._encoder.encode(frame_pcm.tobytes(), self.frame_size_samples)
                    frame_header = OpusFrameHeader(
                        frame_size=len(encoded_data),
                        frame_duration_samples=self.frame_size_samples
                    )
                    encoded_frames.append(frame_header.pack() + encoded_data)
                    logger.debug(f"Flushed residual {remaining} samples with zero-padding")
                else:
                    # 不刷新：缓存残留数据
                    self._residual_buffer = pcm_data[offset:].copy()
                    logger.debug(f"Buffered {remaining} residual samples for next encode")
                break
            
            # 完整帧：直接编码
            frame_pcm = pcm_data[offset:offset + self.frame_size_samples]
            encoded_data = self._encoder.encode(frame_pcm.tobytes(), self.frame_size_samples)
            
            frame_header = OpusFrameHeader(
                frame_size=len(encoded_data),
                frame_duration_samples=self.frame_size_samples
            )
            
            encoded_frames.append(frame_header.pack() + encoded_data)
            offset += self.frame_size_samples
        
        # 组合流头部和帧数据
        result = stream_header.pack() + b"".join(encoded_frames)
        
        logger.debug(
            f"Opus encoded: {total_samples} samples -> {len(result)} bytes, "
            f"{len(encoded_frames)} frames, residual={len(self._residual_buffer) if self._residual_buffer is not None else 0}"
        )
        
        return result
    
    def flush(self) -> bytes:
        """
        刷新残留缓冲区，编码剩余的数据
        
        Returns:
            编码后的 Opus 数据（如果有残留数据），否则返回空流
        """
        if self._residual_buffer is None or len(self._residual_buffer) == 0:
            # 返回空的 Opus 流
            stream_header = OpusStreamHeader(
                sample_rate=self.sample_rate,
                channels=self.channels,
                frame_size_ms=self.frame_size_ms
            )
            return stream_header.pack()
        
        # 用空数组调用 encode 并强制刷新
        return self.encode(np.array([], dtype=np.int16), flush=True)
    
    def reset(self):
        """
        重置编码器状态，清空残留缓冲区
        
        在开始新的音频流时调用此方法
        """
        self._residual_buffer = None
        logger.debug("Opus encoder reset")
    
    def encode_frame(self, pcm_frame: np.ndarray) -> bytes:
        """
        编码单个 PCM 帧（不包含流头部）
        
        Args:
            pcm_frame: 单帧 PCM 数据，长度应为 frame_size_samples
            
        Returns:
            编码后的帧数据（包含帧头部）
        """
        # 转换为 int16
        if pcm_frame.dtype != np.int16:
            if np.issubdtype(pcm_frame.dtype, np.floating):
                pcm_frame = np.clip(pcm_frame, -1.0, 1.0)
                pcm_frame = (pcm_frame * 32767).astype(np.int16)
            else:
                pcm_frame = pcm_frame.astype(np.int16)
        
        # 确保帧大小正确
        if len(pcm_frame) < self.frame_size_samples:
            pcm_frame = np.pad(pcm_frame, (0, self.frame_size_samples - len(pcm_frame)))
        elif len(pcm_frame) > self.frame_size_samples:
            pcm_frame = pcm_frame[:self.frame_size_samples]
        
        # 编码
        encoded_data = self._encoder.encode(pcm_frame.tobytes(), self.frame_size_samples)
        
        # 构建帧头部
        frame_header = OpusFrameHeader(
            frame_size=len(encoded_data),
            frame_duration_samples=self.frame_size_samples
        )
        
        return frame_header.pack() + encoded_data


class OpusDecoder:
    """
    Opus 解码器
    
    将 Opus 格式数据解码为 PCM 音频
    """
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1
    ):
        """
        初始化 Opus 解码器
        
        Args:
            sample_rate: 输出音频采样率 (Hz)
            channels: 通道数 (1 或 2)
        """
        if not OPUS_AVAILABLE:
            raise RuntimeError("opuslib is not available. Please install it with: pip install opuslib")
        
        self.sample_rate = sample_rate
        self.channels = channels
        
        # 创建解码器
        self._decoder = opuslib.Decoder(sample_rate, channels)
        
        logger.info(f"Opus decoder initialized: sample_rate={sample_rate}, channels={channels}")
    
    def decode(self, opus_data: bytes) -> np.ndarray:
        """
        将 Opus 流解码为 PCM 数据
        
        Args:
            opus_data: 完整的 Opus 数据流（包含流头部和帧数据）
            
        Returns:
            解码后的 PCM 数据，dtype 为 int16
        """
        if len(opus_data) < OpusStreamHeader.HEADER_SIZE:
            raise ValueError(f"Opus data too short: {len(opus_data)} bytes")
        
        # 解析流头部
        stream_header = OpusStreamHeader.unpack(opus_data)
        if stream_header is None:
            raise ValueError("Failed to parse Opus stream header")
        
        # 如果需要，可以重新初始化解码器以匹配采样率
        # 但通常 Opus 解码器会自动处理采样率转换
        
        # 解析帧数据
        offset = OpusStreamHeader.HEADER_SIZE
        decoded_frames = []
        
        while offset < len(opus_data):
            # 解析帧头部
            frame_header = OpusFrameHeader.unpack(opus_data[offset:])
            if frame_header is None:
                logger.warning(f"Failed to parse Opus frame header at offset {offset}")
                break
            
            offset += OpusFrameHeader.HEADER_SIZE
            
            # 读取帧数据
            frame_data = opus_data[offset:offset + frame_header.frame_size]
            if len(frame_data) < frame_header.frame_size:
                logger.warning(f"Incomplete Opus frame: expected {frame_header.frame_size}, got {len(frame_data)}")
                break
            
            offset += frame_header.frame_size
            
            # 计算目标采样点数（可能因采样率不同而变化）
            target_samples = int(
                frame_header.frame_duration_samples * self.sample_rate / stream_header.sample_rate
            )
            
            # 解码
            pcm_bytes = self._decoder.decode(frame_data, target_samples)
            pcm_array = np.frombuffer(pcm_bytes, dtype=np.int16)
            decoded_frames.append(pcm_array)
        
        if not decoded_frames:
            return np.array([], dtype=np.int16)
        
        result = np.concatenate(decoded_frames)
        
        logger.debug(
            f"Opus decoded: {len(opus_data)} bytes -> {len(result)} samples, "
            f"{len(decoded_frames)} frames"
        )
        
        return result
    
    def decode_frame(self, frame_data: bytes, frame_duration_samples: int) -> np.ndarray:
        """
        解码单个 Opus 帧（不包含帧头部）
        
        Args:
            frame_data: 编码后的帧数据
            frame_duration_samples: 帧时长（采样点数）
            
        Returns:
            解码后的 PCM 数据，dtype 为 int16
        """
        pcm_bytes = self._decoder.decode(frame_data, frame_duration_samples)
        return np.frombuffer(pcm_bytes, dtype=np.int16)


# ============================================================================
# 便捷函数
# ============================================================================

def encode_pcm_to_opus(
    pcm_data: np.ndarray,
    sample_rate: int = 24000,
    channels: int = 1,
    bitrate: int = DEFAULT_OPUS_BITRATE,
    frame_size_ms: int = DEFAULT_OPUS_FRAME_SIZE_MS
) -> bytes:
    """
    便捷函数：将 PCM 数据编码为 Opus
    
    Args:
        pcm_data: PCM 音频数据
        sample_rate: 采样率
        channels: 通道数
        bitrate: 目标比特率
        frame_size_ms: 每帧时长
        
    Returns:
        编码后的 Opus 数据
    """
    encoder = OpusEncoder(
        sample_rate=sample_rate,
        channels=channels,
        bitrate=bitrate,
        frame_size_ms=frame_size_ms
    )
    return encoder.encode(pcm_data)


def decode_opus_to_pcm(
    opus_data: bytes,
    sample_rate: int = 16000,
    channels: int = 1
) -> np.ndarray:
    """
    便捷函数：将 Opus 数据解码为 PCM
    
    Args:
        opus_data: Opus 音频数据
        sample_rate: 输出采样率
        channels: 通道数
        
    Returns:
        解码后的 PCM 数据
    """
    decoder = OpusDecoder(sample_rate=sample_rate, channels=channels)
    return decoder.decode(opus_data)


def is_opus_available() -> bool:
    """检查 Opus 编解码器是否可用"""
    return OPUS_AVAILABLE
