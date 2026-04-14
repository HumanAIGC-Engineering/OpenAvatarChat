"""
Session Memory Manager — 统一记忆管理层

协调 WorkingMemory / PerceptionBuffer / SessionSummary / WriteBackQueue
四个子系统，为 ChatAgentHandler 提供单一入口。

职责：
- 初始化和生命周期管理
- 跨子系统的协同操作（如：用户对话同时更新 WorkingMemory 和触发 SessionSummary）
- 感知事件写入时自动评估是否需要写回 OC
- 提供面向 Prompt 编排的统一上下文查询
"""
import time
from dataclasses import dataclass
from typing import Dict, List, Optional

from loguru import logger

from handlers.agent.memory.working_memory import WorkingMemory, DialogueTurn
from handlers.agent.memory.perception_buffer import (
    PerceptionBuffer,
    PerceptionEntry,
    WRITEBACK_IMPORTANCE_THRESHOLD,
)
from handlers.agent.memory.session_summary import SessionSummaryGenerator, SessionSummary
from handlers.agent.memory.write_behind_queue import (
    WriteBackQueue,
    WriteBackItem,
    LocalWriteBackQueue,
)


@dataclass
class MemoryConfig:
    """记忆系统配置，从 ChatAgentConfig 解耦。"""
    # WorkingMemory
    max_dialogue_turns: int = 20

    # PerceptionBuffer
    perception_max_entries: int = 100
    perception_decay_rate: float = 0.1
    perception_decay_interval: float = 60.0
    perception_aggregation_window: float = 10.0
    perception_category_ttl: Optional[Dict[str, float]] = None

    # SessionSummary
    summary_update_interval_turns: int = 5

    # WriteBackQueue
    writeback_importance_threshold: float = WRITEBACK_IMPORTANCE_THRESHOLD
    writeback_max_queue_size: int = 1000

    # Auto-Compact（Phase 2.5 → 3.3 增强）
    compact_enabled: bool = True
    compact_threshold: int = 15
    compact_keep_recent: int = 5
    compact_save_transcript: bool = True
    rehydrate_task_brief: bool = True
    rehydrate_env_state: bool = True


