"""
ToolRegistry — unified tool registration, discovery, and execution.

All tools (instant, async, sub-agent) register here and are exposed
to the LLM through a single consistent interface.
"""

import time
from typing import Any, Dict, List, Optional

from loguru import logger

from handlers.agent.tools.base_tool import BaseTool, ToolResult


class ToolRegistry:
    """Manages registered tools and provides schemas for LLM function calling."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._schemas_cache: Optional[List[dict]] = None

    def register(self, tool: BaseTool) -> None:
        if tool.name in self._tools:
            logger.warning(f"[ToolRegistry] Overwriting existing tool: {tool.name}")
        self._tools[tool.name] = tool
        self._schemas_cache = None
        logger.info(f"[ToolRegistry] Registered tool: {tool.name}")

    def unregister(self, name: str) -> bool:
        if name in self._tools:
            del self._tools[name]
            self._schemas_cache = None
            logger.info(f"[ToolRegistry] Unregistered tool: {name}")
            return True
        return False

    def get(self, name: str) -> Optional[BaseTool]:
        return self._tools.get(name)

    def has_tools(self) -> bool:
        return len(self._tools) > 0

    @property
    def tool_names(self) -> List[str]:
        return list(self._tools.keys())

    def get_schemas(self) -> List[dict]:
        """Return OpenAI-format tool schemas for all registered tools."""
        if self._schemas_cache is None:
            self._schemas_cache = [
                tool.get_openai_schema() for tool in self._tools.values()
            ]
        return self._schemas_cache

    def execute(self, name: str, args: Dict[str, Any]) -> ToolResult:
        """Execute a tool by name. Returns ToolResult on success or error."""
        tool = self._tools.get(name)
        if tool is None:
            logger.error(f"[ToolRegistry] Unknown tool: {name}")
            return ToolResult(success=False, error=f"Unknown tool: {name}")

        start = time.time()
        try:
            result = tool.execute(args)
            elapsed_ms = (time.time() - start) * 1000
            logger.info(
                f"[ToolRegistry] {name} executed in {elapsed_ms:.0f}ms "
                f"(success={result.success})"
            )
            return result
        except Exception as e:
            elapsed_ms = (time.time() - start) * 1000
            logger.error(
                f"[ToolRegistry] {name} failed in {elapsed_ms:.0f}ms: {e}"
            )
            return ToolResult(success=False, error=str(e))
