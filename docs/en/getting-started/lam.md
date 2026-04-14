# LAM Quick Start

Uses [LAM](https://github.com/aigc3d/LAM) Gaussian Splatting assets for client-side rendering. Only VAD and ASR run locally, making this the lightest config.

## Handlers Used

| Type | Handler | Reference |
|---|---|---|
| Client | client/ws_lam_client/ws_lam_client_handler | [LAM Client](/en/reference/handlers/client/lam-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI Compatible](/en/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [Bailian CosyVoice](/en/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/lam/avatar_handler_lam_audio2expression | [LAM](/en/reference/handlers/avatar/lam) |

## Quick Start

```bash
uv run install.py --config config/chat_with_lam.yaml
uv run scripts/download_models.py --handler lam
uv run src/demo.py --config config/chat_with_lam.yaml
```
