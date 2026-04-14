"""
WebSocket 消息协议定义
定义所有 JSON 消息的 Pydantic 模型
"""
import time
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum
from loguru import logger


# ============================================================================
# 基础结构
# ============================================================================

class MessageType(str, Enum):
    """消息类型枚举"""
    # 输入端口 - 客户端消息
    INITIALIZE_AVATAR_SESSION = "InitializeAvatarSession"
    SEND_HUMAN_AUDIO = "SendHumanAudio"
    SEND_HUMAN_VIDEO = "SendHumanVideo"
    SEND_HUMAN_TEXT = "SendHumanText"
    TRIGGER_HEARTBEAT = "TriggerHeartbeat"
    INTERRUPT = "Interrupt"
    
    # 输入端口 - 服务器消息
    AVATAR_SESSION_INITIALIZED = "AvatarSessionInitialized"
    ECHO_HUMAN_TEXT = "EchoHumanText"
    ECHO_AVATAR_TEXT = "EchoAvatarText"
    ECHO_AVATAR_AUDIO = "EchoAvatarAudio"
    AVATAR_HEARTBEAT = "AvatarHeartbeat"
    INTERRUPT_ACCEPTED = "InterruptAccepted"
    INTERRUPT_NOTIFICATION = "InterruptNotification"  # Server-initiated interrupt (for non-MotionData mode)
    CHAT_SIGNAL = "ChatSignal"
    ERROR = "Error"
    
    # 输出端口 - 服务器消息
    MOTION_DATA = "MotionData"
    MOTION_DATA_WELCOME = "MotionDataWelcome"
    
    # 输入端口 - 渲染器消息
    END_SPEECH = "EndSpeech"

class MessageHeader(BaseModel):
    """消息头部"""
    name: MessageType
    request_id: str = Field(..., description="请求ID")


class BaseMessage(BaseModel):
    """基础消息结构"""
    header: MessageHeader
    payload: Optional[Dict[str, Any]] = Field(default=None)


# ============================================================================
# 输入端口 - 客户端 → 服务器消息
# ============================================================================

class AudioFormat(str, Enum):
    """音频格式枚举"""
    PCM = "PCM"
    OPUS = "OPUS"


class AudioConfig(BaseModel):
    """音频配置"""
    format: str = Field(default="PCM", description="音频格式: PCM 或 OPUS")
    sample_rate: int = Field(default=16000, description="采样率")
    channels: int = Field(default=1, description="通道数")
    
    # Opus 特有配置
    opus_frame_size_ms: Optional[int] = Field(
        default=20, 
        description="Opus 每帧时长(毫秒)，仅当 format=OPUS 时有效"
    )


class InitializeAvatarSessionPayload(BaseModel):
    """初始化会话载荷"""
    audio: AudioConfig
    subscriptions: Optional[List[str]] = Field(default=None, description="需要订阅的下行内容列表")


class InitializeAvatarSession(BaseModel):
    """初始化数字人会话"""
    header: MessageHeader
    payload: InitializeAvatarSessionPayload


class BinaryDataInfo(BaseModel):
    """二进制数据信息"""
    binary_size: int = Field(..., description="二进制数据总大小")
    segment_num: int = Field(..., description="分段数量")


class SendHumanAudioPayload(BaseModel):
    """发送音频数据载荷"""
    transport: str = Field(default="binary", description="传输方式: binary/base64")
    binary_size: Optional[int] = Field(default=None, description="binary 模式下的二进制总大小")
    segment_num: Optional[int] = Field(default=None, description="binary 模式下的二进制帧数量")
    data_base64: Optional[str] = Field(default=None, description="base64 数据")
    
    # 音频格式相关（用于运行时覆盖会话配置）
    format: Optional[str] = Field(default=None, description="音频格式: PCM 或 OPUS，不指定则使用会话配置")


class SendHumanAudio(BaseModel):
    """发送用户音频数据"""
    header: MessageHeader
    payload: SendHumanAudioPayload


class SendHumanVideoPayload(BaseModel):
    """发送视频数据载荷"""
    width: int = Field(..., description="视频宽度")
    height: int = Field(..., description="视频高度")
    format: str = Field(default="JPEG", description="视频格式")
    transport: str = Field(default="binary", description="传输方式: binary/base64")
    binary_size: Optional[int] = Field(default=None, description="binary 模式下的二进制总大小")
    segment_num: Optional[int] = Field(default=None, description="binary 模式下的二进制帧数量")
    data_base64: Optional[str] = Field(default=None, description="base64 数据")


