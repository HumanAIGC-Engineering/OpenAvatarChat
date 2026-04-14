"""
PromptCompiler — 4 层 Prompt 编排器

人格原档在 OC；实时 system/context 的最终组装在 OAC。
OAC 每轮 prompt 按以下 4 层重建，不照搬 OC 的 system prompt。

4 层架构:
  L1 Stable Core         — OAC 自身的实时规则、安全边界、输出约束 + 工具使用引导
  L2 Persona Snapshot    — 从 OC 人格主档编译的精简快照
  L3 Environment State   — 持续性环境状态快照，<environment-state> 包裹，尾部注入
  L4 Recent Dialogue     — 离散事件 <observation> + 对话历史 + 当前用户消息

L1-L3 拼入 system message（L3 贴近尾部）；L4 拼入 messages 列表。

原 L3(Mode)、L4(TaskBrief)、L5(RetrievedMemory) 已移除 (Phase 4.2)，
对应信息改为 LLM 按需通过工具调用获取。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from loguru import logger

# ── Layer 常量 ──

LAYER_STABLE_CORE = "stable_core"
LAYER_PERSONA_SNAPSHOT = "persona_snapshot"
LAYER_ENVIRONMENT_STATE = "environment_state"
LAYER_RECENT_DIALOGUE = "recent_dialogue"

ALL_LAYERS = [
    LAYER_STABLE_CORE,
    LAYER_PERSONA_SNAPSHOT,
    LAYER_ENVIRONMENT_STATE,
    LAYER_RECENT_DIALOGUE,
]


# ── 数据模型 ──

@dataclass
class PromptInput:
    """ChatAgent 内部传给 PromptCompiler 的上下文，不做跨 handler 序列化。"""
    user_message: str = ""
    trigger_type: str = "user"          # user / event
    response_hint: str = ""             # 事件触发时的自由文本描述
    persona_snapshot: str = ""          # 空 = 用 Compiler 本地默认
    environment_state: str = ""         # L3 持续性环境状态
    perception_events: List[Dict] = field(default_factory=list)
    dialogue_history: List[Dict] = field(default_factory=list)


@dataclass
class PromptLayerConfig:
    """单层的配置。"""
    enabled: bool = True
    max_chars: int = 0          # 0 = 不限制
    section_header: str = ""    # 段头标记，如 "【人格】"


@dataclass
class CompiledPrompt:
    """PromptCompiler 的输出，可直接传给 LLM。"""
    system_message: str = ""
    messages: List[Dict[str, str]] = field(default_factory=list)

    @property
    def full_messages(self) -> List[Dict[str, str]]:
        result = []
        if self.system_message:
            result.append({"role": "system", "content": self.system_message})
        result.extend(self.messages)
        return result

    @property
    def message_count(self) -> int:
        return len(self.messages) + (1 if self.system_message else 0)

    def __repr__(self) -> str:
        return (
            f"CompiledPrompt(system={len(self.system_message)} chars, "
            f"messages={len(self.messages)})"
        )


# ── 默认层配置 ──

DEFAULT_LAYER_CONFIGS: Dict[str, PromptLayerConfig] = {
    LAYER_STABLE_CORE: PromptLayerConfig(),
    LAYER_PERSONA_SNAPSHOT: PromptLayerConfig(
        section_header="【人格】",
    ),
    LAYER_ENVIRONMENT_STATE: PromptLayerConfig(
        max_chars=800,
    ),
    LAYER_RECENT_DIALOGUE: PromptLayerConfig(),
}


# ── 默认文本 ──

DEFAULT_STABLE_CORE = """\
你是一个具有视觉能力的实时数字人助手，正在通过摄像头与用户进行面对面对话。

## 输出约束
- 用口语化的自然语言回答，语气亲切
- 保持简短（通常 2-3 句），除非用户明确要求详细说明
- 不要输出 Markdown 格式、代码块或列表符号
- 不要自称"AI"或"语言模型"，你就是这个数字人角色本身

## 视觉规则
- <environment-state> 标签描述的是你当前看到的持续性环境状态
- 可以自然地提及观察到的内容，但不要每句都提
- 当用户问"你能看到我吗"且有环境描述时，肯定回答并描述

