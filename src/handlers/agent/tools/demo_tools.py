"""
Demo tools for testing the ToolRegistry + Agent Loop pipeline.

These are simple tools to verify end-to-end tool_use flow.
Can be disabled in production via config.
"""

import platform
from datetime import datetime
from typing import Any, Dict

from handlers.agent.tools.base_tool import BaseTool, ToolResult


class GetCurrentTimeTool(BaseTool):
    """Returns the current time and date."""

    @property
    def name(self) -> str:
        return "get_current_time"

    @property
    def description(self) -> str:
        return (
            "获取当前日期和时间。只要用户在问现在几点、今天几号、星期几、"
            "当前时间段，或任何需要当前实时时间的内容，就必须先调用此工具。"
            "不要根据历史对话、上下文或模型记忆猜测时间。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "时区名称，如 'Asia/Shanghai'。默认为系统本地时区。",
                },
            },
            "required": [],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        tz_name = args.get("timezone")
        if tz_name:
            try:
                from zoneinfo import ZoneInfo
                tz = ZoneInfo(tz_name)
                now = datetime.now(tz)
            except Exception:
                now = datetime.now()
        else:
            now = datetime.now()

        weekday_cn = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        return ToolResult(
            success=True,
            data={
                "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
                "weekday": weekday_cn[now.weekday()],
                "timezone": tz_name or "local",
            },
        )


class GetSystemInfoTool(BaseTool):
    """Returns basic system information."""

    @property
    def name(self) -> str:
        return "get_system_info"

    @property
    def description(self) -> str:
        return "获取当前系统基本信息（操作系统、主机名等）。用户问运行环境、设备信息时使用。"

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=True,
            data={
                "os": platform.system(),
                "os_version": platform.version(),
                "hostname": platform.node(),
                "python_version": platform.python_version(),
            },
        )
