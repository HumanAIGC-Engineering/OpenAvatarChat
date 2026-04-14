# Handler Overview

Open Avatar Chat uses a modular Handler architecture where each Handler manages one stage of the conversation pipeline.

## Handler Categories

### Client Handler
- [RTC Client](/en/reference/handlers/client/rtc-client) - Server-rendered WebRTC client
- [LAM Client](/en/reference/handlers/client/lam-client) - LAM client-side rendering

### ASR Handler
- [SenseVoice](/en/reference/handlers/asr/sensevoice) - FunASR SenseVoice speech recognition

### LLM Handler
- [OpenAI Compatible](/en/reference/handlers/llm/openai-compatible) - OpenAI-compatible API
- [Qwen-Omni](/en/reference/handlers/llm/qwen-omni) - Qwen multimodal model
- [Dify](/en/reference/handlers/llm/dify) - Dify Chatflow integration

### Agent Handler
- [Chat Agent](/en/reference/handlers/agent/chat-agent) - Multi-turn tool-calling Agent (Beta)

### TTS Handler
- [Bailian CosyVoice](/en/reference/handlers/tts/bailian-cosyvoice) - Bailian CosyVoice API
- [CosyVoice Local](/en/reference/handlers/tts/cosyvoice-local) - CosyVoice local inference
- [Edge TTS](/en/reference/handlers/tts/edge-tts) - Microsoft Edge TTS

### VAD Handler
- [SileroVAD](/en/reference/handlers/vad/silero-vad) - Silero voice activity detection
- [Smart Turn](/en/reference/handlers/vad/smart-turn) - Smart Turn end-of-utterance (Duplex)

### Avatar Handler
- [LiteAvatar](/en/reference/handlers/avatar/liteavatar) - LiteAvatar 2D avatar
- [LAM](/en/reference/handlers/avatar/lam) - LAM 3D avatar
- [MuseTalk](/en/reference/handlers/avatar/musetalk) - MuseTalk 2D avatar
- [FlashHead](/en/reference/handlers/avatar/flashhead) - FlashHead diffusion avatar

### Manager Handler
- [Manager Console](/en/reference/handlers/manager/data-tool) - Real-time session monitoring and signal flow visualization
