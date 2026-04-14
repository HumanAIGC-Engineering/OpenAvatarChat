"""
SpawnAgentTool — unified entry point for spawning sub-agents.

LLM decides when to spawn a sub-agent, which type, and whether it runs async.
Supports two backends:
  - local: fork independent messages[], run LLM loop, return summary
  - oc: delegate to OpenClaw via oac-bridge HTTP channel, return result
"""

import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from loguru import logger

from handlers.agent.tools.base_tool import BaseTool, ToolResult


@dataclass
class AgentDef:
    """Definition of a sub-agent type (data-driven)."""
    name: str
    when_to_use: str
    model: str = "qwen-turbo"
    system_prompt: str = ""
    allowed_tools: List[str] = field(default_factory=list)
    async_default: bool = True
    backend: str = "local"  # "local" | "oc" | "auto"
    max_rounds: int = 3


DEFAULT_AGENT_DEFS: Dict[str, AgentDef] = {
    "explore": AgentDef(
        name="explore",
        when_to_use="搜索、分析、理解信息，只读操作。适合需要查找记忆或理解上下文的场景。",
        model="qwen-turbo",
        system_prompt="你是一个信息搜索和分析助手。请搜索相关信息并给出精炼的分析摘要。",
        allowed_tools=["memory_search"],
        async_default=True,
        backend="local",
        max_rounds=3,
    ),
    "analyst": AgentDef(
        name="analyst",
        when_to_use="多步推理分析，整理报告。适合需要综合多个信息源进行分析的场景。",
        model="qwen-plus",
        system_prompt="你是一个分析助手。请综合分析提供的信息，输出结构化的分析报告。",
        allowed_tools=["memory_search"],
        async_default=True,
        backend="local",
        max_rounds=5,
    ),
    "oc_delegate": AgentDef(
        name="oc_delegate",
        when_to_use="需要 OpenClaw 完整 agent 能力的复杂后台任务。如文件操作、代码执行、定时任务管理等。",
        model="",
        system_prompt="",
        allowed_tools=[],
        async_default=True,
        backend="oc",
        max_rounds=1,
    ),
}


