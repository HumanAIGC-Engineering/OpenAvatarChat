# LiteAvatar Quick Start

Both LLM and TTS use cloud APIs, making this the lightest config for LiteAvatar.

## Handlers Used

| Type | Handler | Reference |
|---|---|---|
| Client | client/rtc_client/client_handler_rtc | [RTC Client](/en/reference/handlers/client/rtc-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI Compatible](/en/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [Bailian CosyVoice](/en/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/liteavatar/avatar_handler_liteavatar | [LiteAvatar](/en/reference/handlers/avatar/liteavatar) |

## Quick Start

```bash
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
uv run scripts/download_models.py --handler liteavatar
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
```

> [!TIP]
> Set the `DASHSCOPE_API_KEY` environment variable or create a `.env` file in the project root.
