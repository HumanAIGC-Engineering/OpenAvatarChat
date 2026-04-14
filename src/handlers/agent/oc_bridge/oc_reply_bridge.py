"""
OcReplyBridge — routes incoming OC replies (via oac-bridge HTTP callback)
into the agent's TaskNotificationQueue, handling exec-approval parsing,
duplicate detection, external resolution, and proactive-wake signalling.

Extracted from chat_agent_handler._register_oc_reply_bridge to keep the
main agent file free of OC-specific parsing logic.
"""

import re
import threading
from typing import Optional, Set

from loguru import logger

from handlers.agent.oc_bridge.oc_channel_client import OcChannelClient, OcReplyMessage
from handlers.agent.oc_bridge.pending_confirmations import PendingConfirmationsManager
from handlers.agent.oc_bridge.task_notification_queue import (
    TaskNotification,
    TaskNotificationQueue,
)

# ── Regex patterns for OC reply parsing ──

# Pattern A: OC agent text — "/approve <id> <decision>"
_APPROVAL_CMD_RE = re.compile(
    r"/approve\s+([0-9a-f]{6,})\s+(allow-once|allow-always|deny)"
)
_PENDING_CMD_RE = re.compile(
    r"Pending command:\s*```\w*\s*\n(.+?)\n```", re.DOTALL
)

# Pattern B: OC forwarder text — "Exec approval required\nID: <full-uuid>\nCommand: `...`"
_FORWARDER_RE = re.compile(
    r"Exec approval required\s*\nID:\s*([0-9a-f-]{8,})"
)
_FORWARDER_CMD_RE = re.compile(
    r"Command:\s*`([^`]+)`"
)

# Bare resolution echo from OC (e.g. Web UI click)
_APPROVAL_RESOLVE_RE = re.compile(
    r"^/approve\s+([0-9a-f]{6,})\s+(allow-once|allow-always|deny)\s*$"
)


def parse_exec_approval(text: str) -> Optional[dict]:
    """Extract structured approval info from either OC reply format.

    Returns ``{"approval_id": str, "command": str}`` or ``None``.
    """
    # Try Pattern A (OC agent text)
    m = _APPROVAL_CMD_RE.search(text)
    if m:
        approval_id = m.group(1)
        cmd_match = _PENDING_CMD_RE.search(text)
        command = cmd_match.group(1).strip() if cmd_match else "(unknown)"
        return {"approval_id": approval_id, "command": command}

    # Try Pattern B (OC forwarder text)
    m = _FORWARDER_RE.search(text)
    if m:
        full_id = m.group(1)
        approval_id = full_id[:8] if len(full_id) > 8 else full_id
        cmd_match = _FORWARDER_CMD_RE.search(text)
        command = cmd_match.group(1).strip() if cmd_match else "(unknown)"
        return {"approval_id": approval_id, "command": command}

    return None


def format_approval_notification(info: dict) -> str:
    """Build an agent-readable notification for an exec approval request."""
    return (
        f"[exec-approval-needed]\n"
        f"OpenClaw 后台需要你的批准才能执行以下命令：\n"
        f"  命令: {info['command']}\n"
        f"  approval_id: {info['approval_id']}\n"
        f"请向用户简要说明要执行的命令内容，并告知三种选项：\n"
        f"  1. 同意（仅这次）→ decision=\"allow-once\"\n"
        f"  2. 始终同意（后续同类不再询问）→ decision=\"allow-always\"\n"
        f"  3. 拒绝 → decision=\"deny\"\n"
        f"若同一任务已有多次类似审批，应主动建议用户选择\"始终同意\"。\n"
        f"得到用户回答后立即调用 exec_approve 工具。"
    )


