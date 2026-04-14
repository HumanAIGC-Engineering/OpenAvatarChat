---
name: deploy-liteavatar
description: 使用 uv 部署 LiteAvatar 数字人系统，解决依赖冲突、多轮对话问题。当用户需要部署 Open Avatar Chat、LiteAvatar 数字人、或遇到 pkg_resources、多轮对话、VAD 状态问题时使用。
---

# LiteAvatar 数字人 uv 部署指南

## 概述

本 skill 指导如何使用 uv 包管理工具部署 LiteAvatar 数字人系统，包含常见问题的解决方案。

## 前置要求

- Python 3.11
- CUDA >= 12.4
- uv 包管理工具
- 百炼 API Key（DASHSCOPE）

## 部署步骤

### 1. 初始化子模块

```bash
git submodule update --init --recursive
```

### 2. 修复 setuptools 版本约束

**关键问题**：setuptools 70+ 移除了 `pkg_resources` 模块，导致 LiteAvatar 子进程启动失败。

修改 `pyproject.toml`：
```toml
# 修改前（错误）
"setuptools>=78.1.0",

# 修改后（正确）
"setuptools>=69.5.1,<70",  # pkg_resources 在 setuptools 70+ 中被移除
```

### 3. 配置环境变量

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

### 4. 启动服务

```bash
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml
```

## 常见问题修复

### 问题1：ModuleNotFoundError: pkg_resources

**症状**：LiteAvatar 子进程启动失败，日志显示 `No module named 'pkg_resources'`

**原因**：setuptools 70+ 版本移除了 pkg_resources 模块

**解决**：锁定 setuptools 版本 `>=69.5.1,<70`

### 问题2：多轮语音对话不工作

**症状**：第一轮对话正常，后续语音对话无响应

**原因**：VAD 的 `input_enabled` 和 `enable_vad` 状态未正确恢复

**涉及文件**：
- `src/handlers/tts/bailian_tts/tts_handler_cosyvoice_bailian.py`
- `src/handlers/avatar/liteavatar/liteavatar_handler_context.py`

**修复1 - TTS 添加 meta**：

在 `tts_handler_cosyvoice_bailian.py` 的 `on_data`、`on_complete`、`on_error` 方法中添加：
```python
output.add_meta("avatar_speech_end", False)  # on_data 中
output.add_meta("avatar_speech_end", True)   # on_complete/on_error 最后一个输出
output.add_meta("speech_id", self.speech_id)
```

**修复2 - LiteAvatar 发送 INPUT_ENABLE 信号**：

在 `liteavatar_handler_context.py` 的 `_event_out_loop` 中：
```python
if event == Tts2FaceEvent.SPEAKING_TO_LISTENING:
    self.shared_state.enable_vad = True
    # 添加以下代码发送 INPUT_ENABLE 信号
    enable_signal = ChatSignal(
        source_type=ChatSignalSourceType.HANDLER,
        source_name="LiteAvatar",
        type=ChatSignalType.INPUT_ENABLE,
    )
    self.emit_signal(enable_signal)
```

### 问题3：多轮文字对话不工作

**症状**：发送文字消息后 LLM 无响应

**原因**：RTC client 的 `put_data` 方法未设置 `finish_stream=True`

**涉及文件**：`src/handlers/client/rtc_client/client_handler_rtc.py`

**修复**：
```python
def put_data(self, modality, data, ...):
    ...
    is_last_data = False
    if modality == EngineChannelType.TEXT:
        data_bundle.add_meta('human_text_end', True)
        data_bundle.add_meta('speech_id', str(uuid4()))
        is_last_data = True  # 文本消息立即完成
    ...
    self.data_submitter.submit(chat_data, finish_stream=is_last_data)
```

## 数据流架构

```
用户语音 → VAD → ASR → LLM → TTS → Avatar → 视频输出
              ↑                      ↓
              └── INPUT_ENABLE ←── SPEAKING_TO_LISTENING
```

**关键状态转换**：
1. 用户说话结束 → VAD 设置 `input_enabled=False`
2. TTS 完成 → 发送 `avatar_speech_end=True`
3. Avatar 检测语音结束 → 触发 `SPEAKING_TO_LISTENING`
4. LiteAvatar 发送 `INPUT_ENABLE` 信号 → VAD 恢复 `input_enabled=True`

## 验证清单

- [ ] pyproject.toml 中 setuptools 版本为 `>=69.5.1,<70`
- [ ] 子模块已初始化（前端文件存在）
- [ ] bailian_tts 包含 avatar_speech_end/speech_id meta
- [ ] liteavatar_handler_context 发送 INPUT_ENABLE 信号
- [ ] client_handler_rtc 文本消息设置 finish_stream=True
- [ ] 服务启动无 pkg_resources 错误
- [ ] 多轮语音对话正常
- [ ] 多轮文字对话正常
