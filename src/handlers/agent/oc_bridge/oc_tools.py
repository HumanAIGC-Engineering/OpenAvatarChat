"""
OC Tools — adapts OpenClaw MCP tools to BaseTool for ToolRegistry.

These tools are exposed to the LLM so it can autonomously decide when
to search memory, retrieve agent profile, or list scheduled tasks.

All tools go through Plugin Tools MCP (no direct file reads).
"""

from typing import Any, Dict

from loguru import logger

from handlers.agent.tools.base_tool import BaseTool, ToolResult
from handlers.agent.oc_bridge.mcp_client import OcMcpClient


class OcMemorySearchTool(BaseTool):
    """Search OpenClaw's long-term memory (MEMORY.md + vector store)."""

    def __init__(self, mcp_client: OcMcpClient):
        self._client = mcp_client

    @property
    def name(self) -> str:
        return "memory_search"

    @property
    def description(self) -> str:
        return (
            "搜索长期记忆。当用户提到过去的事、偏好、之前的约定、"
            "历史事件，或任何需要回忆之前内容的场景时使用。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索查询，描述你想要回忆的内容",
                },
                "maxResults": {
                    "type": "integer",
                    "description": "最大返回结果数（默认 5）",
                },
            },
            "required": ["query"],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self._client.is_available:
            return ToolResult(success=False, error="OpenClaw not available")

        result = self._client.call_tool_sync("memory_search", args, timeout=15.0)
        if "error" in result:
            return ToolResult(success=False, error=result["error"])
        return ToolResult(success=True, data=result)


class OcMemoryGetTool(BaseTool):
    """Read a specific snippet from OpenClaw's memory files (MEMORY.md / memory/*.md)."""

    def __init__(self, mcp_client: OcMcpClient):
        self._client = mcp_client

    @property
    def name(self) -> str:
        return "memory_get"

    @property
    def description(self) -> str:
        return (
            "从长期记忆文件中读取指定片段。先用 memory_search 定位文件和行号，"
            "再用此工具拉取具体内容。需要精确引用记忆细节时使用。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "记忆文件的相对路径，如 MEMORY.md 或 memory/notes.md",
                },
                "from": {
                    "type": "integer",
                    "description": "起始行号（可选，默认从头）",
                },
                "lines": {
                    "type": "integer",
                    "description": "读取行数（可选，默认全部）",
                },
            },
            "required": ["path"],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self._client.is_available:
            return ToolResult(success=False, error="OpenClaw not available")

        result = self._client.call_tool_sync("memory_get", args, timeout=15.0)
        if "error" in result:
            return ToolResult(success=False, error=result["error"])
        return ToolResult(success=True, data=result)


class OcGetAgentProfileTool(BaseTool):
    """Get agent identity, personality, and user preferences from OC workspace via MCP."""

    def __init__(self, mcp_client: OcMcpClient):
        self._client = mcp_client

    @property
    def name(self) -> str:
        return "get_agent_profile"

    @property
    def description(self) -> str:
        return (
            "获取 agent 身份信息和用户偏好。当不确定用户称呼、"
            "自身角色设定、或需要了解用户偏好时使用。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "sections": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": '要获取的部分: "identity", "soul", "user"。默认全部。',
                },
            },
            "required": [],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self._client.is_available:
            return ToolResult(success=False, error="OpenClaw not available")

        result = self._client.call_tool_sync("get_agent_profile", args, timeout=15.0)
        if "error" in result:
            return ToolResult(success=False, error=result["error"])
        return ToolResult(success=True, data=result)


class OcListScheduledTasksTool(BaseTool):
    """List active scheduled tasks (cron jobs) from OpenClaw via MCP."""

    def __init__(self, mcp_client: OcMcpClient):
        self._client = mcp_client

    @property
    def name(self) -> str:
        return "list_scheduled_tasks"

    @property
    def description(self) -> str:
        return (
            "查看已设置的定时任务和日程。当用户问「给你布置过什么任务」、"
            "定时提醒、例行日程、或需要确认任务执行状态时使用。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "include_disabled": {
                    "type": "boolean",
                    "description": "是否包含已禁用的任务（默认 false）",
                },
            },
            "required": [],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if not self._client.is_available:
            return ToolResult(success=False, error="OpenClaw not available")

        result = self._client.call_tool_sync("list_scheduled_tasks", args, timeout=15.0)
        if "error" in result:
            return ToolResult(success=False, error=result["error"])
        return ToolResult(success=True, data=result)


def register_oc_tools(registry, mcp_client: OcMcpClient):
    """Register available OC tools into a ToolRegistry.

    Probes Plugin Tools MCP to discover which tools are available.
    """
    if not mcp_client.is_available:
        logger.warning("[OcTools] MCP not available, skipping tool registration")
        return

    plugin_tools = mcp_client.list_tools_sync()
    plugin_tool_names = {t["name"] for t in plugin_tools} if plugin_tools else set()

    registered = []
    if "memory_search" in plugin_tool_names:
        registry.register(OcMemorySearchTool(mcp_client))
        registered.append("memory_search")
    if "memory_get" in plugin_tool_names:
        registry.register(OcMemoryGetTool(mcp_client))
        registered.append("memory_get")
    if "get_agent_profile" in plugin_tool_names:
        registry.register(OcGetAgentProfileTool(mcp_client))
        registered.append("get_agent_profile")
    if "list_scheduled_tasks" in plugin_tool_names:
        registry.register(OcListScheduledTasksTool(mcp_client))
        registered.append("list_scheduled_tasks")

    if registered:
        logger.info(f"[OcTools] Registered plugin tools: {registered}")
    else:
        logger.warning(
            "[OcTools] Plugin Tools MCP connected but no tools found. "
            "Check that plugins are loaded: openclaw plugins list"
        )
