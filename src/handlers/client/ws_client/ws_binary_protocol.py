"""
WebSocket 二进制协议处理
处理二进制数据的打包和解包
"""
import struct
from typing import Optional, List, Tuple
from dataclasses import dataclass
from loguru import logger


# ============================================================================
# 二进制包头部结构
# ============================================================================

@dataclass
class BinaryPacketHeader:
    """
    二进制包头部 (36 字节)
    
    Header (36 bytes):
      - Magic: "JBIN" (4 bytes)
      - Request Id: "xxx" (8 bytes, request_id的前8个字符)
      - Packet Type: 0 (4 bytes, 0=audio, 1=video)
      - Packet Index: 0 (4 bytes, 当前包索引)
      - Total Packets: 2 (4 bytes, 总包数)
      - Data Size: 20000 (4 bytes, 当前包数据大小)
      - Reserved: 0 (8 bytes, 保留字段)
    """
    magic: bytes  # 4 bytes: b"JBIN"
    request_id: str  # 8 bytes: request_id 前8个字符
    packet_type: int  # 4 bytes: 0=audio, 1=video
    packet_index: int  # 4 bytes: 当前包索引
    total_packets: int  # 4 bytes: 总包数
    data_size: int  # 4 bytes: 当前包数据大小
    reserved: int  # 8 bytes: 保留字段
    
    HEADER_SIZE = 36
    MAGIC = b"JBIN"
    
    @classmethod
    def parse(cls, data: bytes) -> Optional['BinaryPacketHeader']:
        """
        解析二进制包头部
        
        Args:
            data: 至少36字节的数据
            
        Returns:
            解析后的头部对象,如果解析失败返回 None
        """
        if len(data) < cls.HEADER_SIZE:
            return None
        
        try:
            # 解包: 4s(magic) + 8s(request_id) + 4I(4个uint32) + Q(uint64)
            unpacked = struct.unpack("<4s8s4IQ", data[:cls.HEADER_SIZE])
            
            magic = unpacked[0]
            if magic != cls.MAGIC:
                logger.warning(f"Invalid magic: {magic}, expected {cls.MAGIC}")
                return None
            
            request_id = unpacked[1].decode('utf-8', errors='ignore').rstrip('\x00')
            packet_type = unpacked[2]
            packet_index = unpacked[3]
            total_packets = unpacked[4]
            data_size = unpacked[5]
            reserved = unpacked[6]
            
            return cls(
                magic=magic,
                request_id=request_id,
                packet_type=packet_type,
                packet_index=packet_index,
                total_packets=total_packets,
                data_size=data_size,
                reserved=reserved
            )
        except Exception as e:
            logger.error(f"Failed to parse binary packet header: {e}")
            return None
    
    def pack(self) -> bytes:
        """
        打包头部为二进制数据
        
        Returns:
            36字节的二进制数据
        """
        # 确保 request_id 是8字节
        request_id_bytes = self.request_id[:8].encode('utf-8')
        request_id_bytes = request_id_bytes.ljust(8, b'\x00')
        
        return struct.pack(
            "<4s8s4IQ",
            self.magic,
            request_id_bytes,
            self.packet_type,
            self.packet_index,
            self.total_packets,
            self.data_size,
            self.reserved
        )


# ============================================================================
# 二进制包组装器 (用于接收分段数据)
# ============================================================================

@dataclass
class StreamAssemblyState:
    """Human音/视频二进制流组装状态"""
    request_id: str
    expected_segments: int
    expected_size: int
    metadata: Optional[object] = None
    received_segments: int = 0
    received_size: int = 0
    chunks: List[bytes] = None
    
    def __post_init__(self):
        if self.chunks is None:
            self.chunks = []
    
    def append(self, chunk: bytes) -> Optional[bytes]:
        """追加一个分段,若完成则返回完整数据"""
        self.chunks.append(chunk)
        self.received_segments += 1
        self.received_size += len(chunk)
        
        if self.received_segments >= self.expected_segments or self.received_size >= self.expected_size:
            data = b"".join(self.chunks)
            if self.expected_size and self.expected_size != len(data):
                logger.warning(
                    f"Binary data size mismatch for request_id={self.request_id}: "
                    f"expected={self.expected_size}, actual={len(data)}"
                )
            return data
        return None


class BinaryStreamAssembler:
    """
    二进制流组装器
    按注册顺序组装 header-less 二进制分段 (用于基础音/视频上传)
    """
    
    def __init__(self):
        from collections import deque
        self._queue = deque()  # type: ignore[var-annotated]
    
    def register(self, request_id: str, expected_segments: int, expected_size: int,
                 metadata: Optional[object] = None) -> StreamAssemblyState:
        state = StreamAssemblyState(
            request_id=request_id,
            expected_segments=expected_segments,
            expected_size=expected_size,
            metadata=metadata or {}
        )
        self._queue.append(state)
        return state
    
    def append(self, chunk: bytes) -> Optional[Tuple[StreamAssemblyState, bytes]]:
        if not self._queue:
            logger.warning("Received unexpected binary chunk with no pending registrations")
            return None
        
        state = self._queue[0]
        data = state.append(chunk)
        if data is not None:
            self._queue.popleft()
            return state, data
        return None
    
    def clear(self):
        self._queue.clear()


# ============================================================================
# 二进制包拆分器 (用于发送大数据)
# ============================================================================

class BinaryPacketSplitter:
    """
    二进制包拆分器
    将大数据拆分为固定大小的分段
    """
    
    # Motion Data 输出分段大小: 16KB
    MOTION_DATA_SEGMENT_SIZE = 16 * 1024
    
    @staticmethod
    def split(request_id: str, packet_type: int, data: bytes, 
              segment_size: int = MOTION_DATA_SEGMENT_SIZE) -> List[bytes]:
        """
        拆分数据为多个分段
        
        Args:
            request_id: 请求ID
            packet_type: 数据类型 (0=audio, 1=video)
            data: 要拆分的数据
            segment_size: 每个分段的大小(不包含头部)
            
        Returns:
            分段列表,每个分段包含头部和数据
        """
        if len(data) == 0:
            # 空数据,返回一个空包
            # header = BinaryPacketHeader(
            #     magic=BinaryPacketHeader.MAGIC,
            #     request_id=request_id,
            #     packet_type=packet_type,
            #     packet_index=0,
            #     total_packets=1,
            #     data_size=0,
            #     reserved=0
            # )
            return [b""]
        
        # 计算总分段数
        total_packets = (len(data) + segment_size - 1) // segment_size
        
        packets = []
        for i in range(total_packets):
            start = i * segment_size
            end = min(start + segment_size, len(data))
            segment_data = data[start:end]
            
            # header = BinaryPacketHeader(
            #     magic=BinaryPacketHeader.MAGIC,
            #     request_id=request_id,
            #     packet_type=packet_type,
            #     packet_index=i,
            #     total_packets=total_packets,
            #     data_size=len(segment_data),
            #     reserved=0
            # )
            
            packet = segment_data
            packets.append(packet)
        
        return packets

