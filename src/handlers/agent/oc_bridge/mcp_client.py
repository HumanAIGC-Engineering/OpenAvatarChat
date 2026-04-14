"""
OcMcpClient — async MCP client wrapper for OpenClaw Plugin Tools.

Manages a stdio-based MCP session to OpenClaw's Plugin Tools MCP server,
which exposes tools like get_agent_profile, list_scheduled_tasks, memory_search, etc.
Designed to be used from synchronous handler code via a background event loop.
"""

import asyncio
import json
import threading
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from loguru import logger

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class OcMcpClient:
    """Manages MCP connection to OpenClaw Plugin Tools server.

    Runs an asyncio event loop in a background thread. Synchronous callers
    use call_tool_sync() which bridges into the async loop.
    """

    def __init__(self, plugin_tools_cmd: Optional[str] = None):
        self._plugin_tools_cmd = plugin_tools_cmd
        self._plugin_session: Optional[ClientSession] = None

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._exit_stack: Optional[AsyncExitStack] = None
        self._started = False
        self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    def start(self) -> bool:
        """Start background event loop and connect to Plugin Tools MCP.

        Returns True if the connection was established.
        """
        if self._started:
            return self._available

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="oc-mcp-loop"
        )
        self._thread.start()

        future = asyncio.run_coroutine_threadsafe(self._connect(), self._loop)
        try:
            self._available = future.result(timeout=30.0)
        except Exception as e:
            logger.warning(f"[OcMcpClient] Connection failed: {e}")
            self._available = False

        self._started = True
        return self._available

    def stop(self):
        """Disconnect and stop the background event loop."""
        if self._loop and self._loop.is_running():
            future = asyncio.run_coroutine_threadsafe(self._disconnect(), self._loop)
            try:
                future.result(timeout=10.0)
            except Exception:
                pass
            self._loop.call_soon_threadsafe(self._loop.stop)

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)

        self._started = False
        self._available = False
        logger.info("[OcMcpClient] Stopped")

    def call_tool_sync(
        self, tool_name: str, args: Dict[str, Any],
        timeout: float = 30.0,
    ) -> Dict[str, Any]:
        """Synchronously call an MCP tool (bridges to async loop)."""
        if not self._available or not self._loop:
            return {"error": "OC MCP not available"}

        future = asyncio.run_coroutine_threadsafe(
            self._call_tool(tool_name, args), self._loop
        )
        try:
            return future.result(timeout=timeout)
        except asyncio.TimeoutError:
            return {"error": f"Tool call timed out after {timeout}s"}
        except Exception as e:
            return {"error": str(e)}

    def list_tools_sync(self) -> List[Dict[str, Any]]:
        """List available tools from Plugin Tools MCP."""
        if not self._available or not self._loop:
            return []

        future = asyncio.run_coroutine_threadsafe(
            self._list_tools(), self._loop
        )
        try:
            return future.result(timeout=15.0)
        except Exception:
            return []

    # ── Async internals ──

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    async def _connect(self) -> bool:
        """Connect to Plugin Tools MCP server."""
        self._exit_stack = AsyncExitStack()
        await self._exit_stack.__aenter__()

        if not self._plugin_tools_cmd:
            logger.info("[OcMcpClient] Plugin Tools MCP not configured, skipping")
            return False

        parts = self._plugin_tools_cmd.split()
        server_params = StdioServerParameters(
            command=parts[0],
            args=parts[1:] if len(parts) > 1 else [],
        )

        try:
            stdio_transport = await self._exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read_stream, write_stream = stdio_transport
            session = await self._exit_stack.enter_async_context(
                ClientSession(read_stream, write_stream)
            )
            await session.initialize()
            self._plugin_session = session

            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            logger.info(
                f"[OcMcpClient] Plugin Tools MCP connected, {len(tool_names)} tools: "
                f"{tool_names}"
            )
            return True
        except Exception as e:
            logger.warning(f"[OcMcpClient] Plugin Tools MCP init failed: {e}")
            return False

    async def _disconnect(self):
        if self._exit_stack:
            try:
                await self._exit_stack.aclose()
            except Exception:
                pass
        self._plugin_session = None

    async def _call_tool(
        self, tool_name: str, args: Dict[str, Any],
    ) -> Dict[str, Any]:
        if self._plugin_session is None:
            return {"error": f"No MCP session available for tool: {tool_name}"}

        try:
            result = await self._plugin_session.call_tool(tool_name, args)

            if result.isError:
                text_parts = [
                    item.text for item in result.content
                    if hasattr(item, "text")
                ]
                return {"error": " ".join(text_parts) or "unknown tool error"}

            if hasattr(result, "structuredContent") and result.structuredContent:
                return result.structuredContent

            content_parts = []
            for item in result.content:
                if hasattr(item, "text"):
                    content_parts.append(item.text)

            text_result = "\n".join(content_parts)
            try:
                return json.loads(text_result)
            except (json.JSONDecodeError, ValueError):
                return {"result": text_result}
        except Exception as e:
            logger.error(f"[OcMcpClient] Tool call failed ({tool_name}): {e}")
            return {"error": str(e)}

    async def _list_tools(self) -> List[Dict[str, Any]]:
        tools = []
        if self._plugin_session:
            result = await self._plugin_session.list_tools()
            tools.extend([
                {"name": t.name, "description": t.description}
                for t in result.tools
            ])
        return tools
