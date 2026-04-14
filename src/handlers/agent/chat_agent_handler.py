"""
Chat Agent Handler — 统一的对话主 Agent

合并了原 ManagerAgent（记忆管理、感知缓存、主动触发、事件处理）和
原 PersonaAgent（PromptCompiler 编排、LLM 调用、流式输出）的全部职责。

数据流:
  HUMAN_TEXT / PERCEPTION_CONTEXT / ENVIRONMENT_EVENT → ChatAgent → AVATAR_TEXT

Perception 作为独立的异步感知服务（handler），将感知数据和事件推送给 ChatAgent。
"""
import json
import os
import re
import threading
import time
from abc import ABC
from typing import Dict, List, Optional, Set, cast

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
from chat_engine.data_models.chat_stream_config import ChatStreamConfig
from chat_engine.data_models.runtime_data.data_bundle import DataBundle, DataBundleDefinition, DataBundleEntry

from handlers.agent.agent_data_models import PerceptionData, EnvironmentEvent
from handlers.agent.memory.session_memory_manager import SessionMemoryManager, MemoryConfig
from handlers.agent.tools.tool_registry import ToolRegistry
from handlers.agent.prompt.prompt_compiler import (
    PromptCompiler,
    PromptInput,
    PromptLayerConfig,
    DEFAULT_STABLE_CORE,
    DEFAULT_PERSONA_SNAPSHOT,
    MANDATORY_DELEGATION_POLICY,
    REALTIME_AND_TRUTH_POLICY,
    LAYER_PERSONA_SNAPSHOT,
    LAYER_ENVIRONMENT_STATE,
)


# ── 主动消息触发配置 ──

class EventTriggerConfig(BaseModel):
    """单个事件类型的触发配置"""
    enabled: bool = True
    cooldown: float = 30.0
    hint: str = ""


class IdleTriggerConfig(BaseModel):
    """空闲触发配置"""
    enabled: bool = False
    idle_seconds: float = 60.0
    hint: str = "用户已经安静了一会儿，可以适当关心一下或轻松地聊点什么。"
    mode_overrides: Dict[str, float] = Field(
        default={},
        description="模式 → 空闲秒数覆盖，如 {companion: 120, office: 300}"
    )


class PendingConfirmationTriggerConfig(BaseModel):
    """待确认项主动提醒配置"""
    enabled: bool = Field(default=True, description="是否启用待确认主动提醒")
    idle_seconds: float = Field(default=15.0, description="用户空闲多少秒后触发提醒")
    cooldown: float = Field(default=30.0, description="两次提醒之间的冷却时间（秒）")
    hint: str = Field(
        default=(
            "有待确认的审批请求。你必须先向用户说明命令内容并询问是否同意，"
            "得到用户同意后立即调用 exec_approve 工具。口头说'已批准'无效。"
        ),
        description="注入给 agent 的提示文本",
    )


class ProactiveConfig(BaseModel):
    """主动消息触发总配置"""
    enabled: bool = Field(default=True, description="总开关")
    event_triggers: Dict[str, EventTriggerConfig] = Field(
        default={
            "waving": EventTriggerConfig(
                hint="请友好地回应用户的招呼，可以适当询问有什么可以帮助的。"
            ),
            "showing_object": EventTriggerConfig(
                hint="用户正在展示物品，请主动询问或评论用户展示的物品。",
            ),
            "asking_for_attention": EventTriggerConfig(
                hint="用户在寻求你的注意，请积极回应并询问需要什么帮助。"
            ),
            "arriving": EventTriggerConfig(
                cooldown=60.0,
                hint="有人进入画面，可以适当欢迎。",
            ),
            "leaving": EventTriggerConfig(
                cooldown=60.0,
                hint="用户似乎要离开，可以适当道别。",
            ),
        },
        description="事件类型 → 触发配置",
    )
    idle_trigger: IdleTriggerConfig = Field(
        default_factory=IdleTriggerConfig,
        description="空闲触发配置",
    )
    pending_confirmation_trigger: PendingConfirmationTriggerConfig = Field(
        default_factory=PendingConfirmationTriggerConfig,
        description="待确认项主动提醒配置",
    )


class ContextCompactConfig(BaseModel):
    """对话上下文 auto-compact 配置（Phase 3.3 增强）"""
    enabled: bool = Field(default=True, description="是否启用自动压缩")
    compact_threshold: int = Field(default=15, description="触发压缩的对话轮次数")
    keep_recent: int = Field(default=5, description="压缩后保留的最近轮次数")
    save_transcript: bool = Field(default=True, description="压缩前是否保存完整记录")
    compact_model: Optional[str] = Field(default=None, description="压缩用 LLM 模型（默认用主模型）")
    rehydrate_task_brief: bool = Field(default=True, description="压缩后重注入活跃任务摘要")
    rehydrate_env_state: bool = Field(default=True, description="压缩后重注入当前环境状态")


class OcBridgeConfig(BaseModel):
    """OpenClaw Bridge 配置

    启用后同时激活：
    - Plugin Tools MCP（get_agent_profile, memory_search 等工具）
    - oac-bridge HTTP 通道（OAC ↔ OC 双向消息）
    """
    enabled: bool = Field(default=False, description="是否启用 OC Bridge")
    plugin_tools_cmd: Optional[str] = Field(
        default=None,
        description="Plugin Tools MCP 启动命令（如 'node dist/mcp/plugin-tools-serve.js'）"
    )
    persona_refresh_interval: float = Field(default=600.0, description="人格快照刷新间隔（秒）")
    task_mirror_path: str = Field(default=".oac_tasks/mirror.json", description="任务镜像 JSON 路径")
    gateway_http_url: str = Field(
        default="http://localhost:18789",
        description="OC Gateway HTTP 地址（用于发送 webhook）"
    )
    webhook_path: str = Field(
        default="/webhook/oac-bridge",
        description="OC 上 oac-bridge 的 webhook 路径"
    )
    token: str = Field(
        default="",
        description="oac-bridge 共享认证 token（留空表示不认证）"
    )
    callback_port: int = Field(
        default=8011,
        description="OAC 侧 callback HTTP 服务端口（接收 OC 回复）"
    )