class SessionMemoryManager:
    """
    统一记忆管理器，每个会话一个实例。

    Usage in ChatAgentHandler:
        memory = SessionMemoryManager(config)
        memory.record_user_input("你好", intent="greeting", perception_snapshot="...")
        memory.record_perception("办公室场景", category="scene")
        memory.record_assistant_response("你好！有什么可以帮你的吗？")

        # 获取上下文给 Prompt 编排
        perception_summary = memory.get_perception_summary(seconds=120)
        dialogue_messages = memory.get_dialogue_for_llm(n=10)
        session_summary_text = memory.get_session_summary_text()
    """

    def __init__(
        self,
        config: Optional[MemoryConfig] = None,
        write_back_queue: Optional[WriteBackQueue] = None,
    ):
        self.config = config or MemoryConfig()

        self.working_memory = WorkingMemory(
            max_turns=self.config.max_dialogue_turns,
        )

        self.perception_buffer = PerceptionBuffer(
            max_entries=self.config.perception_max_entries,
            decay_rate=self.config.perception_decay_rate,
            decay_interval=self.config.perception_decay_interval,
            category_ttl=self.config.perception_category_ttl,
            aggregation_window=self.config.perception_aggregation_window,
        )

        self._summary_generator = SessionSummaryGenerator(
            update_interval_turns=self.config.summary_update_interval_turns,
        )

        self.write_back_queue = write_back_queue or LocalWriteBackQueue(
            max_queue_size=self.config.writeback_max_queue_size,
        )

        logger.info("[SessionMemoryManager] initialized")

    # ── 对话记录 ──

    def record_user_input(
        self,
        content: str,
        intent: Optional[str] = None,
        trigger_type: str = "user",
        perception_snapshot: Optional[str] = None,
    ):
        """记录用户输入，同时触发摘要更新检查。"""
        self.working_memory.add_user_turn(
            content=content,
            intent=intent,
            trigger_type=trigger_type,
            perception_snapshot=perception_snapshot,
        )
        self._maybe_update_summary()

    def record_assistant_response(self, content: str):
        """记录助手回复。"""
        self.working_memory.add_assistant_turn(content)
        self._maybe_update_summary()

    def record_system_event(self, content: str, trigger_type: str = "event"):
        """记录系统事件到对话历史。"""
        self.working_memory.add_system_turn(content, trigger_type=trigger_type)

    # ── 感知记录 ──

    def record_perception(
        self,
        content: str,
        category: str,
        importance: float = 0.5,
        metadata: Optional[Dict] = None,
        event_type: Optional[str] = None,
    ):
        """
        记录感知事件。

        自动评估是否需要写回 OC：
        - importance >= writeback_importance_threshold 的事件会被加入写回队列
        """
        self.perception_buffer.add(
            content=content,
            category=category,
            importance=importance,
            metadata=metadata,
            event_type=event_type,
        )

        if importance >= self.config.writeback_importance_threshold:
            self.write_back_queue.enqueue(WriteBackItem(
                item_type="event" if category == "event" else "episodic",
                content=content,
                importance=importance,
                metadata=metadata or {},
            ))

    # ── 上下文查询（面向 Prompt 编排）──

    def get_environment_state(self, max_length: int = 500) -> str:
        """L6: 获取持续性环境状态快照（最新场景 + micro-compact 历史）。"""
        return self.perception_buffer.get_state_summary(max_length=max_length)

    def get_recent_perception_events(
        self, max_age: float = 60.0
    ) -> List[Dict]:
        """L7: 获取最近的离散事件，格式化为 <observation> 注入用的 dict 列表。"""
        import time as _time
        entries = self.perception_buffer.get_recent_events(max_age=max_age)
        now = _time.time()
        return [
            {
                "source": "camera",
                "time": _time.strftime("%H:%M:%S", _time.localtime(e.timestamp)),
                "content": e.content,
                "event_type": e.metadata.get("event_type", ""),
                "age_seconds": round(now - e.timestamp, 1),
            }
            for e in entries
        ]

    def get_perception_summary(
        self,
        seconds: float = 120.0,
        max_length: int = 200,
    ) -> str:
        """获取最近一段时间的感知摘要（兼容旧接口）。"""
        return self.perception_buffer.get_recent_summary(
            seconds=seconds, max_length=max_length
        )

    def get_perception_full_summary(self, max_length: int = 500) -> str:
        """获取全部感知摘要（按重要性排序）。"""
        return self.perception_buffer.get_summary(max_length=max_length)

    def get_dialogue_for_llm(self, n: Optional[int] = None) -> List[Dict[str, str]]:
        """获取最近 N 轮对话，格式适合 LLM messages。"""
        return self.working_memory.get_llm_messages(n)

    def get_recent_turns(self, n: Optional[int] = None) -> List[DialogueTurn]:
        """获取最近 N 轮完整 DialogueTurn。"""
        return self.working_memory.get_recent_turns(n)

    def get_session_summary_text(self) -> str:
        """获取当前会话摘要文本。"""
        return self._summary_generator.get_text()

    def get_session_summary(self) -> SessionSummary:
        """获取完整的 SessionSummary 数据对象。"""
        return self._summary_generator.summary

    @property
    def current_intent(self) -> Optional[str]:
        return self.working_memory.current_intent

    @property
    def session_mode(self) -> str:
        return self.working_memory.session_mode

    @property
    def turn_count(self) -> int:
        return self.working_memory.turn_count

    # ── 会话状态管理 ──

    def update_session_mode(self, mode: str):
        self.working_memory.update_session_mode(mode)

    def set_task_summary(self, summary: str):
        """由 OC Bridge 调用，设置最近任务摘要。"""
        self.working_memory.set_task_summary(summary)

    # ── 综合快照 ──

    def get_full_context_snapshot(self) -> Dict:
        """
        导出所有记忆层的完整快照，用于调试或一次性传递给 PromptCompiler。
        """
        return {
            "working_memory": self.working_memory.get_context_snapshot(),
            "perception": {
                "recent_summary": self.get_perception_summary(),
                "stats": self.perception_buffer.get_stats(),
            },
            "session_summary": self._summary_generator.summary.to_dict(),
            "write_back_queue": {
                "pending": self.write_back_queue.pending_count(),
            },
        }

    # ── Auto-Compact（Phase 2.5）──

    def should_compact(self) -> bool:
        """检查是否需要触发对话压缩。"""
        if not self.config.compact_enabled:
            return False
        return self.working_memory.should_compact(self.config.compact_threshold)

    def check_and_compact(
        self,
        llm_client,
        model: str,
        task_brief: str = "",
        env_state: str = "",
    ):
        """
        检查并执行对话压缩 + post-compact rehydration。

        由 ChatAgentHandler 在 assistant 回复完成后调用。
        task_brief / env_state 用于压缩后重注入关键上下文。
        """
        if not self.should_compact():
            return

        if self.config.compact_save_transcript:
            transcript = self.working_memory.get_full_transcript()
            self.write_back_queue.enqueue(WriteBackItem(
                item_type="transcript",
                content=transcript,
                importance=0.3,
                metadata={"reason": "auto_compact"},
            ))

        summary = self.working_memory.compact(
            llm_client=llm_client,
            model=model,
            keep_recent=self.config.compact_keep_recent,
        )
        if summary:
            logger.info(
                f"[SessionMemoryManager] auto-compact done: "
                f"summary={len(summary)} chars"
            )
            self._rehydrate(task_brief, env_state)

    def _rehydrate(self, task_brief: str, env_state: str):
        """Post-compact rehydration: re-inject critical context that might be lost."""
        from handlers.agent.memory.working_memory import DialogueTurn

        parts = []
        if self.config.rehydrate_task_brief and task_brief:
            parts.append(f"[当前活跃任务]\n{task_brief}")
        if self.config.rehydrate_env_state and env_state:
            parts.append(f"[当前环境状态]\n{env_state}")
        if parts:
            rehydrated = "\n\n".join(parts)
            self.working_memory.add_turn(DialogueTurn(
                role="system",
                content=f"<rehydrated-context>\n{rehydrated}\n</rehydrated-context>",
                trigger_type="system",
            ))
            logger.info(
                f"[SessionMemoryManager] rehydrated {len(parts)} context sections "
                f"({len(rehydrated)} chars)"
            )

    # ── 生命周期 ──

    def _maybe_update_summary(self):
        if self._summary_generator.should_update(self.working_memory.turn_count):
            self._summary_generator.update(self.working_memory)

    def flush_write_back(self) -> int:
        """手动触发写回队列 flush。"""
        return self.write_back_queue.flush()

    def destroy(self):
        """会话结束时清理。"""
        self.write_back_queue.shutdown()
        self.working_memory.clear()
        self.perception_buffer.clear()
        self._summary_generator.clear()
        logger.info("[SessionMemoryManager] destroyed")
