# Preset Modes

OpenAvatarChat organizes modules based on config files. The `config` directory provides these presets:

| CONFIG Name | ASR | LLM | TTS | AVATAR |
|---|---|:-:|:-:|---|
| chat_with_lam.yaml | SenseVoice | API | API | LAM |
| chat_with_qwen_omni.yaml | Qwen-Omni | Qwen-Omni | Qwen-Omni | lite-avatar |
| chat_with_openai_compatible.yaml | SenseVoice | API | CosyVoice | lite-avatar |
| chat_with_openai_compatible_edge_tts.yaml | SenseVoice | API | edgetts | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice.yaml | SenseVoice | API | API | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml | SenseVoice | API | API | MuseTalk |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml | SenseVoice | API | API | FlashHead |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex.yaml | SenseVoice | API | API | FlashHead (Duplex) |
| chat_with_lam_duplex.yaml | SenseVoice | API | API | LAM (Duplex) |
| chat_with_openai_compatible_bailian_cosyvoice_duplex.yaml | SenseVoice | API | API | lite-avatar (Duplex) |
| chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml | SenseVoice | API | API | MuseTalk (Duplex) |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml | SenseVoice | **Agent** | API | FlashHead (Duplex+Agent) Beta |

> [!TIP]
> Duplex modes (`*_duplex.yaml`) support user interruption. Agent mode (`*_agent.yaml`) uses a multi-turn tool-calling Agent. See [Beta: Chat Agent](/en/beta/chat-agent).
