"""
Working Memory — 会话级工作记忆

维护当前会话的即时状态：最近对话轮次、当前意图、会话模式、
最近任务摘要（Phase 3 由 OC 填充）、待确认事项。

Phase 2.5 新增：
- auto-compact：对话轮次超过阈值时触发 LLM 压缩，旧轮次替换为摘要
- 压缩前保存完整 transcript 到 WriteBackQueue

设计原则：
- 只保留与当前交互直接相关的短期信息
- 所有内容会话结束即丢弃
- 提供面向 Prompt 编排的结构化输出
"""
import json
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from loguru import logger


@dataclass
class DialogueTurn:
    """统一的对话轮次模型。"""
    role: str                               # "user" / "assistant" / "system"
    content: str                            # 消息正文
    timestamp: float = 0.0

    intent: Optional[str] = None            # 用户意图（仅 user 轮次）
    trigger_type: str = "user"              # "user" / "event"
    perception_snapshot: Optional[str] = None  # 该轮次时刻的视觉摘要

    def to_llm_message(self) -> Dict[str, str]:
        return {"role": self.role, "content": self.content}

    def to_dict(self) -> Dict:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
            "intent": self.intent,
            "trigger_type": self.trigger_type,
            "perception_snapshot": self.perception_snapshot,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "DialogueTurn":
        return cls(
            role=data.get("role", ""),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", 0.0),
            intent=data.get("intent"),
            trigger_type=data.get("trigger_type", "user"),
            perception_snapshot=data.get("perception_snapshot"),
        )


