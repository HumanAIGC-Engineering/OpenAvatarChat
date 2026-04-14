"""
Write-behind Queue — 异步写回队列

将值得长期保留的信息异步写给外部长期记忆系统（Phase 3: OpenClaw），
不阻塞实时对话主链路。

Phase 1: LocalWriteBackQueue — 仅日志记录，不实际写入 OC
Phase 3: McpWriteBackQueue — 通过 MCP 写入 OpenClaw
"""
import time
import threading
from abc import ABC, abstractmethod
from collections import Counter, deque
from dataclasses import dataclass, field
from typing import Dict, Optional, List

from loguru import logger


@dataclass
class WriteBackItem:
    """写回条目"""
    item_type: str                      # "episodic" / "preference" / "fact" / "event"
    content: str
    importance: float = 0.5
    timestamp: float = 0.0
    metadata: Dict = field(default_factory=dict)

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()

    def to_dict(self) -> Dict:
        return {
            "item_type": self.item_type,
            "content": self.content,
            "importance": self.importance,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class WriteBackQueue(ABC):
    """写回队列抽象接口。"""

    @abstractmethod
    def enqueue(self, item: WriteBackItem):
        """将条目加入写回队列。"""
        ...

    @abstractmethod
    def flush(self) -> int:
        """立即处理队列中的所有条目。返回处理数量。"""
        ...

    @abstractmethod
    def pending_count(self) -> int:
        """返回队列中待处理的条目数。"""
        ...

    @abstractmethod
    def shutdown(self):
        """关闭队列，释放资源。"""
        ...


class LocalWriteBackQueue(WriteBackQueue):
    """
    Phase 1 实现：仅日志记录。

    所有 enqueue 的条目只写入日志，不实际传输到外部系统。
    用于开发调试和 Phase 1 的行为验证。
    """

    def __init__(self, max_queue_size: int = 1000):
        self._queue: deque[WriteBackItem] = deque(maxlen=max_queue_size)
        self._total_enqueued: int = 0
        self._total_flushed: int = 0
        self._lock = threading.Lock()

    def enqueue(self, item: WriteBackItem):
        with self._lock:
            self._queue.append(item)
            self._total_enqueued += 1
        logger.info(
            f"[WriteBackQueue:Local] enqueued [{item.item_type}] "
            f"importance={item.importance:.2f}: {item.content[:80]}..."
        )

    def flush(self) -> int:
        with self._lock:
            count = len(self._queue)
            if count == 0:
                return 0
            items = list(self._queue)
            self._queue.clear()
            self._total_flushed += count

        by_type = Counter(i.item_type for i in items)
        logger.info(
            f"[WriteBackQueue:Local] flushed {count} items "
            f"(by type: {dict(by_type)}; total flushed all-time: {self._total_flushed})"
        )
        # Per-item lines look like duplicates when many auto-compact snapshots
        # share the same [COMPACT SUMMARY] prefix (log truncates to 60 chars).
        for item in items:
            logger.debug(
                f"[WriteBackQueue:Local] flush item [{item.item_type}] "
                f"{item.content[:120]}..."
            )
        return count

    def pending_count(self) -> int:
        return len(self._queue)

    def shutdown(self):
        self.flush()

    def get_stats(self) -> Dict:
        return {
            "pending": len(self._queue),
            "total_enqueued": self._total_enqueued,
            "total_flushed": self._total_flushed,
        }