class ToolUseConfig(BaseModel):
    """工具调用配置"""
    enabled: bool = Field(default=True, description="是否启用工具调用")
    max_tool_rounds: int = Field(default=5, description="单次 handle 内最大工具调用轮次")
    register_demo_tools: bool = Field(default=True, description="是否注册 demo 工具（用于测试）")


class ChatAgentConfig(HandlerBaseConfigModel, BaseModel):
    """Chat Agent 配置 — 合并了原 Manager 和 Persona 的全部配置"""
    # LLM 配置（只需一套）
    llm_model: str = Field(default="qwen-plus", description="LLM 模型名称")
    api_key: Optional[str] = Field(default=None, description="API Key (默认从环境变量获取)")
    api_url: Optional[str] = Field(default=None, description="API URL")
    # 百炼 OpenAI 兼容接口：混合思考模型默认可能开启思考，此处默认关闭以降低延迟与成本
    enable_thinking: bool = Field(
        default=False,
        description="DashScope 兼容模式下的 enable_thinking；仅当 api_url 指向 dashscope 时注入 extra_body",
    )

    # 工具调用
    tool_use: ToolUseConfig = Field(default_factory=ToolUseConfig, description="工具调用配置")

    # OpenClaw Bridge
    oc_bridge: OcBridgeConfig = Field(default_factory=OcBridgeConfig, description="OpenClaw Bridge 配置")

    # PromptCompiler L1 Stable Core
    stable_core: str = Field(default=DEFAULT_STABLE_CORE, description="OAC 实时规则 / 输出约束")

    # PromptCompiler L2 Persona Snapshot
    persona_snapshot: str = Field(
        default=DEFAULT_PERSONA_SNAPSHOT,
        description="人格快照（本地默认，后续可由 OC 动态更新）"
    )

    # 各层最大字符数
    persona_max_chars: int = Field(default=2500, description="L2 Persona Snapshot 最大字符 (IDENTITY+SOUL+USER)")
    perception_max_chars: int = Field(default=800, description="L3 Environment State 最大字符")

    # 对话历史
    max_dialogue_turns: int = Field(default=20, description="最大对话历史轮次")
    compiler_dialogue_turns: Optional[int] = Field(
        default=None,
        description="PromptCompiler 侧对话历史最大轮次（None = 用全部）"
    )

    # 记忆配置
    perception_max_entries: int = Field(default=100, description="感知缓冲池大小")
    perception_decay_rate: float = Field(default=0.1, description="感知衰减率")
    perception_aggregation_window: float = Field(default=10.0, description="感知事件聚合窗口（秒）")
    summary_update_interval: int = Field(default=5, description="会话摘要更新间隔（轮次）")

    # 主动消息触发
    proactive: ProactiveConfig = Field(default_factory=ProactiveConfig, description="主动消息触发配置")

    # 对话上下文压缩
    context_compact: ContextCompactConfig = Field(
        default_factory=ContextCompactConfig, description="上下文自动压缩配置"
    )

    def to_memory_config(self) -> MemoryConfig:
        return MemoryConfig(
            max_dialogue_turns=self.max_dialogue_turns,
            perception_max_entries=self.perception_max_entries,
            perception_decay_rate=self.perception_decay_rate,
            perception_aggregation_window=self.perception_aggregation_window,
            summary_update_interval_turns=self.summary_update_interval,
            compact_enabled=self.context_compact.enabled,
            compact_threshold=self.context_compact.compact_threshold,
            compact_keep_recent=self.context_compact.keep_recent,
            compact_save_transcript=self.context_compact.save_transcript,
            rehydrate_task_brief=self.context_compact.rehydrate_task_brief,
            rehydrate_env_state=self.context_compact.rehydrate_env_state,
        )


class ChatAgentContext(HandlerContext):
    """Chat Agent 上下文 — 合并了原 Manager 和 Persona 的上下文"""

    def __init__(self, session_id: str):
        super().__init__(session_id)
        self.config: Optional[ChatAgentConfig] = None
        self.llm_client = None
        self.memory: Optional[SessionMemoryManager] = None
        self.compiler: Optional[PromptCompiler] = None
        self.tool_registry: Optional[ToolRegistry] = None

        # OC Bridge components (Phase 3+4)
        self.oc_mcp_client = None
        self.oc_channel_client = None  # OcChannelClient (Phase 4.3: oac-bridge HTTP channel)
        self.persona_mgr = None       # PersonaSnapshotManager (deprecated: Phase 4.1 will use MCP)
        self.task_queue = None         # TaskNotificationQueue
        self.task_mirror = None        # TaskMirror — kept for compact rehydration
        self.pending_confirmations = None  # PendingConfirmationsManager

        # 感知缓存
        self.cached_perception: Optional[PerceptionData] = None

        # 主动触发
        self.pending_events: List[EnvironmentEvent] = []
        self.output_definitions: Optional[Dict[ChatDataType, HandlerDataInfo]] = None

        # 输入缓冲
        self.input_buffer: str = ""
        self.is_generating: bool = False

        # 事件响应追踪
        self.responded_events: Dict[str, float] = {}

        # 空闲触发 & 主动唤醒
        self.last_interaction_time: float = 0.0
        self._idle_stop: threading.Event = threading.Event()
        self._idle_triggered: bool = False
        self._proactive_wake: threading.Event = threading.Event()

        # 流式输出管理
        self.active_stream_keys: Set[str] = set()

        # Serialize _generate_response — the idle-trigger thread and the
        # pipeline thread must never call it concurrently.
        self._generate_lock: threading.Lock = threading.Lock()


