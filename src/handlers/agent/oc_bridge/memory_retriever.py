"""
MemoryRetriever — retrieves relevant long-term memories from OC for each turn.

Uses the current dialogue context to form a query and searches OC's memory
via MCP memory_search tool. No local file fallback.
"""

import time

from loguru import logger

from handlers.agent.oc_bridge.mcp_client import OcMcpClient


class MemoryRetriever:
    """Retrieves relevant memories from OpenClaw via MCP memory_search."""

    def __init__(
        self,
        mcp_client: OcMcpClient,
        max_results: int = 3,
        min_query_length: int = 4,
        cache_ttl: float = 30.0,
    ):
        self._client = mcp_client
        self._max_results = max_results
        self._min_query_length = min_query_length
        self._cache_ttl = cache_ttl

        self._cached_result: str = ""
        self._cached_query: str = ""
        self._cached_time: float = 0.0

    def retrieve(self, query: str) -> str:
        """Search OC memory with a query derived from the current dialogue.

        Returns a formatted string, or empty string if unavailable.
        """
        if not self._client.is_available:
            return ""

        query = query.strip()
        if len(query) < self._min_query_length:
            return ""

        now = time.time()
        if (
            query == self._cached_query
            and (now - self._cached_time) < self._cache_ttl
        ):
            return self._cached_result

        try:
            result = self._client.call_tool_sync(
                "memory_search",
                {"query": query, "maxResults": self._max_results},
                timeout=10.0,
            )

            if "error" in result:
                logger.debug(f"[MemoryRetriever] Search failed: {result['error']}")
                return ""

            formatted = self._format_results(result)

            self._cached_result = formatted
            self._cached_query = query
            self._cached_time = now

            if formatted:
                logger.info(
                    f"[MemoryRetriever] Retrieved {len(formatted)} chars "
                    f"for query: '{query[:50]}'"
                )
            return formatted

        except Exception as e:
            logger.warning(f"[MemoryRetriever] Error: {e}")
            return ""

    def _format_results(self, result: dict) -> str:
        """Format memory search results into a readable string."""
        if isinstance(result.get("result"), str):
            text = result["result"].strip()
            return text if text else ""

        memories = result.get("memories", result.get("results", []))
        if not memories:
            return ""

        if isinstance(memories, list):
            parts = []
            for i, mem in enumerate(memories, 1):
                if isinstance(mem, dict):
                    text = mem.get("text", mem.get("content", str(mem)))
                    parts.append(f"- {text}")
                elif isinstance(mem, str):
                    parts.append(f"- {mem}")
            return "\n".join(parts)

        return str(memories)