## 工具使用
你拥有以下能力，在合适时机主动使用：
- 当用户提到过去的事、偏好、之前的约定时 → 用 memory_search 搜索长期记忆
- 当用户问"给你布置过什么任务"、定时提醒、日程时 → 用 list_scheduled_tasks 查看
- 当不确定用户称呼或自身角色设定时 → 用 get_agent_profile 获取
- 当用户的问题需要实时数据（如时间、天气）时 → 使用对应工具
- 某些工具是异步的，调用后你会收到 {"status": "submitted"} 状态，请据此自行决定回复
- 工具返回结果后，用自然口语将结果融入回复，不要原样复述 JSON

## 结构化标签说明
你会在对话中收到以下结构化标签：
- <environment-state>: 当前环境的持续状态描述，作为背景知识理解，不要当作刚发生的事。
- <observation event="true">: 刚发生的环境事件，你应考虑是否需要回应。
- <observation compact="true">: 历史感知摘要，仅供参考。
- <background-results>: 后台任务完成通知，你可自主决定是否告知用户。
- <dialogue-summary>: 之前对话的压缩摘要，帮助你延续上下文。
- <reminder>: 系统提醒你有未完成的待确认事项，请提醒用户处理。

## 审批流程
当后台任务通知中包含待审批请求（exec approval）时：
1. 用 pending_confirmations 工具记录该待确认项（status=pending, source=exec_approval）
2. 用自然语言告知用户审批内容，询问是否同意
3. 用户回答后，用 exec_approve 工具发送审批决策
4. 用 pending_confirmations 工具更新状态为 confirmed/denied"""

DEFAULT_PERSONA_SNAPSHOT = """\
性格：友善亲切，像朋友一样交流。观察细致，能注意到用户状态变化。
口吻：轻松自然，适当关心用户情绪。"""

MANDATORY_DELEGATION_POLICY = """\
## OAC-OC 协作边界（强约束）
你在系统中的角色是“前台/管家”。真正的功能执行由 OpenClaw (OC) 后台完成。

- 凡是“功能性任务”或“较复杂任务”，都必须先调用工具，不要直接口头承诺已经完成。
- 功能性任务示例：设置/修改/取消提醒与日程、创建/执行任务、跨步骤操作、需要后台持续跟踪的事务。
- 当任务需要 OC 执行时，优先调用 spawn_agent，参数使用 subagent_type="oc_delegate"。
- 在得到工具返回前，不得说“已完成”。若工具返回 submitted_async，应明确告知“已提交给 OpenClaw 后台处理”。

