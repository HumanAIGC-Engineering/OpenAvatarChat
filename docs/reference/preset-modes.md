# 预置模式

OpenAvatarChat 按照配置文件启动并组织各个模块。项目在 `config` 目录下提供以下预置的配置文件：

| CONFIG 名称 | ASR | LLM | TTS | AVATAR |
|----------------------------------------------------|-----|:---------:|:---------:|------------|
| chat_with_lam.yaml | SenseVoice | API | API | LAM |
| chat_with_qwen_omni.yaml | Qwen-Omni | Qwen-Omni | Qwen-Omni | lite-avatar |
| chat_with_openai_compatible.yaml | SenseVoice | API | CosyVoice | lite-avatar |
| chat_with_openai_compatible_edge_tts.yaml | SenseVoice | API | edgetts | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice.yaml | SenseVoice | API | API | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml | SenseVoice | API | API | MuseTalk |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml | SenseVoice | API | API | FlashHead |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex.yaml | SenseVoice | API | API | FlashHead (双工) |
| chat_with_lam_duplex.yaml | SenseVoice | API | API | LAM (双工) |
| chat_with_lam_bailian_asr_duplex.yaml | API | API | API | LAM (双工) |
| chat_with_openai_compatible_bailian_cosyvoice_duplex.yaml | SenseVoice | API | API | lite-avatar (双工) |
| chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml | SenseVoice | API | API | MuseTalk (双工) |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml | SenseVoice | **Agent** | API | FlashHead (双工+Agent) Beta |

> [!TIP]
> 双工模式（`*_duplex.yaml`）支持用户随时打断数字人的回答。Agent 模式（`*_agent.yaml`）使用多轮工具调用 Agent 替代传统 LLM Handler，详见 [Beta: Chat Agent](/beta/chat-agent)。
