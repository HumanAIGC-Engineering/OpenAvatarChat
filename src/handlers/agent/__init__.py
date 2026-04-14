"""
Agent 系统

包含 1+1 架构:
- ChatAgent: 统一主 Agent（记忆管理 + PromptCompiler 编排 + 主动触发 + 流式 LLM 调用）
- Perception: 异步视觉感知服务（独立 handler，推送感知数据和事件给 ChatAgent）
"""
