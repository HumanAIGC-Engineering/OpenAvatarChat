# 百炼 CosyVoice Handler

使用百炼提供的 CosyVoice API 调用 TTS 能力，比本地推理对系统性能要求低。

## 配置参数

```yaml
CosyVoice:
  module: tts/bailian_tts/tts_handler_cosyvoice_bailian
  voice: "longxiaocheng"
  model_name: "cosyvoice-v1"
  api_key: 'yourapikey'  # default=os.getenv("DASHSCOPE_API_KEY")
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| TTS_CosyVoice.api_url | | 自己部署 CosyVoice server 时需填 |
| TTS_CosyVoice.model_name | | 参考 [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) |
| TTS_CosyVoice.spk_id | 中文女 | 使用官方 SFT 音色，和 ref_audio_path 互斥 |
| TTS_CosyVoice.ref_audio_path | | 参考音频路径，和 spk_id 互斥 |
| TTS_CosyVoice.ref_audio_text | | 参考音频的文本内容 |
| TTS_CosyVoice.sample_rate | 24000 | 输出音频采样率 |

> [!TIP]
> 系统默认会获取项目当前目录下的 `.env` 文件用来获取环境变量。