### 后台审批处理
- <background-results> 或 <pending-approvals> 中出现审批请求时，表示 OC 后台正等你批准。
- 第一步：用自然口语向用户说明后台需要执行什么命令，并告知三种选项：仅这次同意、始终允许、拒绝。
- 第二步：根据用户回答调用 exec_approve，decision 为 "allow-once"（仅这次）、"allow-always"（始终允许同类命令）或 "deny"（拒绝）。
- 当同一任务已连续多次弹出审批时，应主动建议用户选择“始终允许”以减少打扰。
- 关键：口头说“已批准”“已确认”完全无效！只有调用 exec_approve 工具才能真正批准。不调用工具，后台审批会一直卡着。
- 不要忽略审批通知，不要自行替用户做决定。
"""

REALTIME_AND_TRUTH_POLICY = """\
## 真实性与实时信息（强约束）
- 当前时间、日期、星期、天气、系统状态等实时信息，必须以工具返回为准。
- 遇到“现在几点”“今天星期几”这类问题，先调用对应工具，再作答。
- 不要根据历史对话、先前回复、上下文联想或模型记忆猜测当前时间。
- 对任务状态同样如此：只有拿到工具结果，才能说“已创建”“已设置”“已生效”。否则只能说“我将提交处理”或“正在确认”。
"""


# ── PromptCompiler ──

class PromptCompiler:
    """
    4 层 Prompt 编排器。

    接收 PromptInput（ChatAgent 内部构造），输出 CompiledPrompt（直接传给 LLM）。

    用法::

        compiler = PromptCompiler()
        compiled = compiler.compile(prompt_input)
        messages = compiled.full_messages
    """

    def __init__(
        self,
        stable_core: str = DEFAULT_STABLE_CORE,
        persona_snapshot: str = DEFAULT_PERSONA_SNAPSHOT,
        layer_configs: Optional[Dict[str, PromptLayerConfig]] = None,
        max_dialogue_turns: Optional[int] = None,
    ):
        self.stable_core = stable_core
        self._persona_snapshot = persona_snapshot
        self.layer_configs = {**DEFAULT_LAYER_CONFIGS, **(layer_configs or {})}
        self.max_dialogue_turns = max_dialogue_turns

    # ── Persona Snapshot 动态更新 ──

    def update_persona_snapshot(self, snapshot: str):
        """OC 推送新的人格快照时调用。"""
        self._persona_snapshot = snapshot
        logger.info(f"[PromptCompiler] persona snapshot updated ({len(snapshot)} chars)")

    @property
    def persona_snapshot(self) -> str:
        return self._persona_snapshot

    # ── 核心编排 ──

    def compile(self, pi: PromptInput) -> CompiledPrompt:
        """
        将 PromptInput 编排为 CompiledPrompt。

        L1-L3 → system_message（L3 Environment State 尾部注入）
        L4    → messages 列表（离散事件 <observation> + 对话历史 + 当前轮）
        """
        system_parts: List[str] = []

        # L1 Stable Core（含工具使用引导 + 结构化标签解读指令）
        self._append_layer(system_parts, LAYER_STABLE_CORE, self.stable_core)

        # L2 Persona Snapshot — 优先使用 pi 中 OC 传来的，否则用本地默认
        snapshot = pi.persona_snapshot or self._persona_snapshot
        self._append_layer(system_parts, LAYER_PERSONA_SNAPSHOT, snapshot)

        # L3 Environment State — <environment-state> 包裹，尾部注入
        env_state = self._build_environment_state(pi)
        self._append_layer(system_parts, LAYER_ENVIRONMENT_STATE, env_state)

        system_message = "\n\n".join(system_parts)

        # L4 Recent Dialogue + 离散事件 <observation> + CurrentTurn
        messages = self._build_messages(pi)

        compiled = CompiledPrompt(
            system_message=system_message,
            messages=messages,
        )

        logger.debug(
            f"[PromptCompiler] compiled: system={len(system_message)} chars, "
            f"messages={len(messages)}, layers={len(system_parts)}"
        )
        return compiled

    # ── 各层构建 ──

    def _build_environment_state(self, pi: PromptInput) -> str:
        """L3: 用 <environment-state> 标签包裹持续性环境状态。"""
        if not pi.environment_state:
            return ""
        return (
            f"<environment-state>\n"
            f"{pi.environment_state}\n"
            f"</environment-state>"
        )

    def _build_messages(self, pi: PromptInput) -> List[Dict[str, str]]:
        """L4: 对话历史 + 离散事件 + 当前轮。"""
        cfg = self.layer_configs.get(LAYER_RECENT_DIALOGUE)
        if cfg and not cfg.enabled:
            return []

        messages: List[Dict[str, str]] = []

        # 对话历史
        history = pi.dialogue_history
        if self.max_dialogue_turns and len(history) > self.max_dialogue_turns:
            history = history[-self.max_dialogue_turns:]

        messages.extend(
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in history
            if m.get("content")
        )

        # 离散事件 → <observation event="true"> user messages
        for event in pi.perception_events:
            obs_msg = self._format_observation(event)
            if obs_msg:
                messages.append({"role": "user", "content": obs_msg})

        # 当前轮
        if pi.trigger_type == "user" and pi.user_message:
            messages.append({"role": "user", "content": pi.user_message})
        elif pi.trigger_type == "event":
            event_desc = pi.response_hint or "环境发生了变化，请根据情况自然回应。"
            messages.append({
                "role": "user",
                "content": (
                    f'<observation source="system" event="true">\n'
                    f'{event_desc}\n'
                    f'</observation>'
                ),
            })

        return messages

    @staticmethod
    def _format_observation(event: Dict) -> str:
        """将单个离散事件格式化为 <observation> 标签。"""
        content = event.get("content", "")
        if not content:
            return ""
        source = event.get("source", "camera")
        t = event.get("time", "")
        age = event.get("age_seconds", 0)
        age_str = f"{int(age)}s" if age else ""

        attrs = f'source="{source}"'
        if t:
            attrs += f' time="{t}"'
        if age_str:
            attrs += f' age="{age_str}"'
        attrs += ' event="true"'

        return f"<observation {attrs}>\n{content}\n</observation>"

    # ── 工具方法 ──

    def _append_layer(self, parts: List[str], layer_name: str, content: str):
        """根据配置追加一层内容。"""
        if not content:
            return

        cfg = self.layer_configs.get(layer_name)
        if cfg and not cfg.enabled:
            return

        if cfg and cfg.max_chars and len(content) > cfg.max_chars:
            content = content[:cfg.max_chars] + "…"

        if cfg and cfg.section_header:
            content = f"{cfg.section_header}\n{content}"

        parts.append(content)
