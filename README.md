<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<p align="center">
<strong>English | <a href="readme_cn.md">中文</a></strong>
</p>

<p align="center">
<strong>A modular interactive digital human conversation implementation that runs full-featured on a single PC.</strong>
</p>

<p align="center" style="display: flex; flex-direction: row; justify-content: center">
 🤗 <a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp<img alt="Static Badge" style="height: 10px;" src="./assets/images/modelscope_logo.png"> <a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp💬 <a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png">WeChat</a>
</p>

## 🔥 Core Highlights
- **Low-latency digital human real-time conversation: The average response delay is about 2.2 seconds.**
- **Multimodal language model: Supports multimodal language models including text, audio, video, etc.**
- **Modular design: Uses modular design, allowing flexible component replacement to achieve different function combinations.**

## 📢 News

### Changelog

- [2025.04.14] ⭐️⭐️⭐️ Version 0.2.2 released:
  - 100 new avatars released, visit [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)
  - Run LiteAvatar use GPU by default
- [2025.04.07] ⭐️⭐️⭐️ Version 0.2.1 released:
  - Added support for history logging
  - Support for text input
  - Camera requirement removed at startup
  - Optimized modular loading method
- [2025.02.20] ⭐️⭐️⭐️ Version 0.1.0 released:
  - Modular real-time interactive digital human
  - Supports MiniCPM-o as a multimodal language model with cloud API options

### Todo List

