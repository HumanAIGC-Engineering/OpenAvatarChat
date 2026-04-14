# 简介

Open Avatar Chat 是一个模块化的交互数字人对话实现，能够在单台PC上运行完整功能。支持使用云端的 API 实现 ASR + LLM + TTS，也支持本地多模态语言模型。

<p align="center">
<img src="../assets/images/data_flow.svg" />
</p>

## 系统需求

* Python版本 >=3.11.7, \<3.12
* 支持CUDA的GPU
* 数字人部分可以使用GPU/CPU进行推理，测试设备CPU为i9-13980HX，CPU推理下可以达到30FPS.

> [!TIP]
> 使用云端 API 实现 ASR + LLM + TTS，可以大大降低配置需求，具体可参考 [百炼API配置](/getting-started/liteavatar)

## 组件依赖

| 类型 | 开源项目 | Github地址 | 模型地址 |
|----------|-------------------------------------|---|---|
| RTC | HumanAIGC-Engineering/gradio-webrtc |[GitHub](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
| WebUI | HumanAIGC-Engineering/OpenAvatarChat-WebUI |[GitHub](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)||
| VAD | snakers4/silero-vad |[GitHub](https://github.com/snakers4/silero-vad)||
| Avatar | HumanAIGC/lite-avatar |[GitHub](https://github.com/HumanAIGC-Engineering/lite-avatar)||
| TTS | FunAudioLLM/CosyVoice |[GitHub](https://github.com/FunAudioLLM/CosyVoice)||
| Avatar | aigc3d/LAM_Audio2Expression |[GitHub](https://github.com/aigc3d/LAM_Audio2Expression)|[HuggingFace](https://huggingface.co/3DAIGC/LAM_audio2exp)|
| | facebook/wav2vec2-base-960h ||[HuggingFace](https://huggingface.co/facebook/wav2vec2-base-960h) / [ModelScope](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)|
| Avatar | TMElyralab/MuseTalk |[GitHub](https://github.com/TMElyralab/MuseTalk)||
| Avatar | Soul-AILab/SoulX-FlashHead |[GitHub](https://github.com/Soul-AILab/SoulX-FlashHead)|[HuggingFace](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B)|
