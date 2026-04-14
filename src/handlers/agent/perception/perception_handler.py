"""
Perception Agent Handler

处理视频流，生成分层视觉上下文，检测环境事件
"""
import json
import threading
import time
from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, List, Optional, cast

import numpy as np
from loguru import logger
from pydantic import BaseModel, Field

from chat_engine.common.handler_base import HandlerBase, HandlerBaseInfo, HandlerDataInfo, HandlerDetail
from chat_engine.contexts.handler_context import HandlerContext
from chat_engine.contexts.session_context import SessionContext
from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel, HandlerBaseConfigModel
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry

from handlers.agent.agent_data_models import PerceptionData, EnvironmentEvent
from handlers.agent.perception.vision_model_interface import (
    VisionModelInterface,
    MockVisionModel,
    OpenAIVisionModel,
    AsyncPerceptionManager,
)


class PerceptionConfig(HandlerBaseConfigModel, BaseModel):
    """Perception Handler 配置"""
    # 摘要生成间隔 (秒)
    summary_interval: float = Field(default=3.0, description="生成视觉摘要的间隔时间")
    
    # 帧缓冲大小
    max_buffer_frames: int = Field(default=30, description="最大缓冲帧数")
    
    # 关键帧选择策略
    key_frame_strategy: str = Field(default="interval", description="关键帧选择策略: interval, motion, all")
    key_frame_interval: int = Field(default=10, description="关键帧间隔 (用于 interval 策略)")
    
    # 视觉模型类型
    vision_model_type: str = Field(default="mock", description="视觉模型类型: mock, qwen_vl, openai")

    # 视觉模型配置 (OpenAI 兼容接口)
    llm_model: str = Field(default="qwen-plus-vl", description="视觉模型名称")
    api_key: Optional[str] = Field(default=None, description="API Key (默认从环境变量获取)")
    api_url: Optional[str] = Field(default=None, description="API URL")
    max_frames: int = Field(default=4, description="每次请求最多发送的帧数")
    
    # 事件检测配置
    enable_event_detection: bool = Field(default=True, description="是否启用事件检测")
    event_detection_interval: int = Field(default=5, description="事件检测间隔 (每 N 帧检测一次)")
    
    # 并发请求配置
    max_concurrent_requests: int = Field(default=3, description="最大并发 LLM 请求数")

    # VLM 自定义 system prompt（不配置则用代码默认值）
    vlm_system_prompt: Optional[str] = Field(default=None, description="VLM system prompt 覆盖")


@dataclass
class PerceptionContext(HandlerContext):
    """Perception Handler 上下文"""
    
    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[PerceptionConfig] = None
        
        # 帧缓冲
        self.frame_buffer: List[np.ndarray] = []
        self.frame_count: int = 0
        
        # 上次生成摘要的时间
        self.last_summary_time: float = 0.0
        
        # 上一帧 (用于事件检测)
        self.previous_frame: Optional[np.ndarray] = None
        
        # 当前的感知数据
        self.current_perception: Optional[PerceptionData] = None
        
        # 视觉模型
        self.vision_model: Optional[VisionModelInterface] = None
        
        # 异步感知管理器
        self.async_manager: Optional[AsyncPerceptionManager] = None
        
        # FPS 统计
        self.fps_start_time: float = 0.0  # FPS 统计开始时间
        self.fps_frame_count: int = 0     # FPS 统计周期内的帧数
        self.current_fps: float = 0.0     # 当前计算的 FPS
        self.fps_update_interval: float = 2.0  # FPS 更新间隔 (秒)
        
        # 感知轮次计数器 (用于日志区分)
        self.perception_round: int = 0
        
        # 输出定义引用 (用于异步回调)
        self.output_definitions: Optional[Dict[ChatDataType, HandlerDataInfo]] = None
        
        # 事件去重：记录最近发送的事件类型和时间
        self.last_event_times: Dict[str, float] = {}
        self.event_dedup_interval: float = 5.0  # 同类型事件去重间隔 (秒)
        
        # 摄像头帧心跳检测
        self.last_frame_time: float = 0.0
        self.frame_stall_warned: bool = False
        self.frame_stall_threshold: float = 10.0  # 超过此秒数未收到帧则告警
        self.frame_resumed_after_stall: bool = False
        self._heartbeat_stop: threading.Event = threading.Event()


