# Handler 概览

Open Avatar Chat 采用模块化的 Handler 架构，每个 Handler 负责对话流程中的一个环节。

## Handler 分类

### Client Handler
- [RTC Client](/reference/handlers/client/rtc-client) - 服务端渲染 WebRTC 客户端
- [LAM Client](/reference/handlers/client/lam-client) - LAM 端侧渲染客户端

### ASR Handler
- [SenseVoice](/reference/handlers/asr/sensevoice) - FunASR SenseVoice 语音识别

### LLM Handler
- [OpenAI 兼容](/reference/handlers/llm/openai-compatible) - OpenAI 兼容 API 语言模型
- [Qwen-Omni](/reference/handlers/llm/qwen-omni) - 通义千问多模态模型
- [Dify](/reference/handlers/llm/dify) - Dify Chatflow 集成

### Agent Handler
- [Chat Agent](/reference/handlers/agent/chat-agent) - 多轮工具调用 Agent（Beta）

### TTS Handler
- [百炼 CosyVoice](/reference/handlers/tts/bailian-cosyvoice) - 百炼 CosyVoice API
- [CosyVoice 本地推理](/reference/handlers/tts/cosyvoice-local) - CosyVoice 本地推理
- [Edge TTS](/reference/handlers/tts/edge-tts) - 微软 Edge TTS

### VAD Handler
- [SileroVAD](/reference/handlers/vad/silero-vad) - Silero 语音活动检测
- [Smart Turn](/reference/handlers/vad/smart-turn) - Smart Turn 端点检测（双工模式）

### Avatar Handler
- [LiteAvatar](/reference/handlers/avatar/liteavatar) - LiteAvatar 2D 数字人
- [LAM](/reference/handlers/avatar/lam) - LAM 3D 数字人驱动
- [MuseTalk](/reference/handlers/avatar/musetalk) - MuseTalk 2D 数字人
- [FlashHead](/reference/handlers/avatar/flashhead) - FlashHead 扩散模型数字人

### Manager Handler
- [Manager 监控台](/reference/handlers/manager/data-tool) - 实时会话监控与信号流可视化
