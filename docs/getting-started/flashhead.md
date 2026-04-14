# FlashHead 快速上手

语言模型与 TTS 都使用云端 API，数字人使用 FlashHead Lite 模式进行推理，基于扩散模型生成高保真说话头视频，默认使用 GPU 推理。

## 使用的 Handler

| 类别 | Handler | 安装说明 |
|---|---|---|
| Client | client/rtc_client/client_handler_rtc | [RTC Client](/reference/handlers/client/rtc-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI 兼容](/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [百炼 CosyVoice](/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/flashhead/avatar_handler_flashhead | [FlashHead](/reference/handlers/avatar/flashhead) |

## 快速开始

```bash
# 1. 安装依赖（会自动编译安装 flash-attn）
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml

# 2. 下载模型
uv run scripts/download_models.py --handler flashhead

# 3. 启动
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml
```

> [!Note]
> FlashHead 依赖 `flash-attn`，首次安装编译时间较长，请耐心等待。
