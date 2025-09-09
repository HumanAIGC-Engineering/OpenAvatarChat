<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<p align="center">
<strong><a href="README.md">中文</a> | English</strong>
</p>

<p align="center">
<strong>A modular interactive digital human conversation implementation.</strong>
</p>

<p align="center" style="display: flex; flex-direction: row; justify-content: center">
 🤗 <a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp<img alt="Static Badge" style="height: 10px;" src="./assets/images/modelscope_logo.png"> <a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp💬 <a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png">WeChat</a>
</p>

## 🔥 Core Highlights
- **Multimodal language model: Supports multimodal language models including text, audio, video, etc.**
- **Modular design: Uses modular design, allowing flexible component replacement to achieve different function combinations.**

## 📢 News

### Changelog

- [2025.08.19] ⭐️⭐️⭐️ Version 0.5.1 Released:
  - LiteAvatar support multi-session. Please refer to LiteAvatar configuration part below.
  - Add support for the Qwen-Omni multimodal model, using the Qwen-Omni-Realtime API service of BaiLian. For the configuration file, please refer to this [config](#chat_with_qwen_omniyaml).
- [2025.08.12] ⭐️⭐️⭐️ Version 0.5.0 Released:
  - Modified to a separated frontend and backend version. The frontend repository[OpenAvatarChat-WebUI](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)has been added to facilitate custom frontend interfaces and expand interactions.
  - Added basic support for calling dify, currently only supporting the chatflow version.
- [2025.06.12] ⭐️⭐️⭐️ Version 0.4.1 Released:
  - Added support for [MuseTalk](https://github.com/TMElyralab/MuseTalk), including customizable videos for personalized avatars.
  - Released 50 new LiteAvatar styles featuring a variety of professional roles. Please refer to [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery).
- [2025.04.18] ⭐️⭐️⭐️ Version 0.3.0 Released:
  - 🎉🎉🎉 Congratulations to the [LAM](https://github.com/aigc3d/LAM) team on their paper being accepted to SIGGRAPH 2025! 🎉🎉🎉
  - Added support for [LAM](https://github.com/aigc3d/LAM) in digital humans, enabling concurrent configuration when LAM is selected. TTS now supports edge_tts and BaiLian CosyVoice.
  - Updated dependency management approach based on UV and handler modules, supporting direct execution or using Docker.
  - CSS responsive layout updated.
- [2025.04.14] ⭐️⭐️⭐️ Version 0.2.2 released:
  - 100 new avatars released, visit [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery)
  - Run [LiteAvatar](https://github.com/HumanAIGC/lite-avatar) use GPU by default
- [2025.04.07] ⭐️⭐️⭐️ Version 0.2.1 released:
  - Added support for history logging
  - Support for text input
  - Camera requirement removed at startup
  - Optimized modular loading method
- [2025.02.20] ⭐️⭐️⭐️ Version 0.1.0 released:
  - Modular real-time interactive digital human
  - Supports MiniCPM-o as a multimodal language model with cloud API options

### Todo List

- [ ] Refine documentation and video tutorials
- [ ] Integrate Live2D digital humans
- [ ] Integrate 3D digital humans

## Demo

### Try it Online

We have deployed a demo service on 
<a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    <img alt="Static Badge" style="height: 10px; margin-right: 1px;" src="./assets/images/modelscope_logo.png">
ModelScope
</a>
and 
<a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat" target="_blank" style="display: inline-block; vertical-align: middle;">
    🤗
HuggingFace
</a>. The audio part is implemented using ``SenseVoice + Qwen-VL + CosyVoice``. Now you can switch between ``LiteAvatar`` and ``LAM``. Feel free to try it out.

### Demo Video

<table>
  <tr>
    <td align="center">
      <h3>LiteAvatar</h3>
      <video controls src="https://github.com/user-attachments/assets/e2861200-84b0-4c7a-93f0-f46268a0878b"></video>
    </td>
    <td align="center">
      <h3>LAM</h3>
      <video controls src="https://github.com/user-attachments/assets/a72a8c33-39dd-4656-a4a9-b76c5487c711"></video>
    </td>
  </tr>
</table>

## Community

* Wechat Group

<img alt="community_wechat.png" height="200" src="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png" width="200"/>

## 🚨 FAQ
Frequently asked questions encountered during the course of the project can be found at [link](./docs/FAQ.md)

## 📖 Contents <!-- omit in toc -->

- [🔥 Core Highlights](#-core-highlights)
- [📢 News](#-news)
  - [Changelog](#changelog)
  - [Todo List](#todo-list)
- [Demo](#demo)
  - [Try it Online](#try-it-online)
  - [Demo Video](#demo-video)
- [Community](#community)
- [🚨 FAQ](#-faq)
- [Overview](#overview)
  - [Introduction](#introduction)
  - [Requirements](#requirements)
  - [Performance](#performance)
  - [Component Dependencies](#component-dependencies)
  - [Pre-set Modes](#pre-set-modes)
- [🚀 Get Started](#-get-started)
  - [Select a config](#select-a-config)
    - [chat\_with\_lam.yaml](#chat_with_lamyaml)
    - [chat\_with\_qwen\_omni.yaml](#chat_with_qwen_omniyaml)
    - [chat\_with\_openai\_compatible.yaml](#chat_with_openai_compatibleyaml)
    - [chat\_with\_openai\_compatible\_edge\_tts.yaml](#chat_with_openai_compatible_edge_ttsyaml)
    - [chat\_with\_openai\_compatible\_bailian\_cosyvoice.yaml](#chat_with_openai_compatible_bailian_cosyvoiceyaml)
    - [chat\_with\_openai\_compatible\_bailian\_cosyvoice\_musetalk.yaml](#chat_with_openai_compatible_bailian_cosyvoice_musetalkyaml)
    - [chat\_with\_minicpm.yaml](#chat_with_minicpmyaml)
  - [Local Execution](#local-execution)
    - [UV Installation](#uv-installation)
    - [Dependency Installation](#dependency-installation)
      - [Install all dependencies](#install-all-dependencies)
      - [Install dependencies for the required mode only](#install-dependencies-for-the-required-mode-only)
    - [Run](#run)
  - [Docker Execution](#docker-execution)
- [Handler Dependencies Installation Notes](#handler-dependencies-installation-notes)
  - [Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)
  - [LAM Client Rendering Handler](#lam-client-rendering-handler)
    - [Select the Avatar Asset](#select-the-avatar-asset)
  - [OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
  - [Qwen-Omni Speech2Speech Handler](#qwen-omni-speech2speech-handler)
  - [MiniCPM Omni Speech2Speech Handler](#minicpm-omni-speech2speech-handler)
    - [Models used](#models-used)
  - [Bailian CosyVoice Handler](#bailian-cosyvoice-handler)
  - [CosyVoice Local Inference Handler](#cosyvoice-local-inference-handler)
  - [Edge TTS Handler](#edge-tts-handler)
  - [LiteAvatar Avatar Handler](#liteavatar-avatar-handler)
    - [Model Dependencies](#model-dependencies)
  - [Dify Chatflow Handler](#dify-chatflow-handler)
    - [Configuration](#configuration)
  - [LAM Avatar Driver Handler](#lam-avatar-driver-handler)
    - [Models used](#models-used-1)
  - [MuseTalk Avatar Handler](#musetalk-avatar-handler)
    - [Model Dependencies](#model-dependencies-1)
    - [Configuration](#configuration-1)
    - [Run](#run-1)
- [Optional Deployment](#optional-deployment)
  - [Prepare ssl certificates](#prepare-ssl-certificates)
  - [TURN Server](#turn-server)
- [Configuration](#configuration-2)
- [Community Thanks](#community-thanks)
- [Star History](#star-history)
- [Citation](#citation)


## Overview

### Introduction

Open Avatar Chat is a modular interactive digital human dialogue implementation that can run full functionality on a single PC. It currently supports MiniCPM-o as a multimodal language model or using cloud-based APIs to replace the conventional ASR + LLM + TTS setup. The architecture of these two modes is illustrated in the diagram below. For more pre-set modes, see [below](#pre-set-modes).

<p align="center">
<img src="./assets/images/data_flow.svg" />
</p>

### Requirements
* Python version >=3.10, <3.12
* CUDA-enabled GPU. The CUDA version supported by the NVIDIA driver needs to be >= 12.4.
* The unquantized multimodal language model MiniCPM-o requires more than 20GB of VRAM.
* The digital human component can perform inference using GPU/CPU. The test device is an i9-13980HX CPU, achieving up to 30 FPS for CPU inference.

> [!TIP]
> 
> Using the int4 quantized version of the language model can run on graphics cards with less than 10GB of VRAM, but quantization may affect the performance.
> 
> Replacing MiniCPM-o with cloud APIs to implement the typical ASR + LLM + TTS functions can greatly reduce configuration requirements. For more details, see [ASR + LLM + TTS Mode](#chat_with_openai_compatible_bailian_cosyvoiceyaml).

### Performance
In our tests, using a PC equipped with an i9-13900KF processor and Nvidia RTX 4090 graphics card, we recorded the response delay. After ten tests, the average delay was about 2.2 seconds. The delay time is the interval from the end of the user's speech to the start of the digital human's speech, including RTC two-way data transmission time, VAD (Voice Activity Detection) stop delay, and the entire process computation time.

### Component Dependencies

| Type | Open Source Project | GitHub Link | Model Link |
|----------|-------------------------------------|---|---|
| RTC      | HumanAIGC-Engineering/gradio-webrtc |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
| WebUI      | HumanAIGC-Engineering/OpenAvatarChat-WebUI |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)||
| VAD      | snakers4/silero-vad                 |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
| LLM      | OpenBMB/MiniCPM-o                   |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)| [🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6) |
| LLM-int4 | OpenBMB/MiniCPM-o                   |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/OpenBMB/MiniCPM-o)|[🤗](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6-int4)|
| Avatar   | HumanAIGC/lite-avatar               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||
| TTS      | FunAudioLLM/CosyVoice               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/FunAudioLLM/CosyVoice)||
|Avatar|aigc3d/LAM_Audio2Expression|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/aigc3d/LAM_Audio2Expression)|[🤗](https://huggingface.co/3DAIGC/LAM_audio2exp)|
||facebook/wav2vec2-base-960h||[🤗](https://huggingface.co/facebook/wav2vec2-base-960h)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)|
|Avatar|TMElyralab/MuseTalk|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/TMElyralab/MuseTalk)|||
|||||

### Pre-set Modes

| CONFIG Name                                          | ASR        |    LLM    |    TTS    | AVATAR       |
|------------------------------------------------------|------------|:---------:|:---------:|--------------|
| chat_with_lam.yaml                                   | SenseVoice |    API    |   API     | LAM          |
| chat_with_qwen_omni.yaml                             |Qwen-Omni| Qwen-Omni | Qwen-Omni | lite-avatar |
| chat_with_minicpm.yaml                               | MiniCPM-o  | MiniCPM-o | MiniCPM-o | lite-avatar  |
| chat_with_openai_compatible.yaml                     | SenseVoice |    API    | CosyVoice | lite-avatar  |
| chat_with_openai_compatible_edge_tts.yaml            | SenseVoice |    API    | edgetts   | lite-avatar  |
| chat_with_openai_compatible_bailian_cosyvoice.yaml   | SenseVoice |    API    |   API     | lite-avatar  |
| chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml | SenseVoice |    API    |   API     | MuseTalk  |
||||||



## 🚀 Get Started

> [!IMPORTANT]
> **[PRE-DEPLOYMENT WARNING] IGNORE THIS, AND YOUR DIGITAL HUMAN WILL 100% GO ON STRIKE!**
>
> Before you excitedly jump into deployment, **STOP!**
> Otherwise, you will almost certainly run into these two major pitfalls: **an inaccessible UI** and a **Digital Human that is stuck loading forever**.
>
> **To get your Digital Human to work, you MUST complete the following checks first:**
>
> 1.  **Confirm Module Installation**: Go to the **installation methods for relevant modules** for your chosen mode and ensure not a single one is missing.
>
> 2.  **Nail Down the Network Setup**: This is the lifeline for internal and external communication. **99% of "my Digital Human isn't responding" issues happen right here**! Please carefully read the **SSL and TURN Service** section in the [Optional Deployment](#optional-deployment).
>
>     **Specifically, your network environment determines the MANDATORY setup:**
>     *   **① Localhost-Only Access**
>         > The simplest setup, usually requiring no extra configuration. However, you can only access it on the machine you deployed it on. It won't be accessible from another device (like your phone).
>
>     *   **② LAN (Local Area Network) Access (e.g., from your phone to your PC)**
>         > An **SSL certificate becomes ESSENTIAL**! Most browsers require a secure `https://` connection to grant camera/microphone permissions. Without it, your Digital Human **can't hear or speak**.
>
>     *   **③ Public / Internet Access (for anyone to use)**
>         > Both an **SSL certificate and a TURN service are NON-NEGOTIABLE**!
>         > - **Without a valid SSL certificate**, browsers will refuse the connection outright. Users won't even be able to open the page.
>         > - **Without a TURN service**, users on different networks (e.g., home vs. office) cannot establish a video stream connection. The button will be **stuck on "Waiting..."**.


### Select a config
The functionalities of OpenAvatarChat will follow the config specified during startup. We provided several sample config files under the config folder.

#### chat_with_lam.yaml
This config uses [LAM](https://github.com/aigc3d/LAM) generated gaussion splatting asset as client-side rendered avatar. With api based openai compatible llm and tts from Bailian platform, only vad and asr handlers are run locally, so this is the lightest config choice, which supports multiple connection on single service.

##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/h5_rendering_client/cllient_handler_lam| [LAM Client Rendering Handler](#lam-client-rendering-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
|TTS|tts/bailian_tts/tts_handler_cosyvoice_bailian|[Bailian CosyVoice Handler](#bailian-cosyvoice-handler)|
|Avatar|avatar/lam/avatar_handler_lam_audio2expression|[LAM Avatar Driver Handler](#lam-avatar-driver-handler)|
||||

#### chat_with_qwen_omni.yaml
Local speech-to-speech dialogue generation is implemented using Qwen-Omni, with the Qwen-Omni-Realtime API (from Alibaba Cloud BaiLian).
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|LLM|llm/qwen_omni/llm_handler_qwen_omni|[Qwen-Omni Speech2Speech Handler](#qwen-omni-speech2speech-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar Avatar Handler](#liteavatar-avatar-handler)|
|||| 

#### chat_with_openai_compatible.yaml
This config use openai-compatible api as llm provider and CosyVoice as local tts model.

##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
|TTS|tts/cosyvoice/tts_handler_cosyvoice|[CosyVoice Local Inference Handler](#cosyvoice-local-inference-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar Avatar Handler](#liteavatar-avatar-handler)|

#### chat_with_openai_compatible_edge_tts.yaml
This config use Edge TTS, it does not need an API Key of Bailian.
##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
|TTS|tts/edgetts/tts_handler_edgetts|[Edge TTS Handler](#edge-tts-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar Avatar Handler](#liteavatar-avatar-handler)|
||||

#### chat_with_openai_compatible_bailian_cosyvoice.yaml
Both LLM and TTS are provided by API, it is the lightest config for LiteAvatar.
##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
|TTS|tts/bailian_tts/tts_handler_cosyvoice_bailian|[Bailian CosyVoice Handler](#bailian-cosyvoice-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar Avatar Handler](#liteavatar-avatar-handler)|
||||

#### chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
Both LLM and TTS are provided by API, while the 2D digital human uses MuseTalk for inference. By default, it uses GPU for inference and CPU inference is not currently supported.
##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|ASR|asr/sensevoice/asr_handler_sensevoice||
|LLM|llm/openai_compatible/llm_handler/llm_handler_openai_compatible|[OpenAI Compatible LLM Handler](#openai-compatible-llm-handler)
|TTS|tts/bailian_tts/tts_handler_cosyvoice_bailian|[Bailian CosyVoice Handler](#bailian-cosyvoice-handler)|
|Avatar|avatar/musetalk/avatar_handler_musetalk|[MuseTalk Avatar Handler](#musetalk-avatar-handler)
||||

#### chat_with_minicpm.yaml
Use MiniCPM-o-2.6 as audio2audio chat model, it need enough VRAM and GPU computaion power.
##### Used Handlers
|Type|Handler|Install Notes|
|---|---|---|
|Client|client/rtc_client/client_handler_rtc|[Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler)|
|VAD|vad/silerovad/vad_handler/silero||
|LLM|llm/minicpm/llm_handler_minicpm|[MiniCPM Omni Speech2Speech Handler](#minicpm-omni-speech2speech-handler)|
|Avatar|avatar/liteavatar/avatar_handler_liteavatar|[LiteAvatar Avatar Handler](#liteavatar-avatar-handler)|
|||| 


### Local Execution

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
> 
> This project depends on CUDA, please make sure that the CUDA version supported by the local NVIDIA driver is >= 12.4

#### UV Installation
It is recommended to install [UV](https://docs.astral.sh/uv/), using UV for local environment management.
> Official standalone installer
> ```bash
> # On Windows.
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
> # On macOS and Linux.
> curl -LsSf https://astral.sh/uv/install.sh | sh
> ```
> PyPI installation
> ```
> # With pip.
> pip install uv
> # Or pipx.
> pipx install uv
> ```
#### Dependency Installation
##### Install all dependencies
```bash
uv sync --all-packages
```
##### Install dependencies for the required mode only
```bash
uv venv --python 3.11.11

uv pip install setuptools pip

uv run install.py --uv --config <absolute path to config file>.yaml

./scripts/post_config_install.sh --config <absolute path to config file>.yaml
```
> [!Note]
> The `post_config_install.sh` script adds the NVIDIA CUDA library paths from the virtual environment to `ld.so.conf.d` and updates the `ldconfig` cache to ensure the system correctly loads these dynamic link libraries.


#### Run
```bash
uv run src/demo.py --config <absolute path to config file>.yaml
```

### Docker Execution
> [!Note] 
Containerized execution: The container relies on NVIDIA's container environment. After preparing a Docker environment that supports GPUs, execute the following command to complete the construction and deployment of the image:
```bash
./build_and_run.sh --config <relative path to config file>.yaml
```

> [!Note]  
> For RTX 50-series GPUs, we have updated the CUDA version to 12.8 in the project's `pyproject.toml` and adapted it for MuseTalk. We tested this in a Docker environment (Ubuntu 24.04, Driver Version: 575.64.03), and confirmed that Lam, LiteAvatar, and MuseTalk all run normally.  
If you need to build the image yourself, use `build_cuda128.sh` (which uses `Dockerfile.cuda128`). To run the image, use `run_docker_cuda128.sh`. Unlike previous versions, `Dockerfile.cuda128` packages all dependencies required by the project into the image file—dynamic loading via config files is no longer used, making it easier to test all digital humans.  


```bash
# Clone the project repository
git clone https://github.com/HumanAIGC-Engineering/OpenAvatarChat.git

# Navigate to the project directory
cd OpenAvatarChat

# Download all submodules
git submodule update --init --recursive --depth 1

# Download models required for LiteAvatar
# The script uses ModelScope to download models by default. 
# If ModelScope is not installed locally, install it first with: pip install modelscope
bash scripts/download_liteavatar_weights.sh

# Download models required for LAM
git clone --depth 1 https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git ./models/wav2vec2-base-960h
wget https://virutalbuy-public.oss-cn-hangzhou.aliyuncs.com/share/aigc3d/data/LAM/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp && rm ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar

# Download models required for MuseTalk
bash scripts/download_musetalk_weights.sh

# Build the Docker image (with CUDA 12.8)
bash build_cuda128.sh

# (Optional) If using the Bailian API:
# Create a .env file in the project root and add your API key
touch .env 
# Edit the .env file manually to add: DASHSCOPE_API_KEY=sk-xxxxx

# Run the Docker container
# Replace the config file with your desired one (example below)
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```

## Handler Dependencies Installation Notes
### Server Rendering RTC Client Handler
Currently there is no extra dependency or essential configs.

### LAM Client Rendering Handler
Client rendering handler is derived from [Server Rendering RTC Client Handler](#server-rendering-rtc-client-handler). It supports multi-connection. Client avatar asset can be selected in handler config.
#### Select the Avatar Asset
LAM avatar asset can be generated by the [LAM project](https://github.com/aigc3d/LAM) (The ready-to-use generation pipeline is not ready yet. Stay tunned!). OpenAvatarChat provides 4 sample asset. They can be found under 
src/handlers/client/h5_rendering_client/lam_samples. The selected asset should be set to the asset_path field in the handler config. You can use one of the sample asset, a your own asset that created by LAM, please refer to the follow handler config sample:
```yaml
LamClient:
  module: client/h5_rendering_client/client_handler_lam
  asset_path: "lam_samples/barbara.zip"
  concurrent_limit: 5
```

### OpenAI Compatible LLM Handler
Local llm handler has relatively high startup requirements. If you already have an available LLM api_key, you can start it this way to experience interactive digital humans.
Modify the corresponding config, such as the LLMOpenAICompatible configuration in config/chat_with_openai_compatible.yaml. The invocation method in the code uses the standard OpenAI approach, which should theoretically be compatible with similar setups.
```yaml
LLMOpenAICompatible: 
  model_name: "qwen-plus"
  system_prompt: "You are an AI digital human. Respond to my questions briefly and insert punctuation where appropriate."
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```
>[!TIP]
>OpenAvatarChat will acquire the .env file in current working directory, it is can be used to set the environment variables without change the config file.

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
> * The default LLM API is Bailian api_url.

### Qwen-Omni Speech2Speech Handler
The capabilities of Qwen-Omni are integrated via Alibaba Cloud BaiLian's API. Currently, only the manual mode is supported. Voice Activity Detection (VAD) is executed by the local SileroVad model. Additionally, due to the poor quality and unreliability of input_transcription results in manual mode, an extra SenseVoice module has been added exclusively for echoing conversation records.
For the complete configuration file, please refer to chat_with_qwen_omni.yaml. Among them, the avatar module supports a choice between AvatarMusetalk and LiteAvatar.

### MiniCPM Omni Speech2Speech Handler
> [!IMPORTANT]
> **Note：According to the repository size of MiniCPM, it is not included as a submodule. If it is needed, please refer to src/handlers/llm/minicpm/notes.md to get the code first.**
#### Models used
In this project, MiniCPM-o-2.6 can be used as a multimodal language model to provide dialogue capabilities for digital humans. Users can download the relevant model as needed from [Huggingface](https://huggingface.co/openbmb/MiniCPM-o-2_6) or [Modelscope](https://modelscope.cn/models/OpenBMB/MiniCPM-o-2_6). It is recommended to directly download the model to <ProjectRoot>/models/. The default configuration points to this path, so if the model is placed elsewhere, you need to modify the configuration file. There is a corresponding model download script in the scripts directory, which can be used in a Linux environment. Please run the script in the project root directory:

```bash
scripts/download_MiniCPM-o_2.6.sh
```
```bash
scripts/download_MiniCPM-o_2.6-int4.sh
```

> [!NOTE]
> Both full precision version and the int4 quantized one are supported. However，the int4 version need a special version of AutoGPTQ to load, refer to the [model card](https://huggingface.co/openbmb/MiniCPM-o-2_6-int4) please.

### Bailian CosyVoice Handler
Bailian provides CosyVoice API, it can be used as an alternative to local tts inference handler. Though it requires an Bailian API Key, it reduces quite amount of system requirments.
Sample handler config looks like this:
```
CosyVoice:
  module: tts/bailian_tts/tts_handler_cosyvoice_bailian
  voice: "longxiaocheng"
  model_name: "cosyvoice-v1"
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```
Same as [OpenAI Compatible LLM Handler](#openai-compatible-llm-handler), api_key can be set in the handler config or from environment variables.
>[!TIP]
>OpenAvatarChat will acquire the .env file in current working directory, it is can be used to set the environment variables without change the config file.

### CosyVoice Local Inference Handler
> [!WARNING]
> Due to an issue where the pynini package dependency fails to compile with unsupported parameters when fetched via PyPI on Windows, the current recommended workaround by CosyVoice is to install the precompiled pynini package from conda-forge on Windows using Conda.

When using CosyVoice locally as TTS on Windows, it is necessary to combine Conda and UV for installation. The specific dependency installation and execution process are as follows:

1. Install Anaconda or [Miniconda](https://docs.anaconda.net.cn/miniconda/install/)
```bash
conda create -n openavatarchat python=3.10
conda activate openavatarchat
conda install -c conda-forge pynini==2.1.6
```

2. Set the environment variable indexed by UV to the Conda environment
```bash
# cmd
set VIRTUAL_ENV=%CONDA_PREFIX%
# powershell 
$env:VIRTUAL_ENV=$env:CONDA_PREFIX
```
3. When installing dependencies and running with UV, add the `--active` parameter to prioritize the use of the activated virtual environment
```bash
# Install dependencies
uv sync --active --all-packages
# Install required dependencies only
uv run --active install.py --uv --config config/chat_with_openai_compatible.yaml
# Run CosyVoice 
uv run --active src/demo.py --config config/chat_with_openai_compatible.yaml
```
> [!Note]
> - TTS defaults to CosyVoice's `iic/CosyVoice-300M-SFT` + `Chinese Female` You can modify it to other models and use `ref_audio_path` and `ref_audio_text` for voice cloning.

### Edge TTS Handler
OpenAvatarChat integrated Microsoft Edge TTS, it is inference on the cloud and api key is not esstential, the sample handler config looks like:
```yaml
Edge_TTS:
  module: tts/edgetts/tts_handler_edgetts
  voice: "zh-CN-XiaoxiaoNeural"
```

### LiteAvatar Avatar Handler
LiteAvatar is integarted to provide 2D avatar feature. Currenty, 100 avatar assets are provided on modelscope project [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery), please refer to this project for detail.

#### Model Dependencies
**Model weights have to be downloaded before you use LiteAvatar**, LiteAvatar source code includes a model download script. For convenience, a script for Linux enviroments also provided in the `scripts` directory of this repo. You can call this script under **project root**:
```bash
bash scripts/download_liteavatar_weights.sh
```

### Dify Chatflow Handler 
The project currently integrates Dify's Chatflow. Users can create a Chatflow in Dify, and after filling in the generated Chatflow application's api_url and api_key, they can use Dify's Chatflow for conversation.
```yaml
 Dify:
      enabled: True
      module: llm/dify/llm_handler_dify
      enable_video_input: False # Allow camera input, ensure application supports vision and accepts file inputs
      api_key: '' #your dify api key
      api_url: 'http://localhost/v1' # your dify api url
 
```

#### Configuration
LiteAvatar can be run on CPU as well as GPU. If other GPU heavy handlers are used, let liteavatar run on cpu may be a good choice.

Sample handler config looks like:
```yaml
LiteAvatar:
  module: avatar/liteavatar/avatar_handler_liteavatar
  avatar_name: 20250408/sample_data
  fps: 25
  use_gpu: true
```

#### Multi-Session Support
LiteAvatar supports multiple sessions on a single machine. To enable this feature, refer to `config/chat_with_openai_compatible_bailian_cosyvoice.yaml` and set the `default.chan_engine.concurrent_limit` parameter. By configuring this parameter, you predefine the maximum number of concurrent sessions supported at startup.

Please note that running multiple sessions significantly increases system resource demands. When LiteAvatar runs on a GPU, each concurrent session consumes approximately 3GB of GPU memory. Setting `concurrent_limit` too high may lead to **out-of-memory errors**. Please adjust the number of concurrent sessions according to your machine's hardware specifications.


### LAM Avatar Driver Handler
#### Models used
* facebook/wav2vec2-base-960h [🤗](https://huggingface.co/facebook/wav2vec2-base-960h) [<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)
  * Download from huggingface, ensure lfs is installed properly，run following cmd under root of the project:
  ```
  git clone --depth 1 https://huggingface.co/facebook/wav2vec2-base-960h ./models/wav2vec2-base-960h
  ```
  * Download from modelscope, ensure lfs is installed properly，run following cmd under root of the project:
  ```
  git clone --depth 1 https://www.modelscope.cn/AI-ModelScope/wav2vec2-base-960h.git ./models/wav2vec2-base-960h
  ```
* LAM_audio2exp [🤗](https://huggingface.co/3DAIGC/LAM_audio2exp)
  * Download form huggingface, ensure lfs is installed properly，run following cmds under root of the project:
  ```
  wget https://huggingface.co/3DAIGC/LAM_audio2exp/resolve/main/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
  tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp && rm ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar
  ```
  * If huggingface is unreachable, it can also be downloaded from oss, run following cmds under root of the project:
  ```
  wget https://virutalbuy-public.oss-cn-hangzhou.aliyuncs.com/share/aigc3d/data/LAM/LAM_audio2exp_streaming.tar -P ./models/LAM_audio2exp/
  tar -xzvf ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar -C ./models/LAM_audio2exp && rm ./models/LAM_audio2exp/LAM_audio2exp_streaming.tar
  ```

### MuseTalk Avatar Handler

The project currently integrates the latest MuseTalk 1.5 (previous versions are not tested). This version supports custom avatars, which can be selected by modifying the `avatar_video_path` parameter.

#### Model Dependencies

* MuseTalk source code includes a model download script. To keep the directory structure consistent, a modified script is provided in the `scripts` directory for Linux environments. The original MuseTalk code uses relative paths for loading; although adaptations have been made, some code cannot be configured via input parameters. **Do not change the model download location.** Run the script from the project root:
  ```bash
  bash scripts/download_musetalk_weights.sh
  ```
* The MuseTalk source code will download a model s3fd-619a316812.pth on first startup, which is not included in the download script. The initial download might be slow.

#### Digital Human Model Download Tool

By setting `avatar_video_path`, you can customize the base video for the digital human. To facilitate users without digital human material, we provide a tool that allows MuseTalk users to use digital human materials provided by LiteAvatar. The script file is `scripts/download_avatar_model.py`, and the model list can be viewed at [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery).

**Usage Method:**

```bash
# 1. View help information
python scripts/download_avatar_model.py --help

# 2. Download the specified digital human model
python scripts/download_avatar_model.py -m "20250612/P1rcvIW8H6kvcYWNkEnBWPfg"

# 3. View the list of downloaded models
python scripts/download_avatar_model.py -d

# Output example:
# Downloaded Models List:
# avatar_name（for LiteAvatar config）    avatar_video_path（for Musetalk config）
# --------------------------------------------------------------------------------
# 20250612/P1rcvIW8H6kvcYWNkEnBWPfg       resource/avatar/liteavatar/20250612/P1rcvIW8H6kvcYWNkEnBWPfg/bg_video_silence.mp4
```

#### Configuration

* **Avatar selection:** MuseTalk source includes two default avatars. You can select by modifying the `avatar_video_path` parameter. The system will prepare data on first load and cache it for subsequent runs. You can force regeneration by setting `force_create_avatar: true`. The `avatar_model_dir` parameter specifies where to save avatar data (default: `models/musetalk/avatar_model`).
* **Frame rate:** Although MuseTalk documentation claims 30fps on V100, our adaptation (referencing `realtime_inference.py`) does not reach this in practice. We recommend `fps: 20`, but you can adjust based on your GPU. If you see the warning `[IDLE_FRAME] Inserted idle during speaking` in logs, it means actual inference fps is lower than set fps. 
* **Batch size:** Increasing `batch_size` can improve throughput, but too large a batch may slow first-frame response. The minimum batch_size for inference is 2. If you set it to 1, an error will appear in the log`[IDLE_FRAME] 1 validation error for AvatarMuseTalkConfig，batch_size - Input should be greater than or equal to 2 [type=greater_than_equal, input_value=1, input_type=int]`  

**Sample config:**
```yaml
Avatar_MuseTalk:
  module: avatar/musetalk/avatar_handler_musetalk
  fps: 20  # Video frame rate
  batch_size: 2  # Batch processing frame count, must be greater than 2
  avatar_video_path: "src/handlers/avatar/musetalk/MuseTalk/data/video/sun.mp4"  # Initialization video path
  avatar_model_dir: "models/musetalk/avatar_model"  # Default avatar model directory
  force_create_avatar: false  # Whether to force regenerate digital human data
  debug: false  # Whether to enable debug mode
  ... # See AvatarMuseTalkConfig for more parameters
```

#### Run

* Docker

```bash
./build_and_run.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```

* Local deployment

The order of commands for installing dependencies locally is as follows:

```bash
uv venv --python 3.11.11Add commentMore actions

./scripts/pre_config_install.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml

uv run install.py --uv --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml

./scripts/post_config_install.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```


Note: The mmcv installed by uv by default may report an error "No module named 'mmcv._ext'" during actual runtime. Refer to [MMCV-FAQ](https://mmcv.readthedocs.io/en/latest/faq.html). The solution is:
```bash
uv pip uninstall mmcv
uv pip install mmcv==2.2.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.4/index.html --trusted-host download.openmmlab.com
```

When running the MuseTalk source code for the first time, it will automatically download a model called s3fd-619a316812.pth. This model is now integrated into the download script. It has already been mapped when starting with Docker. However, when running locally, you need to manually perform the mapping again.

```bash
# linux
ln -s $(pwd)/models/musetalk/s3fd-619a316812/* ~/.cache/torch/hub/checkpoints/
```


To start the program:
```bash
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```


## Optional Deployment

### Prepare ssl certificates
Since we use rtc to stream the video and audio, if not linked from localhost an ssl certificates is needed, user can put exist ones into the ssl_certs folder and config them in the config file or create a new self signed one with the provided script. Run the script under project root to put the result into proper position.
```bash
scripts/create_ssl_certs.sh
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
  chat_engine:
    handler_configs:
      RtcClient: # If using Lam, this config should be LamClient
        turn_config:
          turn_provider: "turn_server"
          urls: ["turn:your-turn-server.com:3478", "turns:your-turn-server.com:5349"]
          username: "your-username"
          credential: "your-credential"
```
* Ensure that the firewall (including cloud machine security group policies) opens the ports required by coturn



## Configuration
The default parameter will load config from **<project_root>/configs/chat_with_minicpm.yaml**. Config can be loaded from other file by add the --config parameter.
```bash
uv run src/demo.py --config <absolute-path-to-the-config>.yaml
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
| LLMOpenAICompatible.model_name     | qwen-plus     | The API for Bailian's testing environment. Free quotas can be obtained from [Bailian](https://bailian.console.aliyun.com/#/home). |
| LLMOpenAICompatible.system_prompt  |               | Default system prompt                                                       |
| LLMOpenAICompatible.api_url        |               | API URL for the model                                                      |
| LLMOpenAICompatible.api_key        |               | API key for the model                                                      |

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

*LiteAvatar Digital Human*

| Parameter                     | Default Value | Description                                                                 |
|-------------------------------|---------------|-----------------------------------------------------------------------------|
| LiteAvatar.avatar_name          | 20250408/sample_data   | Name of the digital human data. 100 avatars provided on ModelScope. Refer to [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery) for more details. |
| LiteAvatar.fps                  | 25            | Frame rate for the digital human. On high-performance CPUs, it can be set to 30 FPS. |
| LiteAvatar.enable_fast_mode     | False          | Low-latency mode. Enabling this reduces response delay but may cause stuttering at the beginning of responses on underpowered systems. |
| LiteAvatar.use_gpu | True | Whether to use GPU acceleration. CUDA backend for now.|


> [!IMPORTANT]
> All path parameters in the configuration can use either absolute paths or paths relative to the project root directory.


## Community Thanks

- Grateful to the volunteers, “十字鱼”, for sharing a video on Bilibili featuring a one-click installation package, along with the download link. (The extraction code is included in the video description—take a close look!) [One-click package](https://www.bilibili.com/video/BV1V1oLYmEu3/?vd_source=29463f5b63a3510553325ba70f325293)
- Grateful to the volunteers, "W&H", for the Quark one-click package [windows version: extract code a79V](https://pan.quark.cn/s/237177126010) and [linux version: extract code: E8Kq](https://pan.quark.cn/s/b7fcdc157586)
- Grateful to the volunteers, "W&H", for the source code zip[Quark:extract code 9iNy](https://pan.quark.cn/s/9e6156cafacd) and [BaiDu:extract code xrxr](https://pan.baidu.com/s/16-0OBtSD5cBz2gJDJORW7w)

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