def try_handle_external_resolution(
    text: str,
    pending_mgr: Optional[PendingConfirmationsManager],
) -> bool:
    """If *text* is a bare ``/approve <id> <decision>`` echoed by OC
    (i.e. the approval was resolved externally via Web UI / another
    channel), mark the pending item as resolved and signal the caller
    to drop the message.  Returns ``True`` if handled."""
    m = _APPROVAL_RESOLVE_RE.match(text.strip())
    if not m:
        return False
    aid = m.group(1)
    decision = m.group(2)
    if pending_mgr:
        resolved_status = "denied" if decision == "deny" else "confirmed"
        try:
            pending_mgr.upsert([{"id": aid, "status": resolved_status}])
            logger.info(
                f"[OcReplyBridge] External approval resolution: "
                f"{aid} → {resolved_status}"
            )
        except Exception as e:
            logger.warning(
                f"[OcReplyBridge] Failed to mark external resolution: {e}"
            )
    return True


class OcReplyBridge:
    """Stateful bridge that routes OcReplyQueue messages into a
    TaskNotificationQueue, with exec-approval awareness."""

    def __init__(
        self,
        task_queue: TaskNotificationQueue,
        pending_mgr: Optional[PendingConfirmationsManager],
        proactive_wake: threading.Event,
    ):
        self._task_queue = task_queue
        self._pending_mgr = pending_mgr
        self._proactive_wake = proactive_wake
        self._seen_approval_ids: Set[str] = set()

    def handle_reply(self, msg: OcReplyMessage) -> None:
        """Main entry point — called for every OC reply message."""
        if self._task_queue is None:
            return

        if try_handle_external_resolution(msg.text, self._pending_mgr):
            return

        approval_info = parse_exec_approval(msg.text)
        if approval_info:
            aid = approval_info["approval_id"]
            if aid in self._seen_approval_ids:
                logger.debug(
                    f"[OcReplyBridge] Skipping duplicate approval {aid}"
                )
                return
            self._seen_approval_ids.add(aid)
            summary = format_approval_notification(approval_info)
            status = "approval_needed"
            task_id = f"exec-approval-{approval_info['approval_id']}"
            merge_key = f"approval-{approval_info['approval_id']}"
            if self._pending_mgr:
                try:
                    self._pending_mgr.upsert([{
                        "id": approval_info["approval_id"],
                        "text": f"exec: {approval_info['command'][:60]}",
                        "status": "pending",
                    }])
                except Exception as e:
                    logger.warning(
                        f"[OcReplyBridge] pending_confirmations.upsert failed: {e}"
                    )
        else:
            summary = msg.text
            status = "progress"
            task_id = f"oc-reply-{msg.oac_session_id}"
            merge_key = msg.oac_session_id

        notification = TaskNotification(
            task_id=task_id,
            status=status,
            result_summary=summary,
            timestamp=msg.timestamp,
            merge_key=merge_key,
        )
        self._task_queue.push(notification)
        logger.info(
            f"[OcReplyBridge] Routed OC reply to TaskNotificationQueue "
            f"(session={msg.oac_session_id}, type={status}, len={len(msg.text)})"
        )

        if status == "approval_needed":
            self._proactive_wake.set()
            logger.info(
                f"[OcReplyBridge] Set proactive_wake for approval {task_id}"
            )

    @staticmethod
    def register(
        channel_client: Optional[OcChannelClient],
        session_id: str,
        task_queue: TaskNotificationQueue,
        pending_mgr: Optional[PendingConfirmationsManager],
        proactive_wake: threading.Event,
    ) -> Optional["OcReplyBridge"]:
        """Create an OcReplyBridge and register it on the channel client.

        Returns the bridge instance (or ``None`` if *channel_client* is not
        available).
        """
        if not channel_client:
            return None

        bridge = OcReplyBridge(task_queue, pending_mgr, proactive_wake)

        channel_client.reply_queue.register_callback(
            session_id, bridge.handle_reply
        )
        prefixed_key = f"oac-bridge:{session_id}"
        channel_client.reply_queue.register_callback(
            prefixed_key, bridge.handle_reply
        )
        logger.info(
            f"[OcReplyBridge] Registered callbacks for session "
            f"{session_id} and {prefixed_key}"
        )
        return bridge