- [x] Achieve 100 preset digital human models (expected within 1 month)
- [ ] Integrate [LAM](https://github.com/aigc3d/LAM) (expected within 3 weeks)
- [ ] Integrate [Qwen2.5-Omni](https://github.com/QwenLM/Qwen2.5-Omni)

## Demo

We have deployed a demo service on 
<a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    <img alt="Static Badge" style="height: 10px; margin-right: 1px;" src="./assets/images/modelscope_logo.png">
ModelScope
</a>
and 
<a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    🤗
HuggingFace
</a>. The audio part is implemented using SenseVoice + Qwen-VL + CosyVoice. Feel free to try it out.

<div align="center">
  <video controls src="https://github.com/user-attachments/assets/e2861200-84b0-4c7a-93f0-f46268a0878b">
  </video>
</div>

## 📖 Contents <!-- omit in toc -->

- [Overview](#overview)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Performance](#performance)
  - [Component Dependencies](#component-dependencies)
- [Installation](#installation)
  - [Download Model](#download-model)
  - [Prepare SSL Certificates](#prepare-ssl-certificates)
  - [Run The Demo](#run-the-demo)
  - [TURN Server](#turn-server)
  - [ASR + LLM + TTS Mode](#asr--llm--tts-mode)
  - [Configuration](#Configuration)

## Overview

### Introduction

Open Avatar Chat is a modular implementation of interactive digital human conversation, capable of running full features on a single PC. It currently supports MiniCPM-o as a multimodal language model or can replace the typical ASR + LLM + TTS functions using cloud APIs. The structure of these two modes is shown in the diagram below.

<p align="center">
<img src="./assets/images/data_flow.svg" />
</p>

### Requirements
* Python version 3.10+
* CUDA-enabled GPU
* The unquantized multimodal language model MiniCPM-o requires more than 20GB of VRAM.
* The digital human component uses the CPU for inference, with a tested device CPU of i9-13980HX, capable of reaching 30FPS.

> [!TIP]
> 
> Using the int4 quantized version of the language model can run on graphics cards with less than 10GB of VRAM, but quantization may affect the performance.
> 
> Replacing MiniCPM-o with cloud APIs to implement the typical ASR + LLM + TTS functions can greatly reduce configuration requirements. For more details, see [ASR + LLM + TTS Mode](#asr--llm--tts-replace-local-minicpm-o).

### Performance
In our tests, using a PC equipped with an i9-13900KF processor and Nvidia RTX 4090 graphics card, we recorded the response delay. After ten tests, the average delay was about 2.2 seconds. The delay time is the interval from the end of the user's speech to the start of the digital human's speech, including RTC two-way data transmission time, VAD (Voice Activity Detection) stop delay, and the entire process computation time.

### Component Dependencies

| Type | Open Source Project | GitHub Link | Model Link |
|---|---|---|---|
| RTC | HumanAIGC-Engineering/gradio-webrtc | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc) ||
| VAD | snakers4/silero-vad | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad) ||
| LLM | OpenBMB/MiniCPM-o | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o) | [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6) &nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px">](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
| LLM-int4 | OpenBMB/MiniCPM-o | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o) | [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4) &nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px">](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4) |
| Avatar | HumanAIGC/lite-avatar | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar) ||
| TTS | FunAudioLLM/CosyVoice | [<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/FunAudioLLM/CosyVoice) ||

## Installation

> [!IMPORTANT]
> Submodules and dependent models in this project require the git LFS module. Please ensure that the LFS functionality is installed:
> ```bash
> sudo apt install git-lfs
> git lfs install 
> ```
> This project references third-party libraries via git submodules, so you need to update submodules before running:
> ```bash
> git submodule update --init --recursive
> ```
> 
> If you encounter any issues, feel free to submit an [issue](https://github.com/HumanAIGC-Engineering/OpenAvatarChat/issues) to us.



### Download model
Most models and resource files in this project are included in the referenced submodules. The multimodal language model still needs to be downloaded by the user. This project currently uses MiniCPM-o-2.6 as the multimodal language model to provide dialogue capabilities for the digital human. Users can download the relevant model from [Huggingface](https://huggingface.co/openbmb/MiniCPM-o-2_6) or [Modelscope](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) as needed. It is recommended to download the model directly to \<ProjectRoot\>/models/. The default configuration's model path points to this location. If placed elsewhere, you need to modify the configuration file. 

There are corresponding scripts for downloading the model in the scripts directory, available for use in a Linux environment. Run the script in the project root directory:

```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```

> [!NOTE]
> Both full precision version and the int4 quantized one are supported. However，the int4 version need a special version of AutoGPTQ to load, refer to the [model card](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4) please.

### Prepare ssl certificates
Since we use rtc to stream the video and audio, if not linked from localhost an ssl certificates is needed, user can put exist ones into the ssl_certs folder and config them in the config file or create a new self signed one with the provided script. Run the script under project root to put the result into proper position.
```bash
scripts/create_ssl_certs.sh
```

### Run the demo
The project defaults to using MiniCPM-o as the multimodal language model, which can be started in a Linux container or directly.
  * Run in container: After prepared GPU capable docker environment, run the following script to build and start the service.
    ```bash
    build_and_run.sh
    ```
  * Run directly:
    * Install requirements
    ```bash
    pip install -r requirements.txt
    ```
    * Start demo
    ```bash
    python src/demo.py
    ```

### TURN Server
If you encounter a continuous waiting state after clicking "Start Conversation", it may be due to NAT traversal issues in your deployment environment (such as deployment on cloud machines). In this case, data relay is required. On Linux systems, you can use coturn to set up a TURN server. Follow these steps to install, start, and configure coturn on the same machine:

* Run the installation script
```console
$ chmod 777 scripts/setup_coturn.sh
# scripts/setup_coturn.sh
```
* Modify the config file, add the following configuration and start the service
```yaml
default:
  service:
    rtc_config:
      # Use the following configuration when using turnserver
      urls: ["turn:your-turn-server.com:3478", "turns:your-turn-server.com:5349"]
      username: "your-username"
      credential: "your-credential"
```
* Ensure that the firewall (including cloud machine security group policies) opens the ports required by coturn

### ASR + LLM + TTS Mode
MiniCPM-o's local startup requirements are relatively high. If you already have an LLM API key, you can start this way to experience the conversational digital human. After making the modifications, you can still use `python src/demo.py` to start.

1. Modify the LLM_Bailian configuration in `config/chat_with_openai_compatible.yaml`. The call method in the code uses the standard OpenAI approach, which should be compatible in theory.

```yaml
LLM_Bailian: 
  model_name: "qwen-plus"
  system_prompt: "You are an AI digital human. Respond to my questions briefly and insert punctuation where appropriate."
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```

2. Modify the startup configuration to use: ```python src/demo.py --config config/chat_with_openai_compatible.yaml```

> [!Note]
> * Internal Code Calling Method
> ```python
> client = OpenAI(
>       api_key= self.api_key, 
>       base_url=self.api_url,
>   )
> completion = client.chat.completions.create(
>     model=self.model_name,
>     messages=[
>        self.system_prompt,
>         {'role': 'user', 'content': chat_text}
>     ],
>     stream=True
>     )
> ```
> - Defaults:
>   - ASR defaults to FunASR using `iic/SenseVoiceSmall`.
>   - LLM defaults to Bailian API URL + API key.
>   - TTS defaults to CosyVoice's `iic/CosyVoice-300M-SFT` + `Chinese Female`. You can modify it to other models and use `ref_audio_path` and `ref_audio_text` for voice cloning.



### Configuration
The default parameter will load config from **<project_root>/configs/chat_with_minicpm.yaml**. Config can be loaded from other file by add the --config parameter.
```bash
python src/demo.py --config <absolute-path-to-the-config>.yaml
```
Configurable parameters are listed here：

|Parameter|Default|Description|
|---|---|---|
|log.log_level|INFO|Log level of the demo.|
|service.host|0.0.0.0|Address to start gradio application on.|
|service.port|8282|Port to start gradio application on.|
|service.cert_file|ssl_certs/localhost.crt|Certificate file for ssl, if both cert_file and cert_key are found, https will be enabled.|
|service.cert_key|ssl_certs/localhost.key|Certificate file for ssl, if both cert_file and cert_key are found, https will be enabled.|
|chat_engine.model_root|models|Path to find models.|
|chat_engine.handler_configs|N/A|Handler configs are provided by each handler.|

Current implemented handler provide following configs:
* VAD

|Parameter|Default|Description|
|---|---|---|
|SileraVad.speaking_threshold|0.5|Threshold to determine whether user starts speaking or end speaking.|
|SileraVad.start_delay|2048|Speaking probability should be higher than threshold longer than this period to be recognized as start of speaking, unit in audio sample.|
|SileraVad.end_delay|2048|Speaking probability should be lower than threshold longer than this period to be recognized as end of speaking, unit in audio sample.|
|SileraVad.buffer_look_back|1024|For high threshold, the very start part to the voice may be clipped, use this to compensate, unit in audio sample.|
|SileraVad.speech_padding|512|Silence of this length will be padded on both start and end, unit in audio sample.|

* LLM

|Parameter|Default| Description                                                                                                                                                                                                                                                                                                 |
|---|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|S2S_MiniCPM.model_name|MiniCPM-o-2_6| Which model to load, can be "MiniCPM-o-2_6" or "MiniCPM-o-2_6-int4", it should match the folder's name under model directory.                                                                                                                                                                               |
|S2S_MiniCPM.voice_prompt|| Voice prompt for MiniCPM-o.                                                                                                                                                                                                                                                                                 |
|S2S_MiniCPM.assistant_prompt|| Assistant prompt for MiniCPM-o.                                                                                                                                                                                                                                                                             |
| S2S_MiniCPM.enable_video_input | False         | Whether video input is enabled.**when video input is enbaled vram consumption will be increased largely, on 24GB gpu with non-quantized model, oom may occur during inference.**                                                                                                                            |
| S2S_MiniCPM.skip_video_frame   | -1            | Decide how many frames will be used when video modality is used. -1 means only the latest frame in every 1 second interval will be used. 0 means all frames will be used. n>0 means n frames will be skipped after each accepted frame.|


*ASR FunASR Model*

| Parameter              | Default Value          | Description                                                                 |
|------------------------|------------------------|-----------------------------------------------------------------------------|
| ASR_Funasr.model_name  | iic/SenseVoiceSmall    | This parameter selects a model from [FunASR](https://github.com/modelscope/FunASR). Models are downloaded automatically. To use a local model, provide an absolute path. |

---

*LLM Plain Text Model*

| Parameter                  | Default Value | Description                                                                 |
|----------------------------|---------------|-----------------------------------------------------------------------------|
| LLM_Bailian.model_name     | qwen-plus     | The API for Bailian's testing environment. Free quotas can be obtained from [Bailian](https://bailian.console.aliyun.com/#/home). |
| LLM_Bailian.system_prompt  |               | Default system prompt                                                       |
| LLM_Bailian.api_url        |               | API URL for the model                                                      |
| LLM_Bailian.api_key        |               | API key for the model                                                      |

---

*TTS CosyVoice Model*

| Parameter                      | Default Value | Description                                                                 |
|--------------------------------|---------------|-----------------------------------------------------------------------------|
| TTS_CosyVoice.api_url          |               | Required if deploying CosyVoice server on another machine.                 |
| TTS_CosyVoice.model_name       |               | Refer to [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) for details. |
| TTS_CosyVoice.spk_id           | '中文女' | Use official SFT voices like '英文女' or '英文男'. Mutually exclusive with `ref_audio_path`. |
| TTS_CosyVoice.ref_audio_path  |               | Absolute path to the reference audio. Mutually exclusive with `spk_id`.    |
| TTS_CosyVoice.ref_audio_text  |               | Text content of the reference audio.                                       |
| TTS_CosyVoice.sample_rate      | 24000         | Output audio sample rate                                                   |

---

*Digital Human*

| Parameter                     | Default Value | Description                                                                 |
|-------------------------------|---------------|-----------------------------------------------------------------------------|
| LiteAvatar.avatar_name          | 20250408/sample_data   | Name of the digital human data. 100 avatars provided on ModelScope. Refer to [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery) for more details. |
| LiteAvatar.fps                  | 25            | Frame rate for the digital human. On high-performance CPUs, it can be set to 30 FPS. |
| LiteAvatar.enable_fast_mode     | False          | Low-latency mode. Enabling this reduces response delay but may cause stuttering at the beginning of responses on underpowered systems. |
| LiteAvatar.use_gpu | True | Whether to use GPU acceleration. CUDA backend for now.|


> [!IMPORTANT]
> All path parameters in the configuration can use either absolute paths or paths relative to the project root directory.

## Community Thanks

- Thanks to community member "titan909" for posting the [deployment tutorial video](https://www.bilibili.com/video/BV1FNZ8YNEA8) on Bilibili.
- Thanks to another community member, “十字鱼”, for sharing a video on Bilibili featuring a one-click installation package, along with the download link. (The extraction code is included in the video description—take a close look!) [One-click package](https://www.bilibili.com/video/BV1V1oLYmEu3/?vd_source=29463f5b63a3510553325ba70f325293)

## Star History
![](https://api.star-history.com/svg?repos=HumanAIGC-Engineering/OpenAvatarChat&type=Date)

## Citation

If you found OpenAvatarChat helpful in your research/project, we would appreciate a Star⭐ and citation✏️

```
@software{avatarchat2025,
  author = {Gang Cheng, Tao Chen, Feng Wang, Binchao Huang, Hui Xu, Guanqiao He, Yi Lu, Shengyin Tan},
  title = {OpenAvatarChat},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/HumanAIGC-Engineering/OpenAvatarChat}
}
```
