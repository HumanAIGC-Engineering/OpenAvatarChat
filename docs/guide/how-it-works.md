# 工作原理

Open Avatar Chat 采用模块化的 Handler 架构，通过配置文件组合不同的 ASR、LLM、TTS 和 Avatar 模块，实现灵活的数字人对话系统。

## 架构概述

系统由以下核心模块组成：

- **Client Handler**：负责 WebRTC 音视频流的接入和传输
- **VAD Handler**：语音活动检测，识别用户说话的起止时间
- **ASR Handler**：语音识别，将用户语音转换为文本
- **LLM Handler**：语言模型推理，生成对话回复
- **Agent Handler**：多轮工具调用 Agent，替代传统 LLM Handler（Beta）
- **TTS Handler**：文本转语音，将回复文本合成为语音
- **Avatar Handler**：数字人驱动，根据语音生成对应的面部动画

## 性能指标

在我们的测试中，使用配备 i9-13900KF 处理器和 Nvidia RTX 4090 显卡的 PC，我们记录了回答的延迟时间。经过十次测试，平均延迟约为 2.2 秒。

延迟时间是从用户语音结束到数字人开始语音的时间间隔，其中包含了 RTC 双向数据传输时间、VAD（语音活动检测）停止延迟以及整个流程的计算时间。

## 数据流

1. 用户通过浏览器发送音视频流（WebRTC）
2. VAD 检测用户是否在说话
3. ASR 将语音转为文本
4. LLM/Agent 生成回复文本
5. TTS 将文本转为语音
6. Avatar 根据语音生成面部动画
7. 合成的音视频流通过 WebRTC 返回给用户
