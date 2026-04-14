"""
OAC Prompt Compiler — 4 层 Prompt 编排

人格原档在 OC；实时 system/context 的最终组装在 OAC。

Layer Architecture (Phase 4.2):
  L1  Stable Core         OAC 自身的实时规则、安全边界、输出约束 + 工具使用引导
  L2  Persona Snapshot    从 OC 人格主档编译的精简快照
  L3  Environment State   持续性环境状态快照（<environment-state> 包裹，尾部注入 system prompt）
  L4  Recent Dialogue     离散事件 <observation> + 对话历史 + 当前用户消息

原 L3(Mode)、L4(TaskBrief)、L5(RetrievedMemory) 已移除，
对应信息改为 LLM 按需通过工具调用获取。
"""
from handlers.agent.prompt.prompt_compiler import (
    PromptCompiler,
    PromptInput,
    PromptLayerConfig,
    CompiledPrompt,
    LAYER_STABLE_CORE,
    LAYER_PERSONA_SNAPSHOT,
    LAYER_ENVIRONMENT_STATE,
    LAYER_RECENT_DIALOGUE,
    ALL_LAYERS,
)

__all__ = [
    "PromptCompiler",
    "PromptInput",
    "PromptLayerConfig",
    "CompiledPrompt",
    "LAYER_STABLE_CORE",
    "LAYER_PERSONA_SNAPSHOT",
    "LAYER_ENVIRONMENT_STATE",
    "LAYER_RECENT_DIALOGUE",
    "ALL_LAYERS",
]
