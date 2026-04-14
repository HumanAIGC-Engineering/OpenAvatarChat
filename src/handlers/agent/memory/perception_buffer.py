"""
Perception Buffer — 感知事件缓冲池

特性：
- 时间衰减 + 硬 TTL 过期
- 同类事件聚合（短时间内多次出现的同类事件合并计数）
- 重要性分级与写回筛选接口
- 容量限制与自动淘汰

设计原则：
- 感知事件不是天然长期记忆，大部分会过期丢弃
- 只有高重要性事件才值得通过 WriteBackQueue 写入 OC
"""
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable

from loguru import logger


@dataclass
class PerceptionEntry:
    """感知缓冲条目"""
    content: str
    category: str                       # scene / event / user_action / conversation
    importance: float                   # 初始重要性 (0-1)
    timestamp: float = 0.0
    metadata: Dict = field(default_factory=dict)

    effective_importance: float = 0.0   # 衰减后的有效重要性
    ttl: float = 0.0                    # 绝对过期时间戳（0 = 不过期）
    occurrence_count: int = 1           # 聚合计数

    def is_expired(self, now: Optional[float] = None) -> bool:
        if self.ttl <= 0:
            return False
        return (now or time.time()) >= self.ttl

    def to_dict(self) -> Dict:
        return {
            "content": self.content,
            "category": self.category,
            "importance": self.importance,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "effective_importance": self.effective_importance,
            "occurrence_count": self.occurrence_count,
        }


# 默认 TTL 映射（秒）
DEFAULT_CATEGORY_TTL = {
    "scene": 300.0,         # 场景描述 5 分钟后过期
    "event": 120.0,         # 交互事件 2 分钟后过期
    "user_action": 180.0,   # 用户动作 3 分钟后过期
    "conversation": 600.0,  # 对话片段 10 分钟后过期
}

# 默认重要性阈值：高于此值的事件才值得写回 OC
WRITEBACK_IMPORTANCE_THRESHOLD = 0.6