class ChatAgentHandler(HandlerBase, ABC):
    """
    Chat Agent — 统一的对话主 Agent

    职责:
    1. 接收 HUMAN_TEXT, PERCEPTION_CONTEXT, ENVIRONMENT_EVENT
    2. 通过 SessionMemoryManager 维护分层记忆
    3. 通过 PromptCompiler 4 层架构编排 prompt (L1 Core + L2 Persona + L3 Env + L4 Dialogue)
    4. 流式调用 LLM + Agent Loop (tool_call → execute → feedback → repeat)
    5. 主动消息触发（事件驱动 + 空闲驱动）
    """

    def __init__(self):
        super().__init__()
        self.output_definition: Optional[DataBundleDefinition] = None

    def get_handler_info(self) -> HandlerBaseInfo:
        return HandlerBaseInfo(config_model=ChatAgentConfig)

    def load(self, engine_config: ChatEngineConfigModel,
             handler_config: Optional[HandlerBaseConfigModel] = None):
        self.output_definition = DataBundleDefinition()
        self.output_definition.add_entry(DataBundleEntry(name="avatar_text"))
        logger.info("ChatAgentHandler loaded")

    def create_context(self, session_context: SessionContext,
                       handler_config: Optional[HandlerBaseConfigModel] = None) -> HandlerContext:
        context = ChatAgentContext(session_context.session_info.session_id)

        if isinstance(handler_config, ChatAgentConfig):
            context.config = handler_config
        else:
            context.config = ChatAgentConfig()

        api_key = context.config.api_key or os.getenv("DASHSCOPE_API_KEY")
        try:
            from openai import OpenAI
            context.llm_client = OpenAI(api_key=api_key, base_url=context.config.api_url)
        except Exception as e:
            logger.warning(f"Failed to create LLM client: {e}")

        context.memory = SessionMemoryManager(config=context.config.to_memory_config())
        context.compiler = self._build_compiler(context.config)
        context.tool_registry = self._build_tool_registry(context.config)

        # OC Bridge initialization
        if context.config.oc_bridge.enabled:
            self._init_oc_bridge(context)
        else:
            logger.info(
                "[ChatAgent] OC Bridge 未启用：不会从 OpenClaw 拉取 L2 人格，"
                "也不会注册 OC 工具。请在配置中设置 ChatAgent.oc_bridge.enabled=true "
                "（并配置 plugin_tools_cmd、gateway_http_url）。"
            )

        context.last_interaction_time = time.time()

        logger.info(f"ChatAgentContext created for session {context.session_id}")
        return context

    def start_context(self, session_context: SessionContext, handler_context: HandlerContext):
        context = cast(ChatAgentContext, handler_context)
        proactive_cfg = context.config.proactive
        need_loop = proactive_cfg.enabled and (
            proactive_cfg.idle_trigger.enabled
            or proactive_cfg.pending_confirmation_trigger.enabled
        )
        if need_loop:
            t = threading.Thread(
                target=self._idle_trigger_loop,
                args=(context,),
                daemon=True,
                name=f"chat-idle-{context.session_id}",
            )
            t.start()
            logger.info(
                f"[ChatAgent] 主动触发循环已启动 "
                f"(idle={proactive_cfg.idle_trigger.enabled}, "
                f"pending_confirm={proactive_cfg.pending_confirmation_trigger.enabled})"
            )

    def get_handler_detail(self, session_context: SessionContext,
                           context: HandlerContext) -> HandlerDetail:
        definition = DataBundleDefinition()
        definition.add_entry(DataBundleEntry(name="avatar_text"))

        return HandlerDetail(
            inputs={
                ChatDataType.HUMAN_TEXT: HandlerDataInfo(type=ChatDataType.HUMAN_TEXT),
                ChatDataType.PERCEPTION_CONTEXT: HandlerDataInfo(type=ChatDataType.PERCEPTION_CONTEXT),
                ChatDataType.ENVIRONMENT_EVENT: HandlerDataInfo(type=ChatDataType.ENVIRONMENT_EVENT),
            },
            outputs={
                ChatDataType.AVATAR_TEXT: HandlerDataInfo(
                    type=ChatDataType.AVATAR_TEXT,
                    definition=definition,
                ),
            },
            signal_filters=[
                SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, None),
            ],
        )

    # ── Signal 兼容 ──

    def on_signal(self, context: HandlerContext, signal: ChatSignal):
        context = cast(ChatAgentContext, context)

        if signal.type == ChatSignalType.STREAM_CANCEL and signal.related_stream:
            stream_key = signal.related_stream.stream_key_str
            if stream_key is not None and stream_key in context.active_stream_keys:
                context.active_stream_keys.discard(stream_key)
                logger.info(f"[ChatAgent] Removed stream {stream_key} from active set")
            return

        if signal.type == ChatSignalType.ENVIRONMENT_EVENT:
            event = EnvironmentEvent.from_dict(signal.signal_data or {})
            importance = self._event_importance(event)
            if context.memory:
                context.memory.record_perception(
                    content=event.description,
                    category="event",
                    importance=importance,
                    metadata=event.to_dict(),
                    event_type=event.event_type,
                )
            context.pending_events.append(event)

    # ── 主入口 ──

    def handle(self, context: HandlerContext, inputs: ChatData,
               output_definitions: Dict[ChatDataType, HandlerDataInfo]):
        context = cast(ChatAgentContext, context)

        logger.debug(
            f"[ChatAgent] 收到输入: type={inputs.type.value}, is_last={inputs.is_last_data}"
        )

        if inputs.type == ChatDataType.PERCEPTION_CONTEXT:
            self._handle_perception_context(context, inputs)
            return

        if inputs.type == ChatDataType.ENVIRONMENT_EVENT:
            self._handle_environment_event(context, inputs, output_definitions)
            return

        if inputs.type == ChatDataType.HUMAN_TEXT:
            self._handle_human_text(context, inputs, output_definitions)
            return

    # ── PERCEPTION_CONTEXT ──

    def _handle_perception_context(self, context: ChatAgentContext, inputs: ChatData):
        data = inputs.data.get_main_data()
        if data is None:
            return

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse perception data as JSON: {data[:100]}")
                return
        if isinstance(data, dict):
            context.cached_perception = PerceptionData.from_dict(data)
        elif isinstance(data, PerceptionData):
            context.cached_perception = data

        if context.memory and context.cached_perception:
            context.memory.record_perception(
                content=context.cached_perception.scene_summary,
                category="scene",
                importance=0.3,
            )

    # ── ENVIRONMENT_EVENT ──

    def _handle_environment_event(
        self, context: ChatAgentContext, inputs: ChatData,
        output_definitions: Dict[ChatDataType, HandlerDataInfo],
    ):
        data = inputs.data.get_main_data()
        if data is None:
            return

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return

        if not context.config.proactive.enabled:
            return

        event = EnvironmentEvent.from_dict(data)
        trigger_cfg = context.config.proactive.event_triggers.get(event.event_type)

        if trigger_cfg is None or not trigger_cfg.enabled:
            logger.debug(f"[ChatAgent] 事件类型未配置或已禁用: {event.event_type}")
            return

        if self._should_skip_event(context, event, trigger_cfg.cooldown):
            logger.info(f"[ChatAgent] 跳过已响应事件: {event.event_type} (冷却中)")
            return

        logger.info(
            f"[ChatAgent] 处理交互事件: {event.event_type} "
            f"(confidence: {event.confidence:.2f}, urgency: {event.urgency})"
        )

        importance = self._event_importance(event)
        if context.memory:
            context.memory.record_perception(
                content=event.description,
                category="event",
                importance=importance,
                metadata=event.to_dict(),
                event_type=event.event_type,
            )

        context.output_definitions = output_definitions

        if event.should_interrupt():
            self._handle_proactive_response(
                context, [event], output_definitions, [trigger_cfg]
            )
        elif event.should_respond_immediately():
            if not context.is_generating:
                self._handle_proactive_response(
                    context, [event], output_definitions, [trigger_cfg]
                )
            else:
                context.pending_events.append(event)
        else:
            context.pending_events.append(event)

    # ── 主动响应 ──

    def _handle_proactive_response(
        self,
        context: ChatAgentContext,
        events: List[EnvironmentEvent],
        output_definitions: Dict[ChatDataType, HandlerDataInfo],
        trigger_cfgs: Optional[List[Optional[EventTriggerConfig]]] = None,
    ):
        """对一组事件产出一次合并回复。"""
        if not events:
            return

        acquired = context._generate_lock.acquire(timeout=0.5)
        if not acquired:
            logger.info("[ChatAgent] 主动响应跳过: _generate_lock 被占用")
            return
        try:
            context.is_generating = True

            cfgs = trigger_cfgs or [None] * len(events)

            hints = []
            for ev, cfg in zip(events, cfgs):
                if cfg and cfg.hint:
                    hints.append(cfg.hint)
                else:
                    hints.append(ev.description)

            merged_hint = "\n".join(hints)

            prompt_input = self._build_prompt_input(
                context,
                trigger_type="event",
                response_hint=merged_hint,
            )

            if context.memory:
                for ev in events:
                    context.memory.record_system_event(
                        content=f"[环境事件: {ev.event_type}] {ev.description}",
                        trigger_type="event",
                    )

            event_names = ", ".join(ev.event_type for ev in events)
            logger.info(f"[ChatAgent] 主动响应 ({len(events)} 事件合并): {event_names}")
            self._generate_response(context, prompt_input, output_definitions)

            now = time.time()
            for ev in events:
                context.responded_events[ev.event_type] = now
            context.last_interaction_time = now
            context._idle_triggered = False
        finally:
            context._generate_lock.release()

    # ── HUMAN_TEXT (用户输入主流程) ──

    def _handle_human_text(
        self, context: ChatAgentContext,
        inputs: ChatData,
        output_definitions: Dict[ChatDataType, HandlerDataInfo],
    ):
        if context.responded_events:
            context.responded_events.clear()
        if context.pending_events:
            logger.info(
                f"[ChatAgent] 用户输入，丢弃 {len(context.pending_events)} 个待处理事件"
            )
            context.pending_events.clear()

        text = inputs.data.get_main_data()
        if isinstance(text, str):
            context.input_buffer += text

        if not inputs.is_last_data:
            return

        full_text = context.input_buffer.strip()
        context.input_buffer = ""

        if not full_text:
            return

        # Wait for any in-flight proactive generation to finish (user
        # input takes priority, but we must not overlap _generate_response).
        acquired = context._generate_lock.acquire(timeout=10.0)
        if not acquired:
            logger.warning(
                f"[ChatAgent] 用户输入 '{full_text[:40]}' 等待生成锁超时，强制继续"
            )
        try:
            logger.info("[ChatAgent] ══════════════════════════════════════════")
            logger.info(f"[ChatAgent] 开始处理用户输入: '{full_text}'")
            context.is_generating = True
            context.last_interaction_time = time.time()
            context._idle_triggered = False
            context.output_definitions = output_definitions

            perception_snapshot = (
                context.cached_perception.scene_summary if context.cached_perception else None
            )
            if context.memory:
                context.memory.record_user_input(
                    content=full_text,
                    trigger_type="user",
                    perception_snapshot=perception_snapshot,
                )

            prompt_input = self._build_prompt_input(
                context,
                trigger_type="user",
            )

            self._generate_response(context, prompt_input, output_definitions)

            self._process_pending_events(context)
            logger.info("[ChatAgent] ══════════════════════════════════════════")
        finally:
            if acquired:
                context._generate_lock.release()

    # ── 构建 PromptInput ──

    def _build_prompt_input(
        self,
        context: ChatAgentContext,
        *,
        trigger_type: str = "user",
        response_hint: str = "",
    ) -> PromptInput:
        """从 Agent 内部状态构建 PromptInput (4 层).

        Phase 4.2: L3(Mode)/L4(TaskBrief)/L5(Memory) 已移除，
        对应信息由 LLM 按需通过工具调用获取。
        """
        # L2: Persona snapshot — prefer OC, fallback to local
        persona_snapshot = ""
        if context.persona_mgr:
            persona_snapshot = context.persona_mgr.get_snapshot()

        # L3: 持续性环境状态快照
        env_state = ""
        if context.memory:
            env_state = context.memory.get_environment_state(max_length=500)
        if not env_state and context.cached_perception:
            env_state = context.cached_perception.scene_summary

        # L4: 离散事件（从 PerceptionBuffer 获取，已由 record_perception 写入）
        perception_events = []
        if context.memory:
            perception_events = context.memory.get_recent_perception_events(max_age=60.0)

        # Drain OC background notifications and pending approvals into memory
        from handlers.agent.oc_bridge.oc_prompt_injection import (
            drain_task_notifications,
            inject_pending_approvals,
        )
        drain_task_notifications(context.task_queue, context.memory)
        inject_pending_approvals(context.pending_confirmations, context.memory)

        return PromptInput(
            trigger_type=trigger_type,
            response_hint=response_hint,
            persona_snapshot=persona_snapshot,
            environment_state=env_state,
            perception_events=perception_events,
            dialogue_history=(
                context.memory.get_dialogue_for_llm(context.config.max_dialogue_turns)
                if context.memory else []
            ),
        )

    # ── LLM 调用 + 流式输出 + Agent Loop ──

    def _generate_response(
        self,
        context: ChatAgentContext,
        prompt_input: PromptInput,
        output_definitions: Dict[ChatDataType, HandlerDataInfo],
    ):
        output_definition = output_definitions.get(ChatDataType.AVATAR_TEXT).definition
        streamer = context.data_submitter.get_streamer(ChatDataType.AVATAR_TEXT)

        if context.llm_client is None:
            logger.error("[ChatAgent] LLM 客户端不可用")
            output = DataBundle(output_definition)
            output.set_main_data("抱歉，我暂时无法处理您的请求，请稍后再试。")
            streamer.stream_data(output, finish_stream=True)
            context.is_generating = False
            return

        stream_key = streamer.current_stream.identity.stream_key_str if streamer.current_stream is not None else None
        if stream_key is None:
            stream = streamer.new_stream(
                sources=[],
                config=ChatStreamConfig(cancelable=True),
            )
            stream_key = stream.stream_key_str

        compiled = context.compiler.compile(prompt_input)
        messages = compiled.full_messages

        logger.info(
            f"[ChatAgent] PromptCompiler: system={len(compiled.system_message)} chars, "
            f"messages={compiled.message_count}"
        )

        self._log_incomplete_work_summary(context)
        self._debug_log_prompt(context, compiled)

        if stream_key:
            context.active_stream_keys.add(stream_key)

        try:
            full_response = self._agent_loop(
                context, messages, output_definition, streamer, stream_key,
            )

            if full_response is None:
                context.is_generating = False
                return

            logger.info(f"[ChatAgent] 回复: '{full_response[:80]}...'")

            if full_response and context.memory:
                context.memory.record_assistant_response(full_response)
                self._check_compact(context)

        except Exception as e:
            logger.error(f"[ChatAgent] LLM 调用失败: {e}")
            output = DataBundle(output_definition)
            output.set_main_data("抱歉，我暂时无法处理您的请求，请稍后再试。")
            streamer.stream_data(output, finish_stream=True)
            context.is_generating = False
            return

        if stream_key:
            context.active_stream_keys.discard(stream_key)
        end_output = DataBundle(output_definition)
        end_output.set_main_data("")
        streamer.stream_data(end_output, finish_stream=True)

        context.is_generating = False
        context.last_interaction_time = time.time()

    @staticmethod
    def _apply_llm_extra_body(context: ChatAgentContext, kwargs: dict) -> None:
        """百炼 OpenAI 兼容接口需通过 extra_body 传 enable_thinking"""
        api_url = context.config.api_url
        if not api_url or "dashscope" not in api_url.lower():
            return
        extra = dict(kwargs.get("extra_body") or {})
        extra["enable_thinking"] = context.config.enable_thinking
        kwargs["extra_body"] = extra

    def _agent_loop(
        self,
        context: ChatAgentContext,
        messages: List[dict],
        output_definition,
        streamer,
        stream_key: Optional[str],
    ) -> Optional[str]:
        """Multi-step agent loop: LLM call → tool_use → feedback → repeat.

        Returns the final text response, or None if cancelled.
        """
        registry = context.tool_registry
        use_tools = (
            registry is not None
            and registry.has_tools()
            and context.config.tool_use.enabled
        )
        max_rounds = context.config.tool_use.max_tool_rounds

        for round_idx in range(max_rounds):
            tools_param = registry.get_schemas() if use_tools else None

            kwargs = dict(
                model=context.config.llm_model,
                messages=messages,
                stream=True,
            )
            if tools_param:
                kwargs["tools"] = tools_param

            self._apply_llm_extra_body(context, kwargs)

            response = context.llm_client.chat.completions.create(**kwargs)

            full_text, tool_calls, cancelled = self._stream_response(
                context, response, output_definition, streamer, stream_key,
            )

            if cancelled:
                logger.info("[ChatAgent] Stream cancelled during agent loop")
                return None

            if not tool_calls:
                return full_text

            # LLM requested tool calls — execute and continue the loop
            logger.info(
                f"[ChatAgent] Agent loop round {round_idx + 1}: "
                f"{len(tool_calls)} tool call(s)"
            )

            assistant_msg = {"role": "assistant", "content": full_text or None}
            assistant_msg["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["name"],
                        "arguments": tc["arguments"],
                    },
                }
                for tc in tool_calls
            ]
            messages.append(assistant_msg)

            interrupted_during_tools = False
            for tc in tool_calls:
                if stream_key and stream_key not in context.active_stream_keys:
                    logger.info(
                        f"[ChatAgent] Interrupted before tool '{tc['name']}', "
                        f"skipping remaining {len(tool_calls)} tool call(s)"
                    )
                    interrupted_during_tools = True
                    break

                args = {}
                try:
                    args = json.loads(tc["arguments"]) if tc["arguments"] else {}
                except json.JSONDecodeError:
                    logger.warning(
                        f"[ChatAgent] Failed to parse tool args: {tc['arguments'][:100]}"
                    )

                result = registry.execute(tc["name"], args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result.to_content_str(),
                })
                logger.info(
                    f"[ChatAgent]   tool={tc['name']} → "
                    f"{result.to_content_str()[:120]}"
                )

            if interrupted_during_tools:
                logger.info("[ChatAgent] Agent loop aborted due to interrupt during tool execution")
                return None

            # Skip nag when this round already resolved approvals — the
            # tool itself marks items confirmed/denied so a nag right after
            # would be stale noise.
            # resolved_this_round = any(
            #     tc["name"] in ("exec_approve", "pending_confirmations")
            #     for tc in tool_calls
            # )
            if context.pending_confirmations:
                context.pending_confirmations.tick_round()
                nag = context.pending_confirmations.get_nag_reminder()
                if nag:
                    messages.append({"role": "user", "content": nag})
                    logger.info("[ChatAgent] Injected pending-confirmations nag reminder")

        logger.warning(
            f"[ChatAgent] Agent loop reached max rounds ({max_rounds}), "
            "forcing text response"
        )
        return full_text

    def _stream_response(
        self,
        context: ChatAgentContext,
        response,
        output_definition,
        streamer,
        stream_key: Optional[str],
    ) -> tuple:
        """Stream an LLM response, accumulating text and tool_calls.

        Returns (full_text, tool_calls_list, cancelled).
        tool_calls_list is a list of dicts: [{"id", "name", "arguments"}, ...]
        """
        full_text = ""
        tool_calls_accum: Dict[int, dict] = {}
        cancelled = False

        for chunk in response:
            if stream_key and stream_key not in context.active_stream_keys:
                cancelled = True
                try:
                    response.close()
                except Exception:
                    pass
                break

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            if delta.content:
                full_text += delta.content
                output = DataBundle(output_definition)
                output.set_main_data(delta.content)
                streamer.stream_data(output)

            if delta.tool_calls:
                for tc_delta in delta.tool_calls:
                    idx = tc_delta.index
                    if idx not in tool_calls_accum:
                        tool_calls_accum[idx] = {
                            "id": "",
                            "name": "",
                            "arguments": "",
                        }
                    entry = tool_calls_accum[idx]
                    if tc_delta.id:
                        entry["id"] = tc_delta.id
                    if tc_delta.function:
                        if tc_delta.function.name:
                            entry["name"] = tc_delta.function.name
                        if tc_delta.function.arguments:
                            entry["arguments"] += tc_delta.function.arguments

        tool_calls_list = [
            tool_calls_accum[idx]
            for idx in sorted(tool_calls_accum.keys())
        ] if tool_calls_accum else []

        return full_text, tool_calls_list, cancelled

    def _check_compact(self, context: ChatAgentContext):
        """检查并触发对话上下文自动压缩。"""
        if context.memory and context.memory.should_compact() and context.llm_client:
            compact_model = (
                context.config.context_compact.compact_model
                or context.config.llm_model
            )
            env_state = ""
            if context.memory:
                env_state = context.memory.perception_buffer.get_state_summary()
            task_brief = ""
            if context.task_mirror:
                task_brief = context.task_mirror.get_active_brief()
            context.memory.check_and_compact(
                context.llm_client, compact_model,
                task_brief=task_brief, env_state=env_state,
            )

    # ── 事件工具方法 ──

    def _should_skip_event(
        self, context: ChatAgentContext, event: EnvironmentEvent, cooldown: float
    ) -> bool:
        last = context.responded_events.get(event.event_type)
        if last is None:
            return False
        return (time.time() - last) <= cooldown

    def _process_pending_events(self, context: ChatAgentContext):
        """合并所有有效 pending events 为一次 LLM 调用。"""
        if not context.pending_events or not context.output_definitions:
            return

        max_event_age = 15.0
        now = time.time()

        valid_events: List[EnvironmentEvent] = []
        valid_cfgs: List[Optional[EventTriggerConfig]] = []

        while context.pending_events:
            event = context.pending_events.pop(0)
            age = now - event.timestamp if event.timestamp > 0 else 0.0

            if age > max_event_age:
                logger.info(f"[ChatAgent] 丢弃过期事件: {event.event_type} (age={age:.1f}s)")
                continue

            trigger_cfg = context.config.proactive.event_triggers.get(event.event_type)
            if trigger_cfg and not trigger_cfg.enabled:
                continue

            cooldown = trigger_cfg.cooldown if trigger_cfg else 30.0
            if self._should_skip_event(context, event, cooldown):
                continue

            valid_events.append(event)
            valid_cfgs.append(trigger_cfg)

        if valid_events:
            event_names = ", ".join(ev.event_type for ev in valid_events)
            logger.info(
                f"[ChatAgent] 合并处理 {len(valid_events)} 个待处理事件: {event_names}"
            )
            self._handle_proactive_response(
                context, valid_events, context.output_definitions, valid_cfgs
            )

    @staticmethod
    def _event_importance(event: EnvironmentEvent) -> float:
        if event.urgency == "critical":
            return 0.9
        elif event.urgency == "high":
            return 0.7
        return 0.5

    # ── 空闲触发 ──

    def _idle_trigger_loop(self, context: ChatAgentContext):
        """后台线程：检测用户空闲并触发主动对话（含待确认项提醒）。

        唤醒方式（取最先到达的）：
        - _proactive_wake 被 set → 立即唤醒（如 approval 到达）
        - 固定 check_interval 超时
        - _idle_stop 终止信号
        """
        check_interval = 2.0
        # Grace period after approval arrives, lets ongoing streaming finish
        approval_grace_seconds = 1

        while not context._idle_stop.is_set():
            # Block until wake signal or timeout
            woken = context._proactive_wake.wait(timeout=check_interval)
            if woken:
                context._proactive_wake.clear()

            if context._idle_stop.is_set():
                break
            if context.is_generating or not context.output_definitions:
                continue

            elapsed = time.time() - context.last_interaction_time
            pc_cfg = context.config.proactive.pending_confirmation_trigger

            # Immediate approval trigger: wake signal + pending items →
            # skip idle_seconds, only respect cooldown
            if (
                woken
                and pc_cfg.enabled
                and context.pending_confirmations
                and context.pending_confirmations.has_pending()
                and not self._should_skip_event(
                    context,
                    EnvironmentEvent(event_type="pending_confirmation"),
                    pc_cfg.cooldown,
                )
            ):
                # Brief grace to let any in-flight streaming settle
                time.sleep(approval_grace_seconds)
                if context.is_generating:
                    continue
                logger.info(
                    "[ChatAgent] Approval 即时主动触发 (proactive_wake)"
                )
                self._fire_pending_confirmation(context, pc_cfg)
                continue

            # Periodic pending-confirmation reminder (original idle-based path)
            if (
                pc_cfg.enabled
                and context.pending_confirmations
                and context.pending_confirmations.has_pending()
                and elapsed >= pc_cfg.idle_seconds
                and not self._should_skip_event(
                    context,
                    EnvironmentEvent(event_type="pending_confirmation"),
                    pc_cfg.cooldown,
                )
            ):
                logger.info(
                    f"[ChatAgent] 待确认主动触发: "
                    f"elapsed={elapsed:.0f}s >= {pc_cfg.idle_seconds:.0f}s"
                )
                self._fire_pending_confirmation(context, pc_cfg)
                continue

            if context._idle_triggered:
                continue

            idle_cfg = context.config.proactive.idle_trigger
            if not idle_cfg.enabled:
                continue

            current_mode = (
                context.memory.session_mode if context.memory else "chitchat"
            )
            threshold = idle_cfg.mode_overrides.get(
                current_mode, idle_cfg.idle_seconds
            )

            if elapsed >= threshold:
                logger.info(
                    f"[ChatAgent] 空闲触发: "
                    f"{elapsed:.0f}s >= {threshold:.0f}s (mode={current_mode})"
                )
                idle_event = EnvironmentEvent(
                    event_type="idle",
                    description="用户已安静一段时间",
                    confidence=1.0,
                    urgency="low",
                    timestamp=time.time(),
                )
                idle_trigger_cfg = EventTriggerConfig(
                    hint=idle_cfg.hint,
                    cooldown=threshold,
                )
                self._handle_proactive_response(
                    context,
                    [idle_event],
                    context.output_definitions,
                    [idle_trigger_cfg],
                )
                context._idle_triggered = True

    def _fire_pending_confirmation(
        self,
        context: ChatAgentContext,
        pc_cfg: PendingConfirmationTriggerConfig,
    ):
        """触发一次 pending-confirmation 主动响应。"""
        pc_event = EnvironmentEvent(
            event_type="pending_confirmation",
            description=context.pending_confirmations.render(),
            confidence=1.0,
            urgency="high",
            timestamp=time.time(),
        )
        pc_trigger_cfg = EventTriggerConfig(
            hint=pc_cfg.hint,
            cooldown=pc_cfg.cooldown,
        )
        self._handle_proactive_response(
            context, [pc_event], context.output_definitions, [pc_trigger_cfg]
        )

    # ── OC Bridge 初始化 ──

    @staticmethod
    def _init_oc_bridge(context: ChatAgentContext):
        """Delegate to ``oc_bridge.oc_bridge_init`` for all OC component wiring."""
        from handlers.agent.oc_bridge.oc_bridge_init import init_oc_bridge
        init_oc_bridge(context)

    # ── ToolRegistry 构建 ──

    @staticmethod
    def _build_tool_registry(config: ChatAgentConfig) -> ToolRegistry:
        registry = ToolRegistry()

        if config.tool_use.enabled and config.tool_use.register_demo_tools:
            from handlers.agent.tools.demo_tools import GetCurrentTimeTool, GetSystemInfoTool
            registry.register(GetCurrentTimeTool())
            registry.register(GetSystemInfoTool())

        logger.info(
            f"[ChatAgent] ToolRegistry initialized with {len(registry.tool_names)} tools: "
            f"{registry.tool_names}"
        )
        return registry

    # ── Debug Logging ──

    def _log_incomplete_work_summary(self, context: "ChatAgentContext"):
        """Print a one-shot INFO summary of unfinished work (queue, approvals, mirror)."""
        lines: List[str] = []

        if context.task_queue and context.task_queue.size > 0:
            for n in context.task_queue.peek():
                summary = (n.result_summary or "").replace("\n", " ")[:120]
                lines.append(
                    f"  [task_queue] {n.task_id} | {n.status} | {summary}"
                )

        if context.pending_confirmations and context.pending_confirmations.has_pending():
            for item in context.pending_confirmations.get_pending_items():
                txt = (item.text or "").replace("\n", " ")[:120]
                lines.append(
                    f"  [pending_confirm] id={item.id} | {txt}"
                )

        if context.task_mirror:
            active = context.task_mirror.get_active_tasks()
            for t in active:
                brief = (t.brief or "").replace("\n", " ")[:80]
                lines.append(
                    f"  [task_mirror] {t.task_id} | {t.status} | {t.title} | {brief}"
                )

        if lines:
            logger.debug(
                "[ChatAgent] 未完成事项 ({} 条):\n{}",
                len(lines),
                "\n".join(lines),
            )
        else:
            logger.debug("[ChatAgent] 未完成事项: 无")

    def _debug_log_prompt(
        self,
        context: "ChatAgentContext",
        compiled,
    ):
        """Log environment state, full system prompt (line-by-line), messages, and tool list.

        Tools are **not** embedded in the system string; they are sent as the API `tools` argument
        (see `_agent_loop`). L1 stable_core only contains prose "## 工具使用" instructions.
        """
        sys_text = compiled.system_message
        # 只匹配 PromptCompiler 注入的真实 L6 块（行首 <environment-state>），
        # 避免误匹配 L1 说明文字里的「- <environment-state> …」
        env_match = re.search(
            r"^<environment-state>\s*\n",
            sys_text,
            re.MULTILINE,
        )
        if env_match:
            env_start = env_match.start()
            env_end = sys_text.find("</environment-state>", env_start)
            env_section = (
                sys_text[env_start: env_end + len("</environment-state>")]
                if env_end >= 0
                else sys_text[env_start:]
            )
            logger.debug("[ChatAgent] ─── Environment State (L3, real block) ───")
            for line in env_section.splitlines():
                logger.debug("[ChatAgent]   {}", line)
        else:
            logger.debug(
                "[ChatAgent] ─── Environment State (L3): (empty — 无感知快照或未注入) ───"
            )

        # Full system message: one log record per line so newlines are readable and nothing is truncated
        logger.debug(
            "[ChatAgent] ─── System Message (full, {} chars, L1–L3) ───",
            len(sys_text),
        )
        for lineno, line in enumerate(sys_text.splitlines(), start=1):
            logger.debug("[ChatAgent]   sys {:4d} | {}", lineno, line)

        use_tools = (
            context.tool_registry is not None
            and context.tool_registry.has_tools()
            and context.config.tool_use.enabled
        )
        if use_tools:
            schemas = context.tool_registry.get_schemas()
            logger.debug(
                "[ChatAgent] ─── Tool definitions (OpenAI `tools` param, NOT in system prompt) ─── "
                "count={}",
                len(schemas),
            )
            for s in schemas:
                fn = s.get("function", {})
                name = fn.get("name", "?")
                desc = (fn.get("description") or "").replace("\n", " ")
                logger.debug("[ChatAgent]   tool: {} | {}", name, desc[:300])
        else:
            logger.debug(
                "[ChatAgent] ─── Tools: disabled or none (not passed to LLM) ───"
            )

        logger.debug("[ChatAgent] ─── Chat messages (full_messages, incl. L4) ───")
        for i, msg in enumerate(compiled.full_messages):
            role = msg.get("role", "?")
            content = msg.get("content")
            if content is None or content == "":
                logger.debug("[ChatAgent]   [{}] {}: (no content)", i, role)
                continue
            body = content if isinstance(content, str) else str(content)
            logger.debug("[ChatAgent]   [{}] {} ({} chars) ───", i, role, len(body))
            for line in body.splitlines():
                logger.debug("[ChatAgent]       {}", line)
        logger.debug("[ChatAgent] ─── End prompt debug ───")

    # ── PromptCompiler 构建 ──

    @staticmethod
    def _build_compiler(config: ChatAgentConfig) -> PromptCompiler:
        layer_configs = {
            LAYER_PERSONA_SNAPSHOT: PromptLayerConfig(
                section_header="【人格】",
                max_chars=config.persona_max_chars,
            ),
            LAYER_ENVIRONMENT_STATE: PromptLayerConfig(
                max_chars=config.perception_max_chars,
            ),
        }
        return PromptCompiler(
            stable_core=(
                f"{config.stable_core.rstrip()}\n\n"
                f"{MANDATORY_DELEGATION_POLICY}\n\n"
                f"{REALTIME_AND_TRUTH_POLICY}"
            ),
            persona_snapshot=config.persona_snapshot,
            layer_configs=layer_configs,
            max_dialogue_turns=config.compiler_dialogue_turns,
        )

    # ── 生命周期 ──

    def destroy_context(self, context: HandlerContext):
        context = cast(ChatAgentContext, context)
        context._idle_stop.set()
        if context.oc_channel_client:
            try:
                context.oc_channel_client.stop()
            except Exception:
                pass
        if context.oc_mcp_client:
            try:
                context.oc_mcp_client.stop()
            except Exception:
                pass
        if context.memory:
            context.memory.destroy()
        context.compiler = None
        context.tool_registry = None
        context.oc_mcp_client = None
        context.oc_channel_client = None
        context.persona_mgr = None
        context.task_queue = None
        context.task_mirror = None
        context.pending_confirmations = None
        logger.info(f"ChatAgentContext destroyed for session {context.session_id}")
