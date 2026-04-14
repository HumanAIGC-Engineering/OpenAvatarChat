"""
Agent 系统共享数据模型

定义 Perception 和 ChatAgent 之间传递的数据结构
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional


# ===== 分层视觉上下文 =====

@dataclass
class UserState:
    """细粒度：用户状态"""
    emotion: str = ""           # focused, happy, confused, sad, angry, surprised, neutral
    gaze: str = ""              # screen, away, camera, down
    posture: str = ""           # sitting, standing, leaning, lying
    action: str = ""            # typing, speaking, idle, reading, writing, gesturing
    
    def to_dict(self) -> Dict:
        return {
            "emotion": self.emotion,
            "gaze": self.gaze,
            "posture": self.posture,
            "action": self.action,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "UserState":
        return cls(
            emotion=data.get("emotion", ""),
            gaze=data.get("gaze", ""),
            posture=data.get("posture", ""),
            action=data.get("action", ""),
        )
    
    def to_text(self) -> str:
        """转换为文本描述，用于注入到 prompt"""
        parts = []
        if self.emotion:
            parts.append(f"情绪: {self.emotion}")
        if self.gaze:
            parts.append(f"视线: {self.gaze}")
        if self.posture:
            parts.append(f"姿态: {self.posture}")
        if self.action:
            parts.append(f"动作: {self.action}")
        return ", ".join(parts) if parts else "未知"


@dataclass
class SceneStructure:
    """中粒度：结构化场景信息"""
    location: str = ""                                      # 办公室, 会议室, 家, 户外
    people: List[str] = field(default_factory=list)         # 检测到的人物列表
    objects: List[str] = field(default_factory=list)        # 关键物品列表
    activities: List[str] = field(default_factory=list)     # 正在进行的活动
    
    def to_dict(self) -> Dict:
        return {
            "location": self.location,
            "people": self.people,
            "objects": self.objects,
            "activities": self.activities,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "SceneStructure":
        return cls(
            location=data.get("location", ""),
            people=data.get("people", []),
            objects=data.get("objects", []),
            activities=data.get("activities", []),
        )
    
    def to_text(self) -> str:
        """转换为文本描述"""
        parts = []
        if self.location:
            parts.append(f"地点: {self.location}")
        if self.people:
            parts.append(f"人物: {', '.join(self.people)}")
        if self.objects:
            parts.append(f"物品: {', '.join(self.objects)}")
        if self.activities:
            parts.append(f"活动: {', '.join(self.activities)}")
        return "; ".join(parts) if parts else "未知场景"


@dataclass
class DetectedEvent:
    """
    检测到的交互事件
    
    由视觉模型在分析视频帧时检测，用于触发主动交互
    """
    event_type: str = ""        # waving, leaving, arriving, showing_object, asking_for_attention
    confidence: float = 0.0     # 置信度 0.0-1.0
    description: str = ""       # 事件描述
    
    # 事件类型常量
    WAVING = "waving"                       # 挥手打招呼
    LEAVING = "leaving"                     # 离开画面
    ARRIVING = "arriving"                   # 进入画面
    SHOWING_OBJECT = "showing_object"       # 展示物品
    ASKING_FOR_ATTENTION = "asking_for_attention"  # 寻求注意
    
    # 置信度阈值
    MIN_CONFIDENCE = 0.7
    
    def to_dict(self) -> Dict:
        return {
            "event_type": self.event_type,
            "confidence": self.confidence,
            "description": self.description,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "DetectedEvent":
        return cls(
            event_type=data.get("event_type", ""),
            confidence=data.get("confidence", 0.0),
            description=data.get("description", ""),
        )
    
    def is_valid(self) -> bool:
        """检查事件是否有效（置信度足够高）"""
        return self.confidence >= self.MIN_CONFIDENCE and self.event_type != ""
    
    def should_trigger_response(self) -> bool:
        """判断是否应该触发主动响应"""
        if not self.is_valid():
            return False
        # 这些事件类型应该触发主动响应
        trigger_types = {self.WAVING, self.SHOWING_OBJECT, self.ASKING_FOR_ATTENTION}
        return self.event_type in trigger_types


@dataclass
class PerceptionData:
    """
    分层视觉上下文
    
    由 PerceptionHandler 生成，传递给 ChatAgentHandler
    """
    # 粗粒度：一句话场景描述
    scene_summary: str = ""
    # 中粒度：结构化信息
    scene_structure: SceneStructure = field(default_factory=SceneStructure)
    # 细粒度：用户状态
    user_state: UserState = field(default_factory=UserState)
    # 检测到的交互事件
    detected_events: List["DetectedEvent"] = field(default_factory=list)
    # 时间戳
    timestamp: float = 0.0
    
    def to_dict(self) -> Dict:
        return {
            "scene_summary": self.scene_summary,
            "scene_structure": self.scene_structure.to_dict(),
            "user_state": self.user_state.to_dict(),
            "detected_events": [e.to_dict() for e in self.detected_events],
            "timestamp": self.timestamp,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "PerceptionData":
        detected_events = [
            DetectedEvent.from_dict(e) for e in data.get("detected_events", [])
        ]
        return cls(
            scene_summary=data.get("scene_summary", ""),
            scene_structure=SceneStructure.from_dict(data.get("scene_structure", {})),
            user_state=UserState.from_dict(data.get("user_state", {})),
            detected_events=detected_events,
            timestamp=data.get("timestamp", 0.0),
        )
    
    def get_context_by_granularity(self, granularity: str = "coarse") -> str:
        """
        根据粒度获取上下文文本
        
        Args:
            granularity: "coarse" (粗粒度), "medium" (中粒度), "fine" (细粒度), "all" (全部)
        """
        if granularity == "coarse":
            return self.scene_summary
        elif granularity == "medium":
            return f"{self.scene_summary}\n{self.scene_structure.to_text()}"
        elif granularity == "fine":
            return f"{self.scene_summary}\n{self.scene_structure.to_text()}\n用户状态: {self.user_state.to_text()}"
        else:  # "all"
            return self.get_context_by_granularity("fine")
    
    def get_triggerable_events(self) -> List["DetectedEvent"]:
        """获取应该触发响应的事件"""
        return [e for e in self.detected_events if e.should_trigger_response()]
    
    def has_triggerable_events(self) -> bool:
        """是否有应该触发响应的事件"""
        return len(self.get_triggerable_events()) > 0


# ===== 环境事件 =====

@dataclass
class EnvironmentEvent:
    """
    环境事件
    
    由 PerceptionHandler 检测并通过 ChatDataType.ENVIRONMENT_EVENT 发送给 ChatAgentHandler
    """
    event_type: str = ""                    # waving, leaving, arriving, showing_object, asking_for_attention
    description: str = ""                   # 事件的详细描述
    confidence: float = 0.0                 # 置信度 0.0-1.0
    urgency: str = "low"                    # critical (立即响应), high (优先处理), low (可延迟)
    timestamp: float = 0.0
    
    # 可选的额外数据
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "event_type": self.event_type,
            "description": self.description,
            "confidence": self.confidence,
            "urgency": self.urgency,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EnvironmentEvent":
        return cls(
            event_type=data.get("event_type", ""),
            description=data.get("description", ""),
            confidence=data.get("confidence", 0.0),
            urgency=data.get("urgency", "low"),
            timestamp=data.get("timestamp", 0.0),
            metadata=data.get("metadata", {}),
        )
    
    @classmethod
    def from_detected_event(cls, detected: "DetectedEvent", urgency: str = "high") -> "EnvironmentEvent":
        """从 DetectedEvent 创建 EnvironmentEvent"""
        import time
        return cls(
            event_type=detected.event_type,
            description=detected.description,
            confidence=detected.confidence,
            urgency=urgency,
            timestamp=time.time(),
        )
    
    def should_interrupt(self) -> bool:
        """判断是否应该中断当前对话"""
        return self.urgency == "critical"
    
    def should_respond_immediately(self) -> bool:
        """判断是否应该立即响应"""
        return self.urgency in ("critical", "high")

