"""
VAD/EOU 分析工具的数据模型

分析目标：
1. EOU 的核心作用是"守门员"——防止用户边思考边说时被 VAD 误截断
2. Early VAD 的目的是快速检测用户真正说完时，尽早开始问答
3. 需要评估的是：
   - EOU 是否正确阻止了过早截断（真阴性）
   - EOU 是否正确加速了短句响应（真阳性）
   - EOU 是否错误截断了未完成的语句（假阳性）
   - EOU 是否漏掉了本应加速的短句（假阴性）
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class VADEvent:
    """VAD 事件"""
    timestamp_ms: float              # 相对时间戳（毫秒）
    event_type: str                  # "speech_start", "early_vad_end", "speech_end", "data"
    sample_id: Optional[int] = None  # 样本 ID
    extra_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EOUEvent:
    """EOU 事件"""
    timestamp_ms: float              # 相对时间戳（毫秒）
    event_type: str                  # "prediction", "signal_sent"
    prediction: Optional[int] = None # 0=Incomplete, 1=Complete
    probability: Optional[float] = None
    buffer_duration_ms: Optional[float] = None


@dataclass
class ASREvent:
    """ASR 事件"""
    timestamp_ms: float              # 相对时间戳（毫秒）
    event_type: str                  # "started", "completed"
    text: Optional[str] = None
    stream_key: Optional[str] = None
    source: Optional[str] = None     # ASR handler 名称


@dataclass 
class UtteranceAnalysis:
    """单次语句的完整分析"""
    utterance_id: int
    stream_key: str
    vad_events: List[VADEvent] = field(default_factory=list)
    eou_events: List[EOUEvent] = field(default_factory=list)
    asr_events: List[ASREvent] = field(default_factory=list)
    
    # 时间点（毫秒）
    speech_start_ms: Optional[float] = None
    early_vad_end_ms: Optional[float] = None
    speech_end_ms: Optional[float] = None
    asr_completed_ms: Optional[float] = None
    
    # 识别文本
    asr_text: Optional[str] = None
    
    # 计算指标（毫秒）
    speech_duration_ms: Optional[float] = None    # 语音持续时间
    early_to_end_delay_ms: Optional[float] = None  # 从 early_vad_end 到 speech_end 的时间（用户继续说话的时长）
    eou_decision_time_ms: Optional[float] = None  # EOU 决策时间（从 early_vad_end 到发送信号）
    total_latency_ms: Optional[float] = None      # VAD→ASR 延迟（从 speech_end 到 ASR 完成，含网络往返）
    
    # EOU 效果
    eou_triggered: bool = False        # EOU 是否触发（发送了 signal）
    eou_effective: bool = False        # EOU 是否生效（提前结束了语音）
    eou_prediction_count: int = 0      # EOU 预测次数
    eou_final_probability: Optional[float] = None  # 最终预测置信度
    
    # 语句分类
    utterance_type: str = "unknown"    # "short_complete", "long_thinking", "incomplete"
    is_sentence_complete: bool = False  # 句子是否完整
    
    # EOU 效果分类
    eou_result_type: str = "unknown"   # "accelerated", "protected", "missed", "false_trigger", "reconnected", "normal"
    time_saved_ms: Optional[float] = None  # EOU 节省的时间（如果触发）
    
    # 重连相关
    was_reconnected: bool = False      # 该语句是否触发了重连（EOU 误判被自动修正）
    cancelled_stream_key: Optional[str] = None  # 被取消的 stream key
    reconnect_time_gap_ms: Optional[float] = None  # 重连时的时间间隔（毫秒）
    
    def calculate_metrics(self):
        """计算指标"""
        # 语音持续时间
        if self.speech_start_ms is not None and self.speech_end_ms is not None:
            self.speech_duration_ms = self.speech_end_ms - self.speech_start_ms
        
        # 从 early_vad_end 到 speech_end 的时间
        if self.early_vad_end_ms is not None and self.speech_end_ms is not None:
            self.early_to_end_delay_ms = self.speech_end_ms - self.early_vad_end_ms
        
        # EOU 决策时间
        signal_events = [e for e in self.eou_events if e.event_type == "signal_sent"]
        if signal_events and self.early_vad_end_ms is not None:
            self.eou_decision_time_ms = signal_events[0].timestamp_ms - self.early_vad_end_ms
        
        # 总延迟
        if self.speech_end_ms is not None and self.asr_completed_ms is not None:
            self.total_latency_ms = self.asr_completed_ms - self.speech_end_ms
        
        # EOU 统计
        self.eou_prediction_count = len([e for e in self.eou_events if e.event_type == "prediction"])
        prediction_events = [e for e in self.eou_events if e.event_type == "signal_sent" and e.probability is not None]
        if prediction_events:
            self.eou_final_probability = prediction_events[-1].probability
        
        # 分析句子完整性
        self._analyze_sentence_completeness()
        
        # 分类语句类型
        self._classify_utterance_type()
        
        # 分类 EOU 效果
        self._classify_eou_result()
    
    def _analyze_sentence_completeness(self):
        """分析句子是否完整"""
        if not self.asr_text:
            self.is_sentence_complete = False
            return
        
        text = self.asr_text.strip()
        
        # 检查是否以完整的句末标点结尾
        complete_endings = ['.', '!', '?', '。', '！', '？']
        incomplete_endings = [',', '，', '、', '...', '…', 'and', 'or', 'but', 'that', 'the', 'a', 'an']
        
        # 以句号、问号、感叹号结尾的认为是完整的
        if any(text.endswith(e) for e in complete_endings):
            # 但如果内容很短且以逗号结尾的词后面接句号，可能是不完整的
            self.is_sentence_complete = True
        elif any(text.lower().rstrip('.,!? ').endswith(e) for e in incomplete_endings):
            self.is_sentence_complete = False
        else:
            # 其他情况根据文本长度判断
            self.is_sentence_complete = len(text.split()) <= 5  # 短语可能是完整的
    
    def _classify_utterance_type(self):
        """分类语句类型"""
        if self.speech_duration_ms is None:
            self.utterance_type = "unknown"
            return
        
        # 短句：小于 2 秒
        if self.speech_duration_ms < 2000:
            if self.is_sentence_complete:
                self.utterance_type = "short_complete"  # 短且完整，如 "Okay.", "No."
            else:
                self.utterance_type = "short_incomplete"  # 短但不完整
        else:
            # 长句：大于 2 秒
            if self.is_sentence_complete:
                self.utterance_type = "long_complete"  # 长句且完整
            else:
                self.utterance_type = "long_thinking"  # 长句，可能是边思考边说
    
    def _classify_eou_result(self):
        """
        分类 EOU 效果：
        - accelerated: EOU 触发且正确加速了响应（短句/完整句）✓
        - protected: EOU 未触发，正确保护了长语句不被截断 ✓
        - missed: EOU 应该触发但没触发（短句但等了太久）
        - false_trigger: EOU 不应触发但触发了（可能截断了未完成的句子）
        - reconnected: EOU 误判被重连机制自动修正 ✓
        - normal: 正常 VAD 结束，无 EOU 参与
        """
        # 如果触发了重连，优先分类为 reconnected
        if self.was_reconnected:
            self.eou_result_type = "reconnected"
            return
        
        if self.eou_triggered:
            # EOU 触发了
            if self.is_sentence_complete:
                self.eou_result_type = "accelerated"
                # 计算节省的时间：假设没有 EOU 会等待完整的 end_delay
                if self.early_to_end_delay_ms is not None:
                    self.time_saved_ms = max(0, 2000 - self.early_to_end_delay_ms)  # 假设默认等待 2 秒
            else:
                # 触发但句子不完整，可能是误触发
                self.eou_result_type = "false_trigger"
        else:
            # EOU 没触发
            if self.utterance_type == "short_complete":
                # 短句但 EOU 没触发，可能漏掉了
                self.eou_result_type = "missed"
            elif self.utterance_type in ["long_thinking", "long_complete"]:
                # 长句 EOU 没触发，这是正确的保护行为
                self.eou_result_type = "protected"
            else:
                self.eou_result_type = "normal"


@dataclass
class SessionAnalysis:
    """Session 级别的分析结果"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    utterances: List[UtteranceAnalysis] = field(default_factory=list)
    
    # 配置信息
    config: Dict[str, Any] = field(default_factory=dict)
    
    # 汇总统计
    total_utterances: int = 0
    avg_speech_duration_ms: Optional[float] = None
    avg_early_to_end_delay_ms: Optional[float] = None
    avg_eou_decision_time_ms: Optional[float] = None
    avg_total_latency_ms: Optional[float] = None
    
    # EOU 效果统计
    eou_trigger_rate: Optional[float] = None
    accelerated_count: int = 0       # EOU 正确加速的数量
    protected_count: int = 0         # EOU 正确保护的数量
    missed_count: int = 0            # EOU 漏掉的数量
    false_trigger_count: int = 0     # EOU 误触发的数量
    reconnected_count: int = 0       # 重连修正的数量（EOU 误判被自动修正）
    normal_count: int = 0            # 正常 VAD 的数量
    
    # 响应时间对比
    avg_latency_with_eou_ms: Optional[float] = None     # EOU 加速时的平均延迟
    avg_latency_without_eou_ms: Optional[float] = None  # 无 EOU 时的平均延迟
    total_time_saved_ms: float = 0   # EOU 总共节省的时间
    
    # 问题列表
    issues: List[Dict[str, Any]] = field(default_factory=list)
    
    def calculate_summary(self):
        """计算汇总统计"""
        self.total_utterances = len(self.utterances)
        
        if self.total_utterances == 0:
            return
        
        # 计算各指标的平均值
        speech_durations = [u.speech_duration_ms for u in self.utterances if u.speech_duration_ms is not None]
        if speech_durations:
            self.avg_speech_duration_ms = sum(speech_durations) / len(speech_durations)
        
        early_delays = [u.early_to_end_delay_ms for u in self.utterances if u.early_to_end_delay_ms is not None]
        if early_delays:
            self.avg_early_to_end_delay_ms = sum(early_delays) / len(early_delays)
        
        eou_decisions = [u.eou_decision_time_ms for u in self.utterances if u.eou_decision_time_ms is not None]
        if eou_decisions:
            self.avg_eou_decision_time_ms = sum(eou_decisions) / len(eou_decisions)
        
        total_latencies = [u.total_latency_ms for u in self.utterances if u.total_latency_ms is not None]
        if total_latencies:
            self.avg_total_latency_ms = sum(total_latencies) / len(total_latencies)
        
        # EOU 触发率
        eou_triggered_count = len([u for u in self.utterances if u.eou_triggered])
        self.eou_trigger_rate = eou_triggered_count / self.total_utterances
        
        # EOU 效果分类统计
        self.accelerated_count = len([u for u in self.utterances if u.eou_result_type == "accelerated"])
        self.protected_count = len([u for u in self.utterances if u.eou_result_type == "protected"])
        self.missed_count = len([u for u in self.utterances if u.eou_result_type == "missed"])
        self.false_trigger_count = len([u for u in self.utterances if u.eou_result_type == "false_trigger"])
        self.reconnected_count = len([u for u in self.utterances if u.eou_result_type == "reconnected"])
        self.normal_count = len([u for u in self.utterances if u.eou_result_type == "normal"])
        
        # 计算 EOU 节省的总时间
        self.total_time_saved_ms = sum(u.time_saved_ms for u in self.utterances if u.time_saved_ms is not None)
        
        # 计算有/无 EOU 时的平均延迟对比
        eou_latencies = [u.total_latency_ms for u in self.utterances 
                         if u.eou_triggered and u.total_latency_ms is not None]
        if eou_latencies:
            self.avg_latency_with_eou_ms = sum(eou_latencies) / len(eou_latencies)
        
        non_eou_latencies = [u.total_latency_ms for u in self.utterances 
                             if not u.eou_triggered and u.total_latency_ms is not None]
        if non_eou_latencies:
            self.avg_latency_without_eou_ms = sum(non_eou_latencies) / len(non_eou_latencies)
        
        # 检测问题
        self._detect_issues()
    
    def _detect_issues(self):
        """检测问题"""
        self.issues = []
        
        for utterance in self.utterances:
            # 检测重连事件（EOU 误判被自动修正）
            if utterance.eou_result_type == "reconnected":
                self.issues.append({
                    "type": "reconnected",
                    "severity": "info",
                    "utterance_id": utterance.utterance_id,
                    "detail": f"重连修正：EOU 误判被自动修正，取消了 stream {utterance.cancelled_stream_key}",
                    "cancelled_stream_key": utterance.cancelled_stream_key,
                    "time_gap_ms": utterance.reconnect_time_gap_ms
                })
            
            # 检测 EOU 误触发（假阳性）
            if utterance.eou_result_type == "false_trigger":
                self.issues.append({
                    "type": "eou_false_trigger",
                    "severity": "warning",
                    "utterance_id": utterance.utterance_id,
                    "detail": f"EOU 可能误触发：句子 \"{utterance.asr_text[:30] if utterance.asr_text else ''}...\" 看起来不完整",
                    "asr_text": utterance.asr_text,
                    "probability": utterance.eou_final_probability
                })
            
            # 检测 EOU 漏触发（假阴性）- 短句但没触发
            if utterance.eou_result_type == "missed":
                self.issues.append({
                    "type": "eou_missed",
                    "severity": "info",
                    "utterance_id": utterance.utterance_id,
                    "detail": f"短句 \"{utterance.asr_text}\" 未被 EOU 加速",
                    "speech_duration_ms": utterance.speech_duration_ms,
                    "early_to_end_delay_ms": utterance.early_to_end_delay_ms
                })
            
            # 检测 EOU 决策过慢
            if utterance.eou_decision_time_ms is not None and utterance.eou_decision_time_ms > 200:
                self.issues.append({
                    "type": "slow_eou_decision",
                    "severity": "info",
                    "utterance_id": utterance.utterance_id,
                    "detail": f"EOU 决策时间 {utterance.eou_decision_time_ms:.0f}ms 较长",
                    "value": utterance.eou_decision_time_ms
                })
            
            # 检测总延迟过高（仅针对 EOU 触发的情况）
            if utterance.eou_triggered and utterance.total_latency_ms is not None:
                if utterance.total_latency_ms > 500:
                    self.issues.append({
                        "type": "high_latency",
                        "severity": "warning",
                        "utterance_id": utterance.utterance_id,
                        "detail": f"总延迟 {utterance.total_latency_ms:.0f}ms 较高",
                        "value": utterance.total_latency_ms
                    })