class SpawnAgentTool(BaseTool):
    """Unified tool for spawning sub-agents of different types."""

    def __init__(
        self,
        agent_defs: Optional[Dict[str, AgentDef]] = None,
        llm_client=None,
        oc_channel_client=None,
        tool_registry=None,
        oac_session_id: str = "",
    ):
        self._agent_defs = agent_defs or DEFAULT_AGENT_DEFS
        self._llm_client = llm_client
        self._oc_channel_client = oc_channel_client
        self._tool_registry = tool_registry
        self._oac_session_id = oac_session_id

    @property
    def name(self) -> str:
        return "spawn_agent"

    @property
    def description(self) -> str:
        type_descs = []
        for name, defn in self._agent_defs.items():
            type_descs.append(f"  - {name}: {defn.when_to_use}")
        types_str = "\n".join(type_descs)
        return (
            f"创建一个子 Agent 来处理独立任务。子 Agent 有自己的上下文，"
            f"完成后只返回结果摘要。"
            f"当用户要求设置提醒、创建/修改/取消日程、安排后台任务、执行多步骤功能操作时，"
            f"应优先使用本工具把任务交给 OpenClaw，而不是直接口头声称“已完成”。"
            f"\n\n可用的 agent 类型：\n{types_str}"
        )

    @property
    def parameters(self) -> dict:
        type_names = list(self._agent_defs.keys())
        return {
            "type": "object",
            "properties": {
                "subagent_type": {
                    "type": "string",
                    "enum": type_names,
                    "description": "子 Agent 类型",
                },
                "prompt": {
                    "type": "string",
                    "description": "交给子 Agent 的任务描述",
                },
                "run_background": {
                    "type": "boolean",
                    "description": "是否异步执行（默认 true）",
                },
            },
            "required": ["subagent_type", "prompt"],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        agent_type = args.get("subagent_type", "explore")
        prompt = args.get("prompt", "")
        run_bg = args.get("run_background", True)

        if not prompt:
            return ToolResult(success=False, error="prompt is required")

        agent_def = self._agent_defs.get(agent_type)
        if not agent_def:
            return ToolResult(
                success=False,
                error=f"Unknown agent type: {agent_type}. "
                      f"Available: {list(self._agent_defs.keys())}",
            )

        backend = agent_def.backend
        if backend == "auto":
            backend = "oc" if self._oc_channel_client else "local"

        logger.info(
            f"[SpawnAgent] Spawning '{agent_type}' (backend={backend}, bg={run_bg})"
        )

        if backend == "oc":
            return self._execute_oc(agent_def, prompt, run_bg)
        return self._execute_local(agent_def, prompt, run_bg)

    def _execute_local(
        self, agent_def: AgentDef, prompt: str, run_bg: bool
    ) -> ToolResult:
        """Run a local sub-agent with its own messages and LLM loop."""
        if not self._llm_client:
            return ToolResult(success=False, error="No LLM client for local agent")

        start = time.time()
        messages = [
            {"role": "system", "content": agent_def.system_prompt or "你是一个助手。"},
            {"role": "user", "content": prompt},
        ]

        final_text = ""
        for round_idx in range(agent_def.max_rounds):
            try:
                resp = self._llm_client.chat.completions.create(
                    model=agent_def.model,
                    messages=messages,
                    tools=self._build_tool_specs(agent_def.allowed_tools),
                )
                choice = resp.choices[0]

                if choice.finish_reason == "stop":
                    final_text = choice.message.content or ""
                    break

                if choice.message.tool_calls:
                    messages.append(choice.message)
                    for tc in choice.message.tool_calls:
                        fn = tc.function
                        tool_args = json.loads(fn.arguments) if fn.arguments else {}
                        tool = (
                            self._tool_registry.get(fn.name)
                            if self._tool_registry
                            else None
                        )
                        if tool:
                            result = tool.execute(tool_args)
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": result.to_content_str(),
                            })
                        else:
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": '{"error": "no tool registry"}',
                            })
            except Exception as e:
                logger.error(f"[SpawnAgent] local agent round {round_idx} failed: {e}")
                break

        duration = time.time() - start
        logger.info(
            f"[SpawnAgent] local agent '{agent_def.name}' done in {duration:.1f}s, "
            f"result: {len(final_text)} chars"
        )

        return ToolResult(
            success=True,
            data={
                "content": final_text or "(子 Agent 未返回内容)",
                "agent_type": agent_def.name,
                "backend": "local",
                "duration_ms": int(duration * 1000),
            },
        )

    def _execute_oc(
        self, agent_def: AgentDef, prompt: str, run_bg: bool
    ) -> ToolResult:
        """Delegate to OpenClaw via oac-bridge HTTP channel."""
        if not self._oc_channel_client:
            return ToolResult(success=False, error="OC channel client not available")
        if not self._oac_session_id:
            return ToolResult(success=False, error="No OAC session ID configured")

        start = time.time()
        result = self._oc_channel_client.send_message(
            oac_session_id=self._oac_session_id,
            text=prompt,
            sender_name="OAC Agent",
        )

        if "error" in result:
            return ToolResult(success=False, error=result["error"])

        if run_bg:
            duration = time.time() - start
            return ToolResult(
                success=True,
                data={
                    "status": "submitted_async",
                    "content": "任务已通过 OAC Bridge 渠道提交给 OpenClaw 处理，完成后会通知你。",
                    "agent_type": agent_def.name,
                    "backend": "oc_channel",
                    "oac_session_id": self._oac_session_id,
                    "duration_ms": int(duration * 1000),
                },
            )

        reply_msg = self._oc_channel_client.reply_queue.wait_for_reply(
            self._oac_session_id, timeout=60.0
        )
        duration = time.time() - start

        reply_text = reply_msg.text if reply_msg else ""
        return ToolResult(
            success=True,
            data={
                "content": reply_text or "OC 已接收任务（暂无即时结果）",
                "agent_type": agent_def.name,
                "backend": "oc_channel",
                "oac_session_id": self._oac_session_id,
                "duration_ms": int(duration * 1000),
            },
        )

    def _build_tool_specs(self, allowed_tools: List[str]) -> Optional[List[dict]]:
        if not allowed_tools or not self._tool_registry:
            return None
        specs = []
        for tool_name in allowed_tools:
            tool = self._tool_registry.get(tool_name)
            if tool:
                specs.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.parameters,
                    },
                })
        return specs if specs else None
