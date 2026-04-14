# Bailian CosyVoice Handler

Uses Bailian CosyVoice API for TTS, reducing system requirements compared to local inference.

## Configuration

```yaml
CosyVoice:
  module: tts/bailian_tts/tts_handler_cosyvoice_bailian
  voice: "longxiaocheng"
  model_name: "cosyvoice-v1"
  api_key: 'yourapikey'
```

| Parameter | Default | Description |
|---|---|---|
| TTS_CosyVoice.api_url | | Custom CosyVoice server URL |
| TTS_CosyVoice.model_name | | See [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) |
| TTS_CosyVoice.spk_id | Chinese Female | SFT voice. Mutually exclusive with ref_audio_path |
| TTS_CosyVoice.ref_audio_path | | Reference audio path. Mutually exclusive with spk_id |
| TTS_CosyVoice.ref_audio_text | | Reference audio text |
| TTS_CosyVoice.sample_rate | 24000 | Output sample rate |
