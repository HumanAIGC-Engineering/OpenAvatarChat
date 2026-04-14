"""
Session Summary — 会话摘要

维护当前会话的压缩表示，用于：
- OC 不可用时的本地兜底上下文
- 作为 WriteBackQueue 的情景事件源
- 为 Prompt Compiler 提供会话概要

Phase 1 只做规则摘要（关键词 + 意图 + 轮次统计），不调 LLM。
Phase 2+ 可接入 LLM 做更精确的压缩。
"""
import time
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from handlers.agent.memory.working_memory import WorkingMemory


@dataclass
class SessionSummary:
    """会话摘要数据"""
    summary_text: str = ""
    key_topics: List[str] = field(default_factory=list)
    key_intents: List[str] = field(default_factory=list)
    turn_count: int = 0
    last_updated: float = 0.0

    def to_dict(self):
        return {
            "summary_text": self.summary_text,
            "key_topics": self.key_topics,
            "key_intents": self.key_intents,
            "turn_count": self.turn_count,
            "last_updated": self.last_updated,
        }


class SessionSummaryGenerator:
    """
    会话摘要生成器。

    Phase 1: 基于规则的轻量摘要
    - 提取最近对话中的用户意图列表
    - 统计轮次数
    - 拼接最近 N 条用户消息的关键短语

    Phase 2+: 可替换为 LLM 驱动的摘要。
    """

    def __init__(
        self,
        update_interval_turns: int = 5,
        max_topics: int = 10,
    ):
        self.update_interval_turns = update_interval_turns
        self.max_topics = max_topics
        self._summary = SessionSummary()
        self._last_turn_count = 0

    @property
    def summary(self) -> SessionSummary:
        return self._summary

    def should_update(self, current_turn_count: int) -> bool:
        return (current_turn_count - self._last_turn_count) >= self.update_interval_turns

    def update(self, working_memory: "WorkingMemory"):
        """根据 WorkingMemory 的最近对话更新摘要。"""
        turns = working_memory.get_recent_turns()
        if not turns:
            return

        intents = []
        user_snippets = []
        for turn in turns:
            if turn.role == "user":
                if turn.intent:
                    intents.append(turn.intent)
                snippet = turn.content[:60].strip()
                if snippet:
                    user_snippets.append(snippet)

        unique_intents = list(dict.fromkeys(intents))[-self.max_topics:]
        recent_snippets = user_snippets[-self.max_topics:]

        summary_parts = []
        if unique_intents:
            summary_parts.append(f"用户意图: {', '.join(unique_intents)}")
        if recent_snippets:
            summary_parts.append(f"最近话题: {'; '.join(recent_snippets)}")
        summary_parts.append(f"已进行 {working_memory.turn_count} 轮对话")

        if working_memory.session_mode != "chitchat":
            summary_parts.append(f"当前模式: {working_memory.session_mode}")

        self._summary = SessionSummary(
            summary_text=" | ".join(summary_parts),
            key_topics=recent_snippets,
            key_intents=unique_intents,
            turn_count=working_memory.turn_count,
            last_updated=time.time(),
        )
        self._last_turn_count = working_memory.turn_count

        logger.debug(
            f"[SessionSummary] updated: {len(unique_intents)} intents, "
            f"{len(recent_snippets)} topics, {working_memory.turn_count} turns"
        )

    def force_update(self, working_memory: "WorkingMemory"):
        """强制更新，忽略间隔。"""
        self._last_turn_count = 0
        self.update(working_memory)

    def get_text(self) -> str:
        return self._summary.summary_text

    def clear(self):
        self._summary = SessionSummary()
        self._last_turn_count = 0
        logger.info("[SessionSummary] cleared")
