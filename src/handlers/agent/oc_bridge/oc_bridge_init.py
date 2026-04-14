"""
OC Bridge initialisation — creates all OC-related components on a
``ChatAgentContext`` and kicks off the background MCP connection thread.

Extracted from ``ChatAgentHandler._init_oc_bridge`` so the main agent
file stays free of OC wiring details.
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from handlers.agent.chat_agent_handler import ChatAgentContext


def init_oc_bridge(context: "ChatAgentContext") -> None:
    """Initialise every OC Bridge component on *context*.

    1. PersonaSnapshot / TaskQueue / TaskMirror / PendingConfirmations (instant)
    2. OC Channel Client (HTTP) + reply bridge
    3. Plugin Tools MCP (background thread, non-blocking)
    """
    oc_cfg = context.config.oc_bridge

    # ── Instant components (no network) ──
    from handlers.agent.oc_bridge.persona_snapshot_mgr import PersonaSnapshotManager
    from handlers.agent.oc_bridge.task_notification_queue import TaskNotificationQueue
    from handlers.agent.oc_bridge.task_mirror import TaskMirror
    from handlers.agent.oc_bridge.pending_confirmations import PendingConfirmationsManager

    context.persona_mgr = PersonaSnapshotManager(
        refresh_interval=oc_cfg.persona_refresh_interval,
        local_default=context.config.persona_snapshot,
    )
    context.task_queue = TaskNotificationQueue()
    context.task_mirror = TaskMirror(mirror_path=oc_cfg.task_mirror_path)
    context.pending_confirmations = PendingConfirmationsManager()

    # ── OC Channel Client (oac-bridge HTTP channel) ──
    from handlers.agent.oc_bridge.oc_channel_client import OcChannelClient
    context.oc_channel_client = OcChannelClient(
        gateway_url=oc_cfg.gateway_http_url,
        webhook_path=oc_cfg.webhook_path,
        token=oc_cfg.token,
        callback_port=oc_cfg.callback_port,
    )
    if context.oc_channel_client.start():
        logger.info(
            f"[ChatAgent] OC Channel Client started "
            f"(callback: {context.oc_channel_client.callback_url})"
        )
        from handlers.agent.oc_bridge.oc_reply_bridge import OcReplyBridge
        OcReplyBridge.register(
            channel_client=context.oc_channel_client,
            session_id=context.session_id,
            task_queue=context.task_queue,
            pending_mgr=context.pending_confirmations,
            proactive_wake=context._proactive_wake,
        )
    else:
        logger.warning("[ChatAgent] OC Channel Client failed to start")
        context.oc_channel_client = None

    # ── Plugin Tools MCP (background thread) ──
    from handlers.agent.oc_bridge.mcp_client import OcMcpClient
    context.oc_mcp_client = OcMcpClient(
        plugin_tools_cmd=oc_cfg.plugin_tools_cmd,
    )

    def _connect_and_register():
        try:
            connected = context.oc_mcp_client.start()
            if connected:
                logger.info("[ChatAgent] OC MCP Client connected (background)")
                if context.persona_mgr:
                    context.persona_mgr.set_mcp_client(context.oc_mcp_client)
                from handlers.agent.oc_bridge.oc_tools import register_oc_tools
                register_oc_tools(context.tool_registry, context.oc_mcp_client)
                _register_oc_tools(context)
            else:
                logger.warning(
                    "[ChatAgent] OC MCP Client failed to connect, degrading gracefully"
                )
        except Exception as e:
            logger.warning(f"[ChatAgent] OC Bridge MCP init failed: {e}")

    t = threading.Thread(
        target=_connect_and_register,
        daemon=True,
        name=f"oc-mcp-init-{context.session_id}",
    )
    t.start()
    logger.info("[ChatAgent] OC Bridge MCP connecting in background (non-blocking)")


def _register_oc_tools(context: "ChatAgentContext") -> None:
    """Register OC-specific agent tools (SpawnAgent, ExecApprove, PendingConfirmations)."""
    from handlers.agent.tools.spawn_agent import SpawnAgentTool
    context.tool_registry.register(SpawnAgentTool(
        llm_client=context.llm_client,
        oc_channel_client=context.oc_channel_client,
        tool_registry=context.tool_registry,
        oac_session_id=context.session_id,
    ))
    from handlers.agent.tools.exec_approve import ExecApproveTool
    context.tool_registry.register(ExecApproveTool(
        oc_channel_client=context.oc_channel_client,
        oac_session_id=context.session_id,
        pending_mgr=context.pending_confirmations,
    ))
    from handlers.agent.tools.pending_confirmations_tool import PendingConfirmationsTool
    context.tool_registry.register(PendingConfirmationsTool(
        manager=context.pending_confirmations,
    ))
