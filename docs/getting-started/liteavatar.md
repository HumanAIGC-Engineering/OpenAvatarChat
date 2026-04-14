# LiteAvatar 快速上手

使用百炼 API 提供 LLM 和 TTS 能力，2D 数字人下对设备要求较低。

## 使用的 Handler

| 类别 | Handler | 安装说明 |
|---|---|---|
| Client | client/rtc_client/client_handler_rtc | [RTC Client](/reference/handlers/client/rtc-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI 兼容](/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [百炼 CosyVoice](/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/liteavatar/avatar_handler_liteavatar | [LiteAvatar](/reference/handlers/avatar/liteavatar) |

## 快速开始

```bash
# 1. 安装依赖
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml

# 2. 下载模型
uv run scripts/download_models.py --handler liteavatar

# 3. 启动
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
```

> [!TIP]
> 需要设置 `DASHSCOPE_API_KEY` 环境变量，或在项目根目录创建 `.env` 文件。
