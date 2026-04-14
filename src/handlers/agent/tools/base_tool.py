"""
BaseTool — abstract base class for all tools callable by the agent.

Each tool provides:
  - name, description: for LLM tool schema
  - parameters: JSON Schema dict describing the tool's input
  - execute(args) -> ToolResult: synchronous execution
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
import json


@dataclass
class ToolResult:
    """Standardized result returned by tool execution."""
    success: bool = True
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_content_str(self) -> str:
        """Serialize to a string suitable for the tool_result message content."""
        if not self.success:
            return json.dumps({"error": self.error or "unknown error"}, ensure_ascii=False)
        return json.dumps(self.data, ensure_ascii=False, default=str)


class BaseTool(ABC):
    """Abstract base class for agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool name (used as function name in tool_call)."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description shown to LLM."""
        ...

    @property
    @abstractmethod
    def parameters(self) -> dict:
        """JSON Schema dict describing input parameters.

        Example:
            {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "search query"}
                },
                "required": ["query"]
            }
        """
        ...

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> ToolResult:
        """Execute the tool with the given arguments.

        Must return a ToolResult. For async tools, execute() should submit
        the task and immediately return {"status": "submitted", ...}.
        """
        ...

    def get_openai_schema(self) -> dict:
        """Return OpenAI function calling tool schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
