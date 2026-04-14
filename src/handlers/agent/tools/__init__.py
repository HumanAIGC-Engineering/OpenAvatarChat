"""
Tool framework for ChatAgent.

Provides BaseTool abstraction and ToolRegistry for unified tool management.
Tools are exposed to the LLM via OpenAI function calling format.
"""

from handlers.agent.tools.base_tool import BaseTool, ToolResult
from handlers.agent.tools.tool_registry import ToolRegistry

__all__ = ["BaseTool", "ToolResult", "ToolRegistry"]
