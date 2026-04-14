"""
VAD/EOU 分析 Handler

旁路监听 VAD、EOU、ASR 的工作过程，收集关键事件和时间点，
生成可视化报告和结构化数据用于 AI 分析。
"""
import time
from abc import ABC
from datetime import datetime
from typing import Dict, Optional, cast

from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.chat_signal import ChatSignal, SignalFilterRule
from chat_engine.data_models.chat_signal_type import ChatSignalType
from chat_engine.data_models.runtime_data.event_model import EventType

from .analyzer_models import (
    ASREvent,
    EOUEvent,
    SessionAnalysis,
    UtteranceAnalysis,
    VADEvent,
)


class VADEOUAnalyzerConfig(HandlerBaseConfigModel, BaseModel):
    """VAD/EOU 分析器配置"""
    output_dir: str = Field(default="logs/vad_eou_analysis", description="输出目录")
    generate_html: bool = Field(default=True, description="是否生成 HTML 报告")
    generate_json: bool = Field(default=True, description="是否生成 JSON 数据")


class VADEOUAnalyzerContext(HandlerContext):
    """VAD/EOU 分析器上下文"""
    
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[VADEOUAnalyzerConfig] = None
        self.session_start_time: float = time.time()
        self.session_analysis: SessionAnalysis = SessionAnalysis(
            session_id=session_id,
            start_time=datetime.now()
        )
        self.current_utterances: Dict[str, UtteranceAnalysis] = {}  # stream_key -> utterance
        self.utterance_counter: int = 0
        self.shared_states = None
    
    def get_relative_time_ms(self) -> float:
        """获取相对时间（毫秒）"""
        return (time.time() - self.session_start_time) * 1000
    
    def get_or_create_utterance(self, stream_key: str) -> UtteranceAnalysis:
        """获取或创建当前语句分析"""
        if stream_key not in self.current_utterances:
            self.current_utterances[stream_key] = UtteranceAnalysis(
                utterance_id=self.utterance_counter,
                stream_key=stream_key
            )
            self.utterance_counter += 1
        return self.current_utterances[stream_key]
    
    def finalize_utterance(self, stream_key: str):
        """完成语句分析并保存"""
        if stream_key in self.current_utterances:
            utterance = self.current_utterances.pop(stream_key)
            utterance.calculate_metrics()
            self.session_analysis.utterances.append(utterance)
            duration_str = f"{utterance.speech_duration_ms:.0f}ms" if utterance.speech_duration_ms is not None else "N/A"
            logger.info(
                f"Utterance #{utterance.utterance_id} finalized: "
                f"duration={duration_str}, "
                f"eou_effective={utterance.eou_effective}, "
                f"asr_text='{utterance.asr_text or ''}'"
            )