class SendHumanVideo(BaseModel):
    """发送用户视频数据"""
    header: MessageHeader
    payload: SendHumanVideoPayload


class SendHumanTextPayload(BaseModel):
    """发送文本数据载荷"""
    stream_key: str = Field(..., description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    mode: str = Field(default="increment", description="文本模式: increment/full_text")
    text: str = Field(..., description="文本内容")
    end_of_speech: bool = Field(..., description="是否结束")


class SendHumanText(BaseModel):
    """发送用户文本数据"""
    header: MessageHeader
    payload: SendHumanTextPayload


class TriggerHeartbeat(BaseModel):
    """触发心跳"""
    header: MessageHeader


class Interrupt(BaseModel):
    """打断信号"""
    header: MessageHeader


# ============================================================================
# 输入端口 - 服务器 → 客户端消息
# ============================================================================

class AvatarSessionInitialized(BaseModel):
    """会话初始化完成"""
    header: MessageHeader


class EchoTextPayload(BaseModel):
    """文本回显载荷"""
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    mode: str = Field(default="increment", description="文本模式: increment/full_text")
    text: str = Field(..., description="文本内容")
    end_of_speech: bool = Field(..., description="是否结束")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="附加元数据，包含 handler 添加的自定义信息（如 task_id）"
    )


class EchoHumanText(BaseModel):
    """回显用户文本(ASR结果)"""
    header: MessageHeader
    payload: EchoTextPayload


class EchoAvatarText(BaseModel):
    """回显数字人文本(LLM结果)"""
    header: MessageHeader
    payload: EchoTextPayload


class EchoAvatarAudioPayload(BaseModel):
    """回显数字人音频载荷"""
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    transport: str = Field(default="binary", description="传输方式: binary/base64")
    binary_size: Optional[int] = Field(default=None, description="binary 模式下的二进制总大小")
    segment_num: Optional[int] = Field(default=None, description="binary 模式下的二进制帧数量")
    format: str = Field(default="PCM", description="音频格式: PCM 或 OPUS")
    sample_rate: int = Field(default=24000, description="音频采样率")
    channels: int = Field(default=1, description="音频通道数")
    data_base64: Optional[str] = Field(default=None, description="base64 数据")
    end_of_speech: bool = Field(default=False, description="本段音频是否结束")
    
    # Opus 特有字段
    opus_frame_size_ms: Optional[int] = Field(
        default=None, 
        description="Opus 每帧时长(毫秒)，仅当 format=OPUS 时有效"
    )
    
    # 扩展元数据（如 task_id 等）
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="附加元数据，包含 handler 添加的自定义信息（如 task_id）"
    )


class EchoAvatarAudio(BaseModel):
    """回显数字人音频(TTS结果)"""
    header: MessageHeader
    payload: EchoAvatarAudioPayload


class AvatarHeartbeat(BaseModel):
    """心跳响应"""
    header: MessageHeader


class InterruptAcceptedPayload(BaseModel):
    """打断已接受载荷"""
    target_stream_id: Optional[str] = Field(default=None, description="被打断的 AVATAR_AUDIO stream ID")
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")


class InterruptAccepted(BaseModel):
    """打断已接受"""
    header: MessageHeader
    payload: Optional[InterruptAcceptedPayload] = Field(default=None)


class InterruptNotificationPayload(BaseModel):
    """服务端打断通知载荷（用于无 Motion Data 场景）"""
    target_stream_id: str = Field(..., description="被打断的 AVATAR_AUDIO stream ID (deprecated: 使用 stream_key 替代)")
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    reason: str = Field(default="user_interrupt", description="打断原因: user_interrupt | semantic_interrupt")
    interrupted_at: float = Field(default_factory=time.time, description="打断时间戳")


class InterruptNotification(BaseModel):
    """服务端打断通知（用于无 Motion Data 场景）"""
    header: MessageHeader
    payload: InterruptNotificationPayload


class ChatSignalPayload(BaseModel):
    timestamp: float = Field(default_factory=time.time)
    type: str
    source_type: str
    stream_type: Optional[str] = Field(default=None, description="流类型")
    stream_producer: Optional[str] = Field(default=None, description="流来源")
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    parent_stream_keys: Optional[List[str]] = Field(default=None, description="父级流的 stream_key 列表（仅 STREAM_BEGIN 信号包含，包含所有直接父级，不包含祖父级）")
    signal_data: Optional[Dict] = Field(default=None, description="信号数据")


