<h1 style='text-align: center; margin-bottom: 1rem'> Open Avatar Chat </h1>

<p align="center">
<strong><a href="README.md">中文</a> | English</strong>
</p>

<p align="center">
<strong>A modular interactive digital human conversation implementation.</strong>
</p>

<p align="center" style="display: flex; flex-direction: row; justify-content: center">
 🤗 <a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp<img alt="Static Badge" style="height: 10px;" src="./assets/images/modelscope_logo.png"> <a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat">Demo</a>&nbsp&nbsp|&nbsp&nbsp💬 <a href="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png">WeChat</a>&nbsp&nbsp|&nbsp&nbsp📖 <a href="https://humanaigc-engineering.github.io/OpenAvatarChat/en/">Docs</a>
</p>

## 💡 Core Highlights

- **Multimodal Interaction**: Supports text, audio, video and other interaction methods for natural human-machine dialogue
- **Modular Architecture**: Highly modular design with flexible ASR, LLM, TTS, and Avatar component replacement
- **Diverse Avatar Options**: Supports LiteAvatar, LAM, MuseTalk, FlashHead and other digital human technologies
- **Low Latency**: Optimized through VAD detection, audio buffering, and frame rate control with ~2.2s average response time

## 📢 News

- [2026.04] ⭐️⭐️⭐️ Version 0.6.0 Released:
  - Architecture refactored with frontend/backend separation: [OpenAvatarChat-WebUI](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)
  - All avatars now support manual interrupt and duplex interrupt modes
  - Optimized installation, deployment, and model download workflow
  - Integrated [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead) diffusion-based real-time streaming talking head
- [2025.08.19] ⭐️⭐️⭐️ Version 0.5.1 Released:
  - LiteAvatar multi-session support
  - Added Qwen-Omni multimodal model support

> 📋 [Full Release Notes](https://humanaigc-engineering.github.io/OpenAvatarChat/en/releases/release-notes)

## Demo

### Try it Online

We have deployed demo services on
<a href="https://www.modelscope.cn/studios/HumanAIGC-Engineering/open-avatar-chat" target="_blank">ModelScope</a>
and
<a href="https://huggingface.co/spaces/HumanAIGC-Engineering-Team/open-avatar-chat" target="_blank">HuggingFace</a>.
Feel free to try it out.

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

## Component Dependencies

| Type | Open Source Project | GitHub Link | Model Link |
|----------|-------------------------------------|---|---|
| RTC      | HumanAIGC-Engineering/gradio-webrtc |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/gradio-webrtc)||
| WebUI      | HumanAIGC-Engineering/OpenAvatarChat-WebUI |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC-Engineering/OpenAvatarChat-WebUI)||
| VAD      | snakers4/silero-vad                 |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/snakers4/silero-vad)||
| Avatar   | HumanAIGC/lite-avatar               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/HumanAIGC/lite-avatar)||
| TTS      | FunAudioLLM/CosyVoice               |[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/FunAudioLLM/CosyVoice)||
|Avatar|aigc3d/LAM_Audio2Expression|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/aigc3d/LAM_Audio2Expression)|[🤗](https://huggingface.co/3DAIGC/LAM_audio2exp)|
||facebook/wav2vec2-base-960h||[🤗](https://huggingface.co/facebook/wav2vec2-base-960h)&nbsp;&nbsp;[<img src="./assets/images/modelscope_logo.png" width="20px"></img>](https://modelscope.cn/models/AI-ModelScope/wav2vec2-base-960h)|
|Avatar|TMElyralab/MuseTalk|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/TMElyralab/MuseTalk)||
|Avatar|Soul-AILab/SoulX-FlashHead|[<img src="https://img.shields.io/badge/github-white?logo=github&logoColor=black"/>](https://github.com/Soul-AILab/SoulX-FlashHead)|[🤗](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B)|
||||||

## 🚀 Quick Start

```bash
# Clone the project
git clone https://github.com/HumanAIGC-Engineering/OpenAvatarChat.git
cd OpenAvatarChat
git submodule update --init --recursive --depth 1

# Install dependencies (LiteAvatar + Bailian API example)
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml

# Download models
uv run scripts/download_models.py --handler liteavatar

# Start
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
```

> 📖 See [Getting Started](https://humanaigc-engineering.github.io/OpenAvatarChat/en/getting-started/) for detailed instructions.

## Preset Modes

| CONFIG Name | ASR | LLM | TTS | AVATAR |
|---|---|:-:|:-:|---|
| chat_with_lam.yaml | SenseVoice | API | API | LAM |
| chat_with_qwen_omni.yaml | Qwen-Omni | Qwen-Omni | Qwen-Omni | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice.yaml | SenseVoice | API | API | lite-avatar |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml | SenseVoice | API | API | FlashHead |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex.yaml | SenseVoice | API | API | FlashHead (Duplex) |
| chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml | SenseVoice | **Agent** | API | FlashHead (Duplex+Agent) Beta |

> 📖 [View all preset modes](https://humanaigc-engineering.github.io/OpenAvatarChat/en/reference/preset-modes)

## 🧪 Beta Features

### Chat Agent Mode (OpenClaw Integration)

> [!WARNING]
> This feature is currently in **Beta**. APIs and configuration formats may change at any time.

Chat Agent mode replaces the traditional LLM Handler with a multi-turn tool-calling Agent, providing:

- **Tool Calling**: Invoke tools across multiple turns (get time, system info, etc.)
- **Persona & Long-term Memory**: Persistent persona through OpenClaw's Agent Profile
- **Context Compression**: Automatically compresses long conversation history
- **Background Task Collaboration**: Execute complex tasks via OpenClaw in the background
- **Visual Perception**: Camera input processing via PerceptionAgent

> 📖 [Full Chat Agent documentation](https://humanaigc-engineering.github.io/OpenAvatarChat/en/beta/chat-agent)

## Community

* WeChat Group

<img alt="community_wechat.png" height="200" src="https://github.com/HumanAIGC-Engineering/OpenAvatarChat/blob/main/assets/images/community_wechat.png" width="200"/>

* 🚨 [FAQ](https://humanaigc-engineering.github.io/OpenAvatarChat/en/community/faq)

## Community Thanks

- One-click installation package by "Shi Zi Yu" on [Bilibili](https://www.bilibili.com/video/BV1V1oLYmEu3/)
- Quark one-click packages by "W&H": [Windows (code: a79V)](https://pan.quark.cn/s/237177126010) / [Linux (code: E8Kq)](https://pan.quark.cn/s/b7fcdc157586)
- Source code zip by "W&H": [Quark (code: 9iNy)](https://pan.quark.cn/s/9e6156cafacd) / [Baidu (code: xrxr)](https://pan.baidu.com/s/16-0OBtSD5cBz2gJDJORW7w)

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
