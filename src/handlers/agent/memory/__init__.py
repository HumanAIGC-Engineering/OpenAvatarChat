"""
OAC Memory Layer

分层记忆系统，为 Multi-Agent 管线提供统一的记忆管理。

层次结构:
- WorkingMemory: 会话级工作记忆（最近对话、当前意图、会话模式）
- PerceptionBuffer: 感知事件缓冲（去重、聚合、TTL、重要性分级）
- SessionSummary: 会话摘要（当前会话的压缩表示）
- WriteBackQueue: 异步写回队列（向外部长期记忆系统写入）
- SessionMemoryManager: 统一管理层，协调以上所有组件
"""

from handlers.agent.memory.working_memory import WorkingMemory, DialogueTurn
from handlers.agent.memory.perception_buffer import PerceptionBuffer, PerceptionEntry
from handlers.agent.memory.session_summary import SessionSummary
from handlers.agent.memory.write_behind_queue import WriteBackQueue, WriteBackItem, LocalWriteBackQueue
from handlers.agent.memory.session_memory_manager import SessionMemoryManager

__all__ = [
    "WorkingMemory",
    "DialogueTurn",
    "PerceptionBuffer",
    "PerceptionEntry",
    "SessionSummary",
    "WriteBackQueue",
    "WriteBackItem",
    "LocalWriteBackQueue",
    "SessionMemoryManager",
]