class HandlerVADEOUAnalyzer(HandlerBase, ABC):
    """VAD/EOU 分析 Handler"""
    
    def __init__(self):
        super().__init__()
        self.config: Optional[VADEOUAnalyzerConfig] = None
    
    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            name="VADEOUAnalyzer",
            config_model=VADEOUAnalyzerConfig,
        )
    
    def load(self, engine_config: ChatEngineConfigModel, handler_config: Optional[BaseModel] = None):
        """加载配置"""
        if isinstance(handler_config, VADEOUAnalyzerConfig):
            self.config = handler_config
        else:
            self.config = VADEOUAnalyzerConfig()
        
        # 保存相关配置用于报告
        self.vad_config = {}
        self.eou_config = {}
        
        # 尝试从 engine_config 获取 VAD 和 EOU 配置
        if engine_config and engine_config.handler_configs:
            for name, cfg in engine_config.handler_configs.items():
                if 'silero' in name.lower() or 'vad' in name.lower():
                    self.vad_config = cfg.model_dump() if hasattr(cfg, 'model_dump') else dict(cfg)
                elif 'eou' in name.lower() or 'smartturn' in name.lower():
                    self.eou_config = cfg.model_dump() if hasattr(cfg, 'model_dump') else dict(cfg)
        
        logger.info(f"VAD/EOU Analyzer loaded, output_dir={self.config.output_dir}")
    
    def create_context(self, session_context: SessionContext, handler_config=None) -> HandlerContext:
        """创建上下文"""
        if not isinstance(handler_config, VADEOUAnalyzerConfig):
            handler_config = self.config or VADEOUAnalyzerConfig()
        
        context = VADEOUAnalyzerContext(session_context.session_info.session_id)
        context.config = handler_config
        context.shared_states = session_context.shared_states
        
        # 保存配置到分析结果
        context.session_analysis.config = {
            "vad": self.vad_config,
            "eou": self.eou_config,
            "analyzer": handler_config.model_dump()
        }
        
        return context
    
    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        """启动上下文"""
        pass
    
    def get_handler_detail(self, session_context: SessionContext, context: HandlerContext) -> HandlerDetail:
        """定义输入输出"""
        # 低优先级旁路监听
        inputs = {
            ChatDataType.HUMAN_AUDIO: HandlerDataInfo(
                type=ChatDataType.HUMAN_AUDIO,
                input_priority=200,  # 低优先级，不影响其他 handler
            ),
            ChatDataType.HUMAN_TEXT: HandlerDataInfo(
                type=ChatDataType.HUMAN_TEXT,
                input_priority=200,
            ),
        }
        
        return HandlerDetail(
            inputs=inputs,
            outputs={},
            signal_filters=[
                # 监听所有信号
                SignalFilterRule(None, None, None)
            ]
        )
    
    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """处理数据"""
        context = cast(VADEOUAnalyzerContext, context)
        
        if inputs.type == ChatDataType.HUMAN_AUDIO:
            self._handle_human_audio(context, inputs)
        elif inputs.type == ChatDataType.HUMAN_TEXT:
            self._handle_human_text(context, inputs)
    
    def _handle_human_audio(self, context: VADEOUAnalyzerContext, inputs: ChatData):
        """处理 HUMAN_AUDIO 数据，提取 VAD 事件"""
        if inputs.stream_id is None:
            return
        
        stream_key = f"{inputs.stream_id.builder_id}_{inputs.stream_id.stream_id}"
        utterance = context.get_or_create_utterance(stream_key)
        current_time_ms = context.get_relative_time_ms()
        
        # 提取 metadata 中的信息
        if inputs.data:
            # 检查是否是重连触发的音频
            if inputs.data.get_meta("reconnected_audio", False):
                reconnected_audio_index = inputs.data.get_meta("reconnected_audio_index", 0)
                utterance.vad_events.append(VADEvent(
                    timestamp_ms=current_time_ms,
                    event_type="reconnected_audio",
                    extra_data={"index": reconnected_audio_index}
                ))
                # 如果是第一个重连音频，记录重连信息
                if reconnected_audio_index == 0:
                    utterance.was_reconnected = True
                    # 记录被取消的 stream key
                    if hasattr(context, '_last_cancelled_stream_key'):
                        utterance.cancelled_stream_key = context._last_cancelled_stream_key
                    # 计算重连时间间隔
                    if hasattr(context, '_last_cancel_time_ms'):
                        utterance.reconnect_time_gap_ms = current_time_ms - context._last_cancel_time_ms
                    logger.info(f"Reconnection detected: cancelled {utterance.cancelled_stream_key}, time gap {utterance.reconnect_time_gap_ms}ms")
            
            # 检查是否是语音开始
            if inputs.data.get_meta("human_speech_start", False):
                utterance.speech_start_ms = current_time_ms
                utterance.vad_events.append(VADEvent(
                    timestamp_ms=current_time_ms,
                    event_type="speech_start",
                    sample_id=inputs.data.get_meta("head_sample_id"),
                    extra_data={"pre_padding": inputs.data.get_meta("pre_padding")}
                ))
                logger.debug(f"VAD speech_start at {current_time_ms:.0f}ms")
            
            # 检查是否有 early_vad_end event
            if inputs.data.has_event(EventType.EVT_EARLY_VAD_END):
                if utterance.early_vad_end_ms is None:  # 只记录第一次
                    utterance.early_vad_end_ms = current_time_ms
                utterance.vad_events.append(VADEvent(
                    timestamp_ms=current_time_ms,
                    event_type="early_vad_end",
                    sample_id=inputs.data.get_meta("head_sample_id"),
                ))
                logger.debug(f"VAD early_vad_end at {current_time_ms:.0f}ms")
            
            # 检查是否是语音结束
            if inputs.data.get_meta("human_speech_end", False):
                utterance.speech_end_ms = current_time_ms
                utterance.vad_events.append(VADEvent(
                    timestamp_ms=current_time_ms,
                    event_type="speech_end",
                    sample_id=inputs.data.get_meta("head_sample_id"),
                    extra_data={"post_padding": inputs.data.get_meta("post_padding")}
                ))
                logger.debug(f"VAD speech_end at {current_time_ms:.0f}ms")
        
        # 如果是最后数据，完成这个语句
        if inputs.is_last_data:
            # 延迟一点完成，等待 ASR 结果
            pass
    
    def _handle_human_text(self, context: VADEOUAnalyzerContext, inputs: ChatData):
        """处理 HUMAN_TEXT 数据，提取 ASR 事件"""
        if inputs.stream_id is None:
            return
        
        current_time_ms = context.get_relative_time_ms()
        text = inputs.data.get_main_data() if inputs.data else None
        source = inputs.source or "Unknown"
        
        # 通过 parent stream 关系找到对应的 HUMAN_AUDIO utterance
        # ASR 的输入是 HUMAN_AUDIO，所以它的 parent 应该是对应的 HUMAN_AUDIO stream
        asr_stream_key = f"{inputs.stream_id.builder_id}_{inputs.stream_id.stream_id}"
        
        # 尝试从 parent stream 获取关联的 HUMAN_AUDIO stream key
        parent_stream_key = None
        if inputs.data:
            parent_stream_id = inputs.data.get_meta("parent_stream_id")
            if parent_stream_id:
                parent_stream_key = f"{parent_stream_id.builder_id}_{parent_stream_id.stream_id}"
        
        # 首选：通过 parent 关系精确匹配
        target_utterance = None
        if parent_stream_key and parent_stream_key in context.current_utterances:
            target_utterance = context.current_utterances[parent_stream_key]
        
        # 备选：找最近的未完成且未被取消的 utterance
        if target_utterance is None:
            for stream_key, utterance in context.current_utterances.items():
                # 跳过被取消的（有 stream_cancelled 事件的）
                is_cancelled = any(e.event_type == "stream_cancelled" for e in utterance.vad_events)
                if not is_cancelled and utterance.asr_text is None:
                    target_utterance = utterance
                    break
        
        if target_utterance is None and context.current_utterances:
            # 最后备选：使用最新的未被取消的
            for utterance in reversed(list(context.current_utterances.values())):
                is_cancelled = any(e.event_type == "stream_cancelled" for e in utterance.vad_events)
                if not is_cancelled:
                    target_utterance = utterance
                    break
        
        if target_utterance:
            asr_event = ASREvent(
                timestamp_ms=current_time_ms,
                event_type="completed" if inputs.is_last_data else "partial",
                text=text if isinstance(text, str) else None,
                stream_key=asr_stream_key,
                source=source
            )
            target_utterance.asr_events.append(asr_event)
            
            if inputs.is_last_data and isinstance(text, str):
                target_utterance.asr_text = text
                target_utterance.asr_completed_ms = current_time_ms
                logger.debug(f"ASR completed at {current_time_ms:.0f}ms: '{text}'")
                
                # ASR 完成后，完成 utterance
                for stream_key in list(context.current_utterances.keys()):
                    if context.current_utterances[stream_key] == target_utterance:
                        context.finalize_utterance(stream_key)
                        break
    
    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        """处理信号"""
        context = cast(VADEOUAnalyzerContext, context)
        current_time_ms = context.get_relative_time_ms()
        
        # 捕获 STREAM_CANCEL 信号（重连触发时会发送）
        if signal.type == ChatSignalType.STREAM_CANCEL:
            if signal.related_stream and signal.related_stream.data_type == ChatDataType.HUMAN_AUDIO:
                cancelled_stream_key = f"{signal.related_stream.builder_id}_{signal.related_stream.stream_id}"
                logger.info(f"STREAM_CANCEL received for {cancelled_stream_key} at {current_time_ms:.0f}ms")
                
                # 记录这个被取消的 stream
                if cancelled_stream_key in context.current_utterances:
                    cancelled_utterance = context.current_utterances[cancelled_stream_key]
                    cancelled_utterance.vad_events.append(VADEvent(
                        timestamp_ms=current_time_ms,
                        event_type="stream_cancelled",
                        extra_data={"source": signal.source_name}
                    ))
                    # 立即完成被取消的 utterance（它不会再有 ASR 结果）
                    context.finalize_utterance(cancelled_stream_key)
                
                # 保存取消信息，后续的新 stream 会引用它
                context._last_cancelled_stream_key = cancelled_stream_key
                context._last_cancel_time_ms = current_time_ms
        
        # 捕获 EOU 发出的 candidate STREAM_END
        elif signal.type == ChatSignalType.STREAM_END and signal.is_candidate:
            # 找到对应的 utterance
            if signal.related_stream:
                stream_key = f"{signal.related_stream.builder_id}_{signal.related_stream.stream_id}"
                if stream_key in context.current_utterances:
                    utterance = context.current_utterances[stream_key]
                    
                    # 从 signal_data 中提取 EOU 预测数据
                    eou_prediction = None
                    eou_probability = None
                    eou_buffer_duration_ms = None
                    if signal.signal_data:
                        eou_prediction = signal.signal_data.get("eou_prediction")
                        eou_probability = signal.signal_data.get("eou_probability")
                        eou_buffer_duration_ms = signal.signal_data.get("eou_buffer_duration_ms")
                    
                    utterance.eou_events.append(EOUEvent(
                        timestamp_ms=current_time_ms,
                        event_type="signal_sent",
                        prediction=eou_prediction,
                        probability=eou_probability,
                        buffer_duration_ms=eou_buffer_duration_ms,
                    ))
                    utterance.eou_triggered = True
                    utterance.eou_effective = True  # 如果触发了，就算有效
                    logger.debug(f"EOU signal_sent at {current_time_ms:.0f}ms for stream {stream_key}, probability={eou_probability}")
        
        # 捕获正式的 STREAM_END（来自 VAD）
        elif signal.type == ChatSignalType.STREAM_END and not signal.is_candidate:
            if signal.related_stream and signal.related_stream.data_type == ChatDataType.HUMAN_AUDIO:
                stream_key = f"{signal.related_stream.builder_id}_{signal.related_stream.stream_id}"
                # 标记这个 utterance 需要被完成
                # 但等待 ASR 结果后再完成
    
    def destroy_context(self, context: HandlerContext):
        """销毁上下文，生成报告"""
        context = cast(VADEOUAnalyzerContext, context)
        
        # 完成所有未完成的 utterance
        for stream_key in list(context.current_utterances.keys()):
            context.finalize_utterance(stream_key)
        
        # 计算汇总统计
        context.session_analysis.end_time = datetime.now()
        context.session_analysis.calculate_summary()
        
        # 生成报告
        self._generate_reports(context)
    
    def _generate_reports(self, context: VADEOUAnalyzerContext):
        """生成分析报告"""
        import os
        
        config = context.config or self.config or VADEOUAnalyzerConfig()
        output_dir = config.output_dir
        
        # 确保输出目录存在
        if not os.path.isabs(output_dir):
            from engine_utils.directory_info import DirectoryInfo
            output_dir = os.path.join(DirectoryInfo.get_project_dir(), output_dir)
        
        os.makedirs(output_dir, exist_ok=True)
        
        session_id = context.session_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成 JSON
        if config.generate_json:
            from .analyzer_json_exporter import export_json
            json_path = os.path.join(output_dir, f"analysis_{session_id}_{timestamp}.json")
            export_json(context.session_analysis, json_path)
            logger.info(f"VAD/EOU analysis JSON exported to {json_path}")
        
        # 生成 HTML
        if config.generate_html:
            from .analyzer_html_generator import generate_html_report
            html_path = os.path.join(output_dir, f"analysis_{session_id}_{timestamp}.html")
            generate_html_report(context.session_analysis, html_path)
            logger.info(f"VAD/EOU analysis HTML report generated at {html_path}")
    
    def destroy(self):
        """销毁 handler"""
        pass
