"""
ExecApproveTool — lets the main agent approve or deny OC exec requests.

When OC needs approval for a command execution, the notification arrives via
TaskNotificationQueue.  The agent asks the user, then calls this tool to
relay the decision back to OC via the oac-bridge channel.

On success the tool automatically marks the corresponding
PendingConfirmationsManager entry as resolved so nag reminders and
proactive triggers stop firing for that approval.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict

from loguru import logger

from handlers.agent.tools.base_tool import BaseTool, ToolResult

if TYPE_CHECKING:
    from handlers.agent.oc_bridge.pending_confirmations import PendingConfirmationsManager


class ExecApproveTool(BaseTool):
    """Approve or deny an OpenClaw exec-approval request."""

    def __init__(
        self,
        oc_channel_client=None,
        oac_session_id: str = "",
        pending_mgr: PendingConfirmationsManager | None = None,
    ):
        self._oc_channel_client = oc_channel_client
        self._oac_session_id = oac_session_id
        self._pending_mgr = pending_mgr

    @property
    def name(self) -> str:
        return "exec_approve"

    @property
    def description(self) -> str:
        return (
            "批准或拒绝 OpenClaw 后台发来的命令执行审批请求。\n"
            "当 <pending-approvals> 中列出了待审批的 approval_id 时，"
            "说明后台命令正等你批准。\n"
            "你必须先口头告知用户命令内容并询问是否同意，"
            "得到用户明确指示后立即调用本工具。\n\n"
            "decision 三种选项：\n"
            "- \"allow-once\"  — 仅允许这一次\n"
            "- \"allow-always\" — 始终允许此类命令（后续不再询问）\n"
            "- \"deny\"        — 拒绝执行\n\n"
            "当同一任务中已经连续多次出现类似的审批请求时，"
            "应主动告知用户可以选择\"始终允许\"以减少重复打扰。\n"
            "重要：不调用本工具，审批不会生效！口头说\"已批准\"无效。"
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "approval_id": {
                    "type": "string",
                    "description": "待审批请求的 ID（来自 exec.approval.requested 通知）",
                },
                "decision": {
                    "type": "string",
                    "enum": ["allow-once", "allow-always", "deny"],
                    "description": "审批决策：allow-once 允许一次、allow-always 始终允许、deny 拒绝",
                },
            },
            "required": ["approval_id", "decision"],
        }

    def execute(self, args: Dict[str, Any]) -> ToolResult:
        approval_id = args.get("approval_id", "").strip()
        decision = args.get("decision", "").strip()

        if not approval_id:
            return ToolResult(success=False, error="approval_id is required")
        if decision not in ("allow-once", "allow-always", "deny"):
            return ToolResult(
                success=False,
                error=f"Invalid decision: {decision}. Must be allow-once, allow-always, or deny",
            )
        if not self._oc_channel_client:
            return ToolResult(success=False, error="OC channel client not available")

        approve_text = f"/approve {approval_id} {decision}"
        logger.info(
            f"[ExecApprove] Sending approval: {approve_text} "
            f"(session={self._oac_session_id})"
        )

        result = self._oc_channel_client.send_message(
            oac_session_id=self._oac_session_id,
            text=approve_text,
            sender_name="OAC Agent",
        )

        if "error" in result:
            return ToolResult(
                success=False,
                error=f"Failed to send approval: {result['error']}",
            )

        decision_label = {
            "allow-once": "已批准（一次）",
            "allow-always": "已始终批准",
            "deny": "已拒绝",
        }.get(decision, decision)

        if self._pending_mgr:
            resolved_status = "denied" if decision == "deny" else "confirmed"
            try:
                self._pending_mgr.upsert(
                    [{"id": approval_id, "status": resolved_status}]
                )
            except Exception as e:
                logger.warning(f"[ExecApprove] Failed to update pending item: {e}")

        return ToolResult(
            success=True,
            data={
                "approval_id": approval_id,
                "decision": decision,
                "message": f"审批结果已发送: {decision_label}",
            },
        )
