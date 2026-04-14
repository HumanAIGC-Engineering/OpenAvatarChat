# LAM 快速上手

使用 [LAM](https://github.com/aigc3d/LAM) 项目生成的 Gaussian Splatting 资产进行端侧渲染。语音使用百炼上的 CosyVoice，只有 VAD 和 ASR 运行在本地 GPU，对机器性能依赖很轻，可以支持一机多路。

## 使用的 Handler

| 类别 | Handler | 安装说明 |
|---|---|---|
| Client | client/ws_lam_client/ws_lam_client_handler | [LAM Client](/reference/handlers/client/lam-client) |
| VAD | vad/silerovad/vad_handler/silero | |
| ASR | asr/sensevoice/asr_handler_sensevoice | |
| LLM | llm/openai_compatible/llm_handler/llm_handler_openai_compatible | [OpenAI 兼容](/reference/handlers/llm/openai-compatible) |
| TTS | tts/bailian_tts/tts_handler_cosyvoice_bailian | [百炼 CosyVoice](/reference/handlers/tts/bailian-cosyvoice) |
| Avatar | avatar/lam/avatar_handler_lam_audio2expression | [LAM](/reference/handlers/avatar/lam) |

## 快速开始

```bash
# 1. 安装依赖
uv run install.py --config config/chat_with_lam.yaml

# 2. 下载模型
uv run scripts/download_models.py --handler lam

# 3. 启动
uv run src/demo.py --config config/chat_with_lam.yaml
```