class PerceptionBuffer:
    """
    感知事件缓冲池。

    - 时间衰减 + TTL 硬过期
    - 同类事件聚合（event_type + category 相同且在聚合窗口内）
    - 重要性分级与写回筛选接口
    - 容量限制（淘汰有效重要性最低的条目）
    """

    def __init__(
        self,
        max_entries: int = 100,
        decay_rate: float = 0.1,
        decay_interval: float = 60.0,
        category_ttl: Optional[Dict[str, float]] = None,
        aggregation_window: float = 10.0,
    ):
        self.max_entries = max_entries
        self.decay_rate = decay_rate
        self.decay_interval = decay_interval
        self.category_ttl = category_ttl or dict(DEFAULT_CATEGORY_TTL)
        self.aggregation_window = aggregation_window

        self.entries: List[PerceptionEntry] = []
        self.last_decay_time: float = time.time()

    # ── 写入 ──

    def add(
        self,
        content: str,
        category: str,
        importance: float = 0.5,
        metadata: Optional[Dict] = None,
        event_type: Optional[str] = None,
    ):
        """
        添加感知条目。

        如果在聚合窗口内存在同类事件（相同 category + event_type），
        则合并而非新增。
        """
        now = time.time()

        if event_type and self._try_aggregate(category, event_type, content, now):
            return

        ttl_seconds = self.category_ttl.get(category, 0.0)
        entry = PerceptionEntry(
            content=content,
            category=category,
            importance=importance,
            timestamp=now,
            metadata=metadata or {},
            effective_importance=importance,
            ttl=now + ttl_seconds if ttl_seconds > 0 else 0.0,
        )
        if event_type:
            entry.metadata["event_type"] = event_type

        self.entries.append(entry)
        self._maybe_decay()
        self._cleanup_expired()
        self._enforce_capacity()

        logger.debug(f"[PerceptionBuffer] +entry [{category}] {content[:50]}...")

    def _try_aggregate(
        self, category: str, event_type: str, content: str, now: float
    ) -> bool:
        """尝试将新事件聚合到已有同类条目。"""
        for entry in reversed(self.entries):
            if entry.category != category:
                continue
            if entry.metadata.get("event_type") != event_type:
                continue
            if now - entry.timestamp > self.aggregation_window:
                continue
            entry.occurrence_count += 1
            entry.content = content
            entry.timestamp = now
            # 聚合提高重要性（上限 1.0）
            entry.effective_importance = min(
                1.0, entry.effective_importance + 0.05
            )
            logger.debug(
                f"[PerceptionBuffer] aggregated [{category}/{event_type}] "
                f"count={entry.occurrence_count}"
            )
            return True
        return False

    # ── 查询 ──

    def query(
        self,
        category: Optional[str] = None,
        top_k: int = 5,
    ) -> List[PerceptionEntry]:
        self._maybe_decay()
        self._cleanup_expired()

        filtered = self.entries
        if category:
            filtered = [e for e in self.entries if e.category == category]

        sorted_entries = sorted(
            filtered, key=lambda x: x.effective_importance, reverse=True
        )
        return sorted_entries[:top_k]

    def get_summary(
        self,
        max_length: int = 500,
        categories: Optional[List[str]] = None,
    ) -> str:
        self._maybe_decay()
        self._cleanup_expired()

        filtered = self.entries
        if categories:
            filtered = [e for e in self.entries if e.category in categories]

        sorted_entries = sorted(
            filtered, key=lambda x: x.effective_importance, reverse=True
        )

        parts = []
        total_length = 0
        for entry in sorted_entries:
            count_tag = f"(x{entry.occurrence_count})" if entry.occurrence_count > 1 else ""
            entry_text = f"[{entry.category}]{count_tag} {entry.content}"
            if total_length + len(entry_text) > max_length:
                break
            parts.append(entry_text)
            total_length += len(entry_text) + 1
        return "\n".join(parts) if parts else ""

    def get_recent_summary(
        self, seconds: float = 60.0, max_length: int = 300
    ) -> str:
        cutoff = time.time() - seconds
        recent = [e for e in self.entries if e.timestamp >= cutoff and not e.is_expired()]
        sorted_entries = sorted(recent, key=lambda x: x.timestamp, reverse=True)

        parts = []
        total_length = 0
        for entry in sorted_entries:
            count_tag = f"(x{entry.occurrence_count})" if entry.occurrence_count > 1 else ""
            entry_text = f"[{entry.category}]{count_tag} {entry.content}"
            if total_length + len(entry_text) > max_length:
                break
            parts.append(entry_text)
            total_length += len(entry_text) + 1
        return "\n".join(parts) if parts else ""

    # ── 写回筛选 ──

    def get_writeback_candidates(
        self,
        threshold: float = WRITEBACK_IMPORTANCE_THRESHOLD,
    ) -> List[PerceptionEntry]:
        """返回重要性高于阈值的条目，适合写入 OC 长期记忆。"""
        return [
            e for e in self.entries
            if e.effective_importance >= threshold and not e.is_expired()
        ]

    # ── 衰减 & 清理 ──

    def _maybe_decay(self):
        now = time.time()
        if now - self.last_decay_time < self.decay_interval:
            return
        elapsed = now - self.last_decay_time
        decay_cycles = int(elapsed / self.decay_interval)
        if decay_cycles > 0:
            decay_factor = (1 - self.decay_rate) ** decay_cycles
            for entry in self.entries:
                entry.effective_importance *= decay_factor
            self.last_decay_time = now
            logger.debug(
                f"[PerceptionBuffer] decay: {decay_cycles} cycles, "
                f"factor={decay_factor:.3f}"
            )

    def _cleanup_expired(self):
        now = time.time()
        before = len(self.entries)
        self.entries = [e for e in self.entries if not e.is_expired(now)]
        removed = before - len(self.entries)
        if removed:
            logger.debug(f"[PerceptionBuffer] expired {removed} entries")

    def _enforce_capacity(self):
        if len(self.entries) <= self.max_entries:
            return
        self.entries.sort(key=lambda x: x.effective_importance, reverse=True)
        removed = self.entries[self.max_entries:]
        self.entries = self.entries[: self.max_entries]
        if removed:
            logger.debug(f"[PerceptionBuffer] capacity: removed {len(removed)} entries")

    # ── L6 / L7 分层输出（Phase 2.5）──

    def get_state_summary(self, max_length: int = 500) -> str:
        """
        L6: 持续性环境状态快照（最新场景完整 + 旧场景 micro-compact）。
        用于注入 system prompt 的 <environment-state> 标签。
        """
        self._maybe_decay()
        self._cleanup_expired()

        now = time.time()
        scene_entries = [
            e for e in self.entries
            if e.category == "scene" and not e.is_expired(now)
        ]
        scene_entries.sort(key=lambda x: x.timestamp, reverse=True)

        if not scene_entries:
            return ""

        parts: List[str] = []
        total_len = 0

        latest = scene_entries[0]
        parts.append(latest.content)
        total_len += len(latest.content)

        compact_parts: List[str] = []
        for entry in scene_entries[1:]:
            compact = self._micro_compact_entry(entry)
            if total_len + len(compact) + 1 > max_length:
                break
            compact_parts.append(compact)
            total_len += len(compact) + 1

        if compact_parts:
            parts.append(" ".join(compact_parts))

        return "\n".join(parts)

    def get_recent_events(
        self,
        max_age: float = 60.0,
        categories: Optional[List[str]] = None,
    ) -> List[PerceptionEntry]:
        """
        L7: 返回最近的离散事件条目，用于注入 history 的 <observation> 标签。
        """
        now = time.time()
        cutoff = now - max_age
        target_categories = categories or ["event", "user_action"]

        events = [
            e for e in self.entries
            if e.category in target_categories
            and e.timestamp >= cutoff
            and not e.is_expired(now)
        ]
        events.sort(key=lambda x: x.timestamp)
        return events

    def get_compact_history(self, max_full: int = 2, max_length: int = 500) -> str:
        """
        返回感知历史的 micro-compact 格式：
        最近 max_full 条保留完整内容，更早的压缩为单行占位符。
        """
        self._maybe_decay()
        self._cleanup_expired()

        if not self.entries:
            return ""

        sorted_entries = sorted(self.entries, key=lambda x: x.timestamp, reverse=True)
        parts: List[str] = []
        total_len = 0

        for i, entry in enumerate(sorted_entries):
            if i < max_full:
                text = entry.content
            else:
                text = self._micro_compact_entry(entry)

            if total_len + len(text) + 1 > max_length:
                break
            parts.append(text)
            total_len += len(text) + 1

        parts.reverse()
        return "\n".join(parts)

    @staticmethod
    def _micro_compact_entry(entry: "PerceptionEntry") -> str:
        """将一条感知条目压缩为单行占位符。纯规则驱动，不消耗 LLM。"""
        icons = {"scene": "📷", "event": "⚡", "user_action": "👤", "conversation": "💬"}
        icon = icons.get(entry.category, "📌")
        t = time.strftime("%H:%M", time.localtime(entry.timestamp))
        summary = entry.content[:30].replace("\n", " ").strip()
        if len(entry.content) > 30:
            summary += "…"
        count = f"(x{entry.occurrence_count})" if entry.occurrence_count > 1 else ""
        return f"[{icon} {t}{count} {summary}]"

    # ── 工具 ──

    def clear(self):
        self.entries.clear()
        logger.info("[PerceptionBuffer] cleared")

    @property
    def size(self) -> int:
        return len(self.entries)

    def get_stats(self) -> Dict:
        categories: Dict[str, int] = {}
        for entry in self.entries:
            categories[entry.category] = categories.get(entry.category, 0) + 1
        return {
            "total_entries": len(self.entries),
            "max_entries": self.max_entries,
            "categories": categories,
            "last_decay_time": self.last_decay_time,
        }
