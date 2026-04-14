"""
PersonaSnapshotManager — manages persona/identity for L2 prompt layer.

Reads from OC via MCP get_agent_profile tool.
Falls back to a local default (from YAML persona_snapshot) if MCP is unavailable.
"""

import time
from loguru import logger


class PersonaSnapshotManager:
    """Reads and caches persona data from OpenClaw via MCP.

    Primary path: MCP get_agent_profile via Plugin Tools MCP.
    Fallback: static persona_snapshot string from YAML config.
    """

    def __init__(
        self,
        refresh_interval: float = 600.0,
        local_default: str = "",
        mcp_client=None,
    ):
        self._refresh_interval = refresh_interval
        self._local_default = local_default
        self._mcp_client = mcp_client

        self._cached_snapshot: str = ""
        self._last_refresh: float = 0.0

    def set_mcp_client(self, mcp_client):
        """Set MCP client after async init (called from background thread)."""
        self._mcp_client = mcp_client

    def get_snapshot(self) -> str:
        """Get the current persona snapshot. Auto-refreshes if stale."""
        now = time.time()
        if (now - self._last_refresh) >= self._refresh_interval or not self._cached_snapshot:
            self._refresh()
        return self._cached_snapshot or self._local_default

    def force_refresh(self) -> str:
        """Force an immediate refresh."""
        self._refresh()
        return self._cached_snapshot or self._local_default

    def _refresh(self):
        """Refresh persona from OC via MCP."""
        self._last_refresh = time.time()

        if not self._mcp_client or not self._mcp_client.is_available:
            logger.debug("[PersonaSnapshot] MCP not available, using local default")
            return

        try:
            result = self._mcp_client.call_tool_sync(
                "get_agent_profile", {}, timeout=10.0
            )
            if "error" in result:
                logger.warning(
                    f"[PersonaSnapshot] MCP get_agent_profile error: {result['error']}"
                )
                return

            text = result.get("result", "")
            if isinstance(text, str) and text.strip():
                self._cached_snapshot = text.strip()
                logger.info(
                    f"[PersonaSnapshot] Refreshed via MCP "
                    f"({len(self._cached_snapshot)} chars)"
                )
                return

            content_list = result.get("content", [])
            if isinstance(content_list, list):
                parts = []
                for item in content_list:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", ""))
                    elif isinstance(item, str):
                        parts.append(item)
                if parts:
                    combined = "\n".join(parts).strip()
                    if combined:
                        self._cached_snapshot = combined
                        logger.info(
                            f"[PersonaSnapshot] Refreshed via MCP "
                            f"({len(combined)} chars)"
                        )
                        return

            logger.debug("[PersonaSnapshot] MCP returned empty profile")
        except Exception as e:
            logger.warning(f"[PersonaSnapshot] MCP call failed: {e}")