class PerceptionHandler(HandlerBase, ABC):
    """
    Perception Agent Handler
    
    职责:
    1. 接收 CAMERA_VIDEO 流
    2. 定期生成分层视觉上下文 (PERCEPTION_CONTEXT)
    3. 实时检测环境事件 (通过 Signal 发送 ENVIRONMENT_EVENT)
    """
    
    def __init__(self):
        super().__init__()
        self.output_definition: Optional[DataBundleDefinition] = None
    
    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(
            config_model=PerceptionConfig,
        )
    
    def load(self, engine_config: ChatEngineConfigModel, 
             handler_config: Optional[HandlerBaseConfigModel] = None):
        """加载 Handler"""
        # 创建输出定义
        self.output_definition = DataBundleDefinition()
        self.output_definition.add_entry(
            DataBundleEntry(
                name="perception_data",
            )
        )
        logger.info("PerceptionHandler loaded")
    
    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        """创建会话上下文"""
        context = PerceptionContext(session_context.session_info.session_id)
        
        if isinstance(handler_config, PerceptionConfig):
            context.config = handler_config
        else:
            context.config = PerceptionConfig()
        
        # 创建视觉模型
        context.vision_model = self._create_vision_model(context.config)
        
        # 创建异步感知管理器
        context.async_manager = AsyncPerceptionManager(
            vision_model=context.vision_model,
            max_workers=context.config.max_concurrent_requests,
            on_result_callback=lambda round_id, data: self._on_async_result(context, round_id, data),
        )
        
        logger.info(f"PerceptionContext created for session {context.session_id} "
                   f"(max_concurrent_requests={context.config.max_concurrent_requests})")
        return context
    
    def _create_vision_model(self, config: PerceptionConfig) -> VisionModelInterface:
        """根据配置创建视觉模型"""
        model_type = config.vision_model_type
        if model_type == "mock":
            return MockVisionModel()
        if model_type == "openai":
            return OpenAIVisionModel(
                model_name=config.llm_model,
                api_key=config.api_key,
                api_url=config.api_url,
                max_frames=config.max_frames,
                system_prompt=config.vlm_system_prompt,
            )
        else:
            logger.warning(f"Unknown vision model type: {model_type}, using mock")
            return MockVisionModel()
    
    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        """启动上下文"""
        context = cast(PerceptionContext, handler_context)
        if context.vision_model:
            context.vision_model.warmup()
        
        # 启动帧心跳监控线程
        heartbeat_thread = threading.Thread(
            target=self._frame_heartbeat_monitor,
            args=(context,),
            daemon=True,
            name=f"perception-heartbeat-{context.session_id}",
        )
        heartbeat_thread.start()
    
    def _frame_heartbeat_monitor(self, context: PerceptionContext):
        """后台线程：定期检查摄像头帧是否仍在到达"""
        check_interval = 5.0
        while not context._heartbeat_stop.wait(timeout=check_interval):
            if context.last_frame_time == 0.0:
                continue
            
            gap = time.time() - context.last_frame_time
            if gap >= context.frame_stall_threshold and not context.frame_stall_warned:
                context.frame_stall_warned = True
                logger.warning(
                    f"[Perception] ⚠️ 摄像头帧中断! 已 {gap:.1f}s 未收到新帧 "
                    f"(阈值: {context.frame_stall_threshold}s, "
                    f"已处理帧数: {context.frame_count})"
                )
    
    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        """定义输入输出"""
        perception_definition = DataBundleDefinition()
        perception_definition.add_entry(
            DataBundleEntry(
                name="perception_data",
            )
        )
        
        event_definition = DataBundleDefinition()
        event_definition.add_entry(
            DataBundleEntry(
                name="event_data",
            )
        )
        
        return HandlerDetail(
            inputs={
                ChatDataType.CAMERA_VIDEO: HandlerDataInfo(
                    type=ChatDataType.CAMERA_VIDEO,
                ),
            },
            outputs={
                ChatDataType.PERCEPTION_CONTEXT: HandlerDataInfo(
                    type=ChatDataType.PERCEPTION_CONTEXT,
                    definition=perception_definition,
                ),
                ChatDataType.ENVIRONMENT_EVENT: HandlerDataInfo(
                    type=ChatDataType.ENVIRONMENT_EVENT,
                    definition=event_definition,
                ),
            },
        )
    
    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """处理视频帧"""
        context = cast(PerceptionContext, context)
        
        if inputs.type != ChatDataType.CAMERA_VIDEO:
            logger.debug(f"[Perception] 跳过非视频输入: {inputs.type}")
            return
        
        frame = inputs.data.get_main_data()
        if frame is None:
            logger.warning("[Perception] 收到空帧数据")
            return
        
        current_time = time.time()
        
        # 摄像头帧心跳检测：检查是否从中断中恢复
        if context.frame_stall_warned:
            gap = current_time - context.last_frame_time
            logger.warning(
                f"[Perception] 📡 摄像头帧恢复! 中断持续 {gap:.1f}s, "
                f"总帧数: {context.frame_count}"
            )
            context.frame_stall_warned = False
            context.frame_resumed_after_stall = True
        context.last_frame_time = current_time
        
        # FPS 统计
        if context.fps_start_time == 0.0:
            context.fps_start_time = current_time
        context.fps_frame_count += 1
        
        fps_elapsed = current_time - context.fps_start_time
        if fps_elapsed >= context.fps_update_interval:
            context.current_fps = context.fps_frame_count / fps_elapsed
            logger.info(f"[Perception] 📊 输入帧率: {context.current_fps:.1f} FPS "
                       f"(统计周期: {fps_elapsed:.1f}s, 帧数: {context.fps_frame_count})")
            # 重置统计
            context.fps_start_time = current_time
            context.fps_frame_count = 0
        
        # 调试：打印帧数据的详细信息
        if context.frame_count % 100 == 0:  # 每100帧打印一次详细信息
            if isinstance(frame, np.ndarray):
                logger.debug(f"[Perception] Frame info: shape={frame.shape}, dtype={frame.dtype}, "
                           f"size={frame.size}, contiguous={frame.flags['C_CONTIGUOUS']}")
            else:
                logger.warning(f"[Perception] Frame is not ndarray, type={type(frame)}, value={str(frame)[:100]}")
        
        # 增加帧计数
        context.frame_count += 1
        
        # 每100帧打印一次状态
        if context.frame_count % 100 == 0:
            logger.info(f"[Perception] 📹 已处理 {context.frame_count} 帧, 缓冲区: {len(context.frame_buffer)} 帧, 当前FPS: {context.current_fps:.1f}")
        
        # 1. 添加到帧缓冲
        self._add_to_buffer(context, frame)
        
        # 2. 检查是否需要生成摘要
        current_time = time.time()
        if current_time - context.last_summary_time >= context.config.summary_interval:
            logger.info(f"[Perception] ⏰ 触发摘要生成 (间隔: {context.config.summary_interval}s)")
            self._generate_and_emit_perception(context, output_definitions)
            context.last_summary_time = current_time
        
        # 注意：事件检测现在通过 generate_perception 的 detected_events 字段实现
        # 不再需要单独的 _detect_and_emit_events 调用
        
        # 更新上一帧
        context.previous_frame = frame
    
    def _add_to_buffer(self, context: PerceptionContext, frame: np.ndarray):
        """添加帧到缓冲"""
        # 根据策略决定是否添加
        should_add = False
        if context.config.key_frame_strategy == "all":
            should_add = True
        elif context.config.key_frame_strategy == "interval":
            if context.frame_count % context.config.key_frame_interval == 0:
                should_add = True
        # TODO: motion 策略需要计算帧间差异
        
        if should_add:
            context.frame_buffer.append(frame)
        
        # 限制缓冲大小
        while len(context.frame_buffer) > context.config.max_buffer_frames:
            context.frame_buffer.pop(0)
    
    def _generate_and_emit_perception(self, context: PerceptionContext,
                                      output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        """生成并发送感知数据（异步提交任务）"""
        if not context.frame_buffer:
            logger.debug("[Perception] 帧缓冲为空，跳过摘要生成")
            return
        
        if context.async_manager is None:
            logger.error("[Perception] AsyncPerceptionManager 未初始化")
            return
        
        try:
            # 增加轮次计数
            context.perception_round += 1
            round_id = context.perception_round
            round_tag = f"[Round-{round_id}]"
            
            # 计算关键帧的有效帧率
            buffer_size = len(context.frame_buffer)
            effective_fps = buffer_size / context.config.summary_interval if context.config.summary_interval > 0 else 0
            
            logger.info(f"[Perception] {round_tag} 🔍 准备提交异步任务:")
            logger.info(f"[Perception] {round_tag}   └─ 缓冲关键帧数: {buffer_size}")
            logger.info(f"[Perception] {round_tag}   └─ 输入帧率: {context.current_fps:.1f} FPS")
            logger.info(f"[Perception] {round_tag}   └─ 关键帧有效帧率: {effective_fps:.1f} FPS (每 {context.config.key_frame_interval} 帧保存1帧)")
            
            # 复制当前帧缓冲（避免并发修改）
            frames_snapshot = context.frame_buffer.copy()
            
            # 保存 output_definitions 引用（用于异步回调）
            context.output_definitions = output_definitions
            
            # 提交异步任务
            submitted = context.async_manager.submit_task(
                round_id=round_id,
                frames=frames_snapshot,
            )
            
            if submitted:
                # 清空帧缓冲
                context.frame_buffer.clear()
            else:
                # 达到并发上限，保留帧缓冲等待下次触发
                # 回退轮次计数，因为任务未实际执行
                context.perception_round -= 1
                logger.warning(f"[Perception] {round_tag} ⚠️ 任务提交失败，保留帧缓冲等待下次触发")
            
        except Exception as e:
            logger.error(f"[Perception] ❌ 提交感知任务失败: {e}")
    
    def _on_async_result(self, context: PerceptionContext, round_id: int, 
                         perception: Optional[PerceptionData]):
        """
        异步任务完成回调
        
        Args:
            context: 感知上下文
            round_id: 感知轮次 ID
            perception: 感知数据（可能为 None 表示失败）
        """
        round_tag = f"[Round-{round_id}]"
        
        try:
            if perception is None:
                logger.warning(f"[Perception] {round_tag} ⚠️ 异步任务返回空结果，跳过发送")
                return
            
            # 更新当前感知数据
            context.current_perception = perception
            
            logger.info(f"[Perception] {round_tag} ✅ 异步任务完成:")
            logger.info(f"[Perception] {round_tag}   └─ 场景描述: {perception.scene_summary}")
            logger.info(f"[Perception] {round_tag}   └─ 用户状态: emotion={perception.user_state.emotion}, gaze={perception.user_state.gaze}")
            logger.info(f"[Perception] {round_tag}   └─ 场景结构: location={perception.scene_structure.location}")
            
            # 创建输出数据
            output_definitions = context.output_definitions
            if output_definitions is None:
                logger.warning(f"[Perception] {round_tag} output_definitions 未设置，无法发送")
                return
            
            # 发送 PERCEPTION_CONTEXT
            output_def = output_definitions.get(ChatDataType.PERCEPTION_CONTEXT)
            if output_def and output_def.definition:
                output = DataBundle(output_def.definition)
                # 序列化为 JSON 字符串，因为 DataBundle 只支持 str 和 np.ndarray
                output.set_main_data(json.dumps(perception.to_dict(), ensure_ascii=False))
                # 多输出类型时需要指定数据类型
                context.submit_data((ChatDataType.PERCEPTION_CONTEXT, output))
                
                logger.info(f"[Perception] {round_tag} 📤 已发送 PERCEPTION_CONTEXT 到 Manager")
            
            # 检查并发送 ENVIRONMENT_EVENT
            self._emit_detected_events(context, perception, output_definitions, round_tag)
            
        except Exception as e:
            logger.error(f"[Perception] {round_tag} ❌ 处理异步结果失败: {e}")
    
    def _emit_detected_events(self, context: PerceptionContext, perception: PerceptionData,
                              output_definitions: Dict[ChatDataType, HandlerDataInfo], round_tag: str):
        """
        检查并发送检测到的交互事件
        
        Args:
            context: 感知上下文
            perception: 感知数据
            output_definitions: 输出定义
            round_tag: 日志标签
        """
        # 获取可触发响应的事件
        triggerable_events = perception.get_triggerable_events()
        
        if not triggerable_events:
            return
        
        current_time = time.time()
        event_def = output_definitions.get(ChatDataType.ENVIRONMENT_EVENT)
        
        if not event_def or not event_def.definition:
            logger.warning(f"[Perception] {round_tag} ENVIRONMENT_EVENT 输出定义未设置")
            return
        
        for detected_event in triggerable_events:
            # 事件去重检查
            last_time = context.last_event_times.get(detected_event.event_type, 0.0)
            if current_time - last_time < context.event_dedup_interval:
                logger.debug(f"[Perception] {round_tag} 跳过重复事件: {detected_event.event_type} "
                           f"(距上次 {current_time - last_time:.1f}s)")
                continue
            
            # 更新事件时间
            context.last_event_times[detected_event.event_type] = current_time
            
            # 转换为 EnvironmentEvent
            env_event = EnvironmentEvent.from_detected_event(detected_event, urgency="high")
            
            # 发送事件 (多输出类型时需要指定数据类型)
            event_output = DataBundle(event_def.definition)
            event_output.set_main_data(json.dumps(env_event.to_dict(), ensure_ascii=False))
            context.submit_data((ChatDataType.ENVIRONMENT_EVENT, event_output))
            
            logger.info(f"[Perception] {round_tag} 📣 检测到交互事件: {detected_event.event_type} "
                       f"(confidence: {detected_event.confidence:.2f})")
            logger.info(f"[Perception] {round_tag} 📤 已发送 ENVIRONMENT_EVENT 到 Manager")
    
    def destroy_context(self, context: HandlerContext):
        """销毁上下文"""
        context = cast(PerceptionContext, context)
        
        # 停止心跳监控
        context._heartbeat_stop.set()
        
        # 关闭异步管理器（不等待，避免卡住）
        if context.async_manager:
            context.async_manager.shutdown(wait=False, timeout=2.0)
            context.async_manager = None
        
        if context.vision_model:
            context.vision_model.cleanup()
        context.frame_buffer.clear()
        logger.info(f"PerceptionContext destroyed for session {context.session_id}")