class WorkingMemory:
    """
    会话级工作记忆。

    管理:
    - recent_dialogue: 最近 N 轮对话
    - current_intent: 当前识别到的用户意图
    - session_mode: 当前会话模式 (chitchat / collaboration / report / ...)
    - last_task_summary: 最近的任务摘要 (Phase 3 由 OC Bridge 填充)
    - pending_confirmations: 待用户确认的事项列表
    """

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._dialogue: List[DialogueTurn] = []

        self.current_intent: Optional[str] = None
        self.session_mode: str = "chitchat"
        self.last_task_summary: Optional[str] = None
        self.pending_confirmations: List[str] = []

        self._compact_summary: Optional[str] = None

    # ── 对话管理 ──

    def add_turn(self, turn: DialogueTurn):
        self._dialogue.append(turn)
        self._enforce_limit()
        logger.debug(
            f"[WorkingMemory] +turn role={turn.role} "
            f"len={len(turn.content)} total={len(self._dialogue)}"
        )

    def add_user_turn(
        self,
        content: str,
        intent: Optional[str] = None,
        trigger_type: str = "user",
        perception_snapshot: Optional[str] = None,
    ):
        self.add_turn(DialogueTurn(
            role="user",
            content=content,
            timestamp=time.time(),
            intent=intent,
            trigger_type=trigger_type,
            perception_snapshot=perception_snapshot,
        ))
        if intent:
            self.current_intent = intent

    def add_assistant_turn(self, content: str):
        self.add_turn(DialogueTurn(
            role="assistant",
            content=content,
            timestamp=time.time(),
        ))

    def add_system_turn(self, content: str, trigger_type: str = "event"):
        self.add_turn(DialogueTurn(
            role="system",
            content=content,
            timestamp=time.time(),
            trigger_type=trigger_type,
        ))

    def get_recent_turns(self, n: Optional[int] = None) -> List[DialogueTurn]:
        count = n if n is not None else self.max_turns
        return list(self._dialogue[-count:])

    def get_llm_messages(self, n: Optional[int] = None) -> List[Dict[str, str]]:
        """
        返回适合直接传给 LLM 的 messages 列表。

        如果有 compact_summary，会在最前面插入 <dialogue-summary> 标签的摘要对，
        让 LLM 了解之前的对话脉络。
        """
        messages: List[Dict[str, str]] = []
        if self._compact_summary:
            messages.append({
                "role": "user",
                "content": f"<dialogue-summary>\n{self._compact_summary}\n</dialogue-summary>",
            })
            messages.append({
                "role": "assistant",
                "content": "好的，我记住了之前的对话内容。",
            })
        messages.extend(t.to_llm_message() for t in self.get_recent_turns(n))
        return messages

    @property
    def turn_count(self) -> int:
        return len(self._dialogue)

    @property
    def last_user_message(self) -> Optional[str]:
        for turn in reversed(self._dialogue):
            if turn.role == "user":
                return turn.content
        return None

    # ── 会话状态 ──

    def update_session_mode(self, mode: str):
        if mode != self.session_mode:
            logger.info(f"[WorkingMemory] session_mode: {self.session_mode} -> {mode}")
            self.session_mode = mode

    def set_task_summary(self, summary: str):
        self.last_task_summary = summary

    def add_pending_confirmation(self, item: str):
        self.pending_confirmations.append(item)

    def resolve_confirmation(self, item: str):
        if item in self.pending_confirmations:
            self.pending_confirmations.remove(item)

    # ── 上下文导出 ──

    def get_context_snapshot(self) -> Dict:
        """导出当前工作记忆的完整快照，用于 Prompt 编排或调试。"""
        return {
            "turn_count": self.turn_count,
            "current_intent": self.current_intent,
            "session_mode": self.session_mode,
            "last_task_summary": self.last_task_summary,
            "pending_confirmations": list(self.pending_confirmations),
            "recent_dialogue": [t.to_dict() for t in self.get_recent_turns(5)],
        }

    # ── Auto-Compact（Phase 2.5）──

    def should_compact(self, threshold: int) -> bool:
        """对话轮次是否超过压缩阈值。"""
        return len(self._dialogue) >= threshold

    COMPACT_SYSTEM_PROMPT = (
        "你是对话压缩助手。请先在 <analysis> 中分析对话要点，再在 <summary> 中输出精炼摘要。\n\n"
        "摘要必须保留以下 6 类信息（缺失的类别跳过）：\n"
        "1. **用户偏好和指令** — 明确表达的喜好、要求、习惯\n"
        "2. **对话中建立的事实** — 双方确认的信息、名字、数字\n"
        "3. **未完成的任务和承诺** — 待办事项、约定、未解决的问题\n"
        "4. **当前情绪和互动状态** — 用户的情绪、互动模式\n"
        "5. **用户原始发言要点** — 关键发言的简要引用\n"
        "6. **环境变化摘要** — 传感器/视觉观察的重要变化\n\n"
        "格式：\n"
        "<analysis>\n（推理分析过程，最终不保留）\n</analysis>\n"
        "<summary>\n（精炼摘要，300字以内）\n</summary>"
    )

    def compact(
        self,
        llm_client,
        model: str,
        keep_recent: int = 5,
    ) -> Optional[str]:
        """
        触发 auto-compact：双标签 LLM 压缩旧对话为摘要。

        使用 <analysis> + <summary> 双标签格式，提取 <summary> 内容。
        返回压缩摘要文本（用于 WriteBackQueue 保存），或 None（无需压缩）。
        """
        if len(self._dialogue) <= keep_recent:
            return None

        old_turns = self._dialogue[:-keep_recent]
        recent_turns = self._dialogue[-keep_recent:]

        old_text = "\n".join(
            f"[{t.role}] {t.content}" for t in old_turns
        )

        try:
            response = llm_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.COMPACT_SYSTEM_PROMPT},
                    {"role": "user", "content": old_text[:8000]},
                ],
                max_tokens=600,
            )
            raw_output = response.choices[0].message.content.strip()
            summary = self._extract_summary_tag(raw_output)
        except Exception as e:
            logger.warning(f"[WorkingMemory] compact LLM call failed: {e}")
            summary = f"（之前进行了 {len(old_turns)} 轮对话）"

        if self._compact_summary:
            self._compact_summary = f"{self._compact_summary}\n{summary}"
        else:
            self._compact_summary = summary

        self._dialogue = recent_turns
        logger.info(
            f"[WorkingMemory] compacted: {len(old_turns)} turns → "
            f"{len(summary)} chars summary, kept {len(recent_turns)} recent"
        )
        return summary

    @staticmethod
    def _extract_summary_tag(text: str) -> str:
        """Extract content from <summary>...</summary> tags. Falls back to full text."""
        import re
        match = re.search(r"<summary>\s*(.*?)\s*</summary>", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def get_full_transcript(self) -> str:
        """导出完整对话记录（含 compact 前缀），用于 WriteBackQueue 保存。"""
        parts = []
        if self._compact_summary:
            parts.append(f"[COMPACT SUMMARY]\n{self._compact_summary}")
        for t in self._dialogue:
            parts.append(json.dumps(t.to_dict(), ensure_ascii=False))
        return "\n".join(parts)

    # ── 内部 ──

    def _enforce_limit(self):
        if len(self._dialogue) > self.max_turns:
            removed = len(self._dialogue) - self.max_turns
            self._dialogue = self._dialogue[-self.max_turns:]
            logger.debug(f"[WorkingMemory] trimmed {removed} old turns")

    def clear(self):
        self._dialogue.clear()
        self.current_intent = None
        self.session_mode = "chitchat"
        self.last_task_summary = None
        self.pending_confirmations.clear()
        self._compact_summary = None
        logger.info("[WorkingMemory] cleared")