class ChatSignalMessage(BaseModel):
    """监听到的信号"""
    header: MessageHeader
    payload: ChatSignalPayload



class ErrorCode(str, Enum):
    """错误码"""
    INVALID_SESSION = "INVALID_SESSION"
    AUDIO_FORMAT_ERROR = "AUDIO_FORMAT_ERROR"
    VIDEO_FORMAT_ERROR = "VIDEO_FORMAT_ERROR"
    HEARTBEAT_TIMEOUT = "HEARTBEAT_TIMEOUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    RATE_LIMIT = "RATE_LIMIT"
    INVALID_MESSAGE = "INVALID_MESSAGE"
    BINARY_DATA_ERROR = "BINARY_DATA_ERROR"


class ErrorPayload(BaseModel):
    """错误载荷"""
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")


class Error(BaseModel):
    """错误消息"""
    header: MessageHeader
    payload: ErrorPayload


# ============================================================================
# 输出端口 - 服务器 → 渲染器消息
# ============================================================================

class MotionDataPayload(BaseModel):
    """Motion Data 载荷"""
    stream_key: Optional[str] = Field(default=None, description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")
    motion_data: BinaryDataInfo
    end_of_speech: bool = Field(..., description="是否结束")


class MotionDataMessage(BaseModel):
    """Motion Data 消息"""
    header: MessageHeader
    payload: MotionDataPayload


# ============================================================================
# 输入端口 - 渲染器 → 服务器消息
# ============================================================================

class EndSpeechPayload(BaseModel):
    """EndSpeech 载荷"""
    stream_key: str = Field(..., description="流的唯一标识，格式为 stream_{builder_id}_{stream_id}")


class EndSpeech(BaseModel):
    """渲染端播放完毕"""
    header: MessageHeader
    payload: EndSpeechPayload


# ============================================================================
# 工具函数
# ============================================================================

def parse_message(json_data: dict) -> Optional[BaseMessage]:
    """
    解析 JSON 消息
    
    Args:
        json_data: JSON 字典
        
    Returns:
        解析后的消息对象,如果解析失败返回 None
    """
    try:
        if "header" not in json_data:
            logger.warning("JSON消息缺少header字段")
            return None
        
        message_name = json_data["header"].get("name")
        if not message_name:
            logger.warning("JSON消息header中缺少name字段")
            return None
        
        # 直接通过枚举查找消息类型
        try:
            message_type = MessageType(message_name)
        except ValueError:
            logger.warning(f"未知的消息类型: {message_name}")
            return None
        
        # 根据消息类型直接获取对应的类
        message_class_map = {
            MessageType.INITIALIZE_AVATAR_SESSION: InitializeAvatarSession,
            MessageType.SEND_HUMAN_AUDIO: SendHumanAudio,
            MessageType.SEND_HUMAN_VIDEO: SendHumanVideo,
            MessageType.SEND_HUMAN_TEXT: SendHumanText,
            MessageType.TRIGGER_HEARTBEAT: TriggerHeartbeat,
            MessageType.INTERRUPT: Interrupt,
            MessageType.AVATAR_SESSION_INITIALIZED: AvatarSessionInitialized,
            MessageType.ECHO_HUMAN_TEXT: EchoHumanText,
            MessageType.ECHO_AVATAR_TEXT: EchoAvatarText,
            MessageType.ECHO_AVATAR_AUDIO: EchoAvatarAudio,
            MessageType.AVATAR_HEARTBEAT: AvatarHeartbeat,
            MessageType.INTERRUPT_ACCEPTED: InterruptAccepted,
            MessageType.ERROR: Error,
            MessageType.MOTION_DATA: MotionDataMessage,
            MessageType.MOTION_DATA_WELCOME: MotionDataMessage,
            MessageType.END_SPEECH: EndSpeech,
        }
        
        message_class = message_class_map.get(message_type)
        if message_class is None:
            logger.error(f"消息类型 {message_type} 没有对应的处理类")
            return None
        
        return message_class.model_validate(json_data)
    except Exception as e:
        logger.error(f"解析JSON消息时发生异常: {e}", exc_info=True)
        return None


def serialize_message(message: BaseMessage) -> dict:
    """
    序列化消息为 JSON 字典
    
    Args:
        message: 消息对象
        
    Returns:
        JSON 字典
    """
    return message.model_dump(exclude_none=True)

