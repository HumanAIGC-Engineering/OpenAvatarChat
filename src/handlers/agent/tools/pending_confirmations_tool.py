"""
PendingConfirmationsTool — lets the agent manage a list of items awaiting
user confirmation.

This is the tool-call interface to ``PendingConfirmationsManager``.  The LLM
writes/updates items via this tool; the manager tracks state and produces
nag reminders when items stay ``pending`` too long.
"""

from typing import Any, Dict

from loguru import logger

from handlers.agent.tools.base_tool import BaseTool, ToolResult


class PendingConfirmationsTool(BaseTool):
    """Manage the pending-confirmations list."""

    def __init__(self, manager=None):
        self._manager = manager

    @property
    def name(self) -> str:
        return "pending_confirmations"

    @property
    def description(self) -> str:
        return (
            "管理需要用户确认的事项列表。"
            "当收到需要用户确认的通知（如命令执行审批）时写入，"
            "用户确认或拒绝后更新状态。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "要创建或更新的待确认项列表",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "唯一标识符",
                            },
                            "text": {
                                "type": "string",
                                "description": "描述文本",
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "confirmed", "denied", "expired"],
                                "description": "状态",
                            },
                            "source": {
                                "type": "string",
                                "description": "来源标识，如 exec_approval",
                            },
                        },
                        "required": ["id"],
                    },
                },
            },
            "required": ["items"],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        if self._manager is None:
            return ToolResult(
                success=False,
                error="PendingConfirmationsManager not initialized",
            )

        items = args.get("items", [])
        if not items:
            return ToolResult(
                success=True,
                data={"list": self._manager.render()},
            )

        rendered = self._manager.upsert(items)
        logger.info(f"[PendingConfirmTool] Updated {len(items)} items")
        return ToolResult(
            success=True,
            data={"list": rendered},
        )
