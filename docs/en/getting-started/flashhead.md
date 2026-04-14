# FlashHead Quick Start

Both LLM and TTS use cloud APIs. The avatar uses FlashHead Lite mode for diffusion-based talking head generation (GPU only).

## Handlers Used

| Type | Handler | Reference |
|---|---|---|
| Client | client/rtc_client/client_handler_rtc | [RTC Client](/en/reference/handlers/client/rtc-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI Compatible](/en/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [Bailian CosyVoice](/en/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/flashhead/avatar_handler_flashhead | [FlashHead](/en/reference/handlers/avatar/flashhead) |

## Quick Start

```bash
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml
uv run scripts/download_models.py --handler flashhead
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml
```

> [!Note]
> FlashHead depends on `flash-attn`. First-time compilation may take a while.
