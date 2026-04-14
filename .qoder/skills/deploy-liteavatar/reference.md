# LiteAvatar 部署技术参考

## 项目架构

### 核心组件

| 组件 | 职责 | 关键文件 |
|------|------|----------|
| VAD | 语音活动检测，控制输入开关 | `vad/silerovad/vad_handler_silero.py` |
| ASR | 语音识别 (SenseVoice) | `asr/sensevoice/asr_handler_sensevoice.py` |
| LLM | 大语言模型对话 | `llm/openai_compatible/llm_handler_openai_compatible.py` |
| TTS | 语音合成 (百炼 CosyVoice) | `tts/bailian_tts/tts_handler_cosyvoice_bailian.py` |
| Avatar | 数字人渲染 (LiteAvatar) | `avatar/liteavatar/avatar_handler_liteavatar.py` |
| Client | WebRTC 客户端 | `client/rtc_client/client_handler_rtc.py` |

### 关键状态变量

```python
# VAD Handler (vad_handler_silero.py)
context.input_enabled: bool  # 控制是否处理音频输入
context.shared_states.enable_vad: bool  # 共享状态，向后兼容

# 状态检查逻辑
is_enabled = context.input_enabled and (
    context.shared_states is None or context.shared_states.enable_vad
)
```

### 信号类型

```python
from chat_engine.data_models.chat_signal import ChatSignalType

ChatSignalType.INPUT_ENABLE   # 启用输入
ChatSignalType.INPUT_DISABLE  # 禁用输入
ChatSignalType.STREAM_END     # 流结束
```

## 配置文件详解

### 百炼云端配置示例

```yaml
# config/chat_with_openai_compatible_bailian_cosyvoice.yaml
handlers:
  - name: RtcClient
    module: client/rtc_client/client_handler_rtc
    
  - name: SileroVad
    module: vad/silerovad/vad_handler_silero
    speaking_threshold: 0.5
    
  - name: SenseVoice
    module: asr/sensevoice/asr_handler_sensevoice
    model_name: iic/SenseVoiceSmall
    
  - name: LLMOpenAICompatible
    module: llm/openai_compatible/llm_handler_openai_compatible
    model_name: qwen-plus
    api_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    
  - name: CosyVoice
    module: tts/bailian_tts/tts_handler_cosyvoice_bailian
    voice: longxiaochun
    model_name: cosyvoice-v1
    
  - name: LiteAvatar
    module: avatar/liteavatar/avatar_handler_liteavatar
    avatar_name: 20250408/sample_data
```

## 依赖配置

### pyproject.toml 关键依赖

```toml
[project]
dependencies = [
    "setuptools>=69.5.1,<70",  # 必须锁定，70+移除pkg_resources
    "torch>=2.5.0",
    "numpy>=1.26.4",
    "loguru>=0.7.2",
    "dashscope>=1.20.6",
    # ... 其他依赖
]

[tool.uv.sources]
torch = { index = "pytorch" }

[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu124"
```

## 多轮对话问题诊断

### 诊断流程

1. **检查 VAD 状态**
   ```python
   # 日志应显示
   "VAD input enabled by signal from LiteAvatar"
   ```

2. **检查 TTS meta**
   ```python
   # 日志应显示
   "speech end"
   "Avatar status changed: SPEAKING_TO_LISTENING"
   ```

3. **检查 INPUT_ENABLE 信号**
   ```python
   # 日志应显示
   "receive output event: SPEAKING_TO_LISTENING"
   ```

### 问题定位表

| 症状 | 可能原因 | 检查点 |
|------|----------|--------|
| 语音不识别 | VAD input_enabled=False | liteavatar_handler_context.py |
| TTS 不结束 | 缺少 avatar_speech_end meta | tts_handler_cosyvoice_bailian.py |
| 文字无响应 | finish_stream 未设置 | client_handler_rtc.py |
| Avatar 不说话 | speech_id 缺失 | TTS handler |

## 代码修改参考

### bailian_tts 完整修改

```python
# tts_handler_cosyvoice_bailian.py

def on_data(self, data: bytes) -> None:
    self.temp_bytes += data
    if len(self.temp_bytes) > 24000:
        output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(np.float32)/32767
        output_audio = output_audio[np.newaxis, ...]
        output = DataBundle(self.output_definition)
        output.set_main_data(output_audio)
        output.add_meta("avatar_speech_end", False)  # 添加
        output.add_meta("speech_id", self.speech_id)  # 添加
        self.context.submit_data(output)
        self.temp_bytes = b''

def on_complete(self) -> None:
    if len(self.temp_bytes) > 0:
        output_audio = np.array(np.frombuffer(self.temp_bytes, dtype=np.int16)).astype(np.float32)/32767
        output_audio = output_audio[np.newaxis, ...]
        output = DataBundle(self.output_definition)
        output.set_main_data(output_audio)
        output.add_meta("avatar_speech_end", False)  # 添加
        output.add_meta("speech_id", self.speech_id)  # 添加
        self.context.submit_data(output)
        self.temp_bytes = b''
    # 发送结束标记
    output = DataBundle(self.output_definition)
    output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
    output.add_meta("avatar_speech_end", True)  # 关键！
    output.add_meta("speech_id", self.speech_id)  # 添加
    self.context.submit_data(output, finish_stream=True)

def on_error(self, message) -> None:
    logger.error(f'bailian tts error: ${message}')
    output = DataBundle(self.output_definition)
    output.set_main_data(np.zeros(shape=(1, 240), dtype=np.float32))
    output.add_meta("avatar_speech_end", True)  # 添加
    output.add_meta("speech_id", self.speech_id)  # 添加
    self.context.submit_data(output, finish_stream=True)
```

### liteavatar_handler_context 完整修改

```python
# liteavatar_handler_context.py

# 添加导入
from chat_engine.data_models.chat_signal import ChatSignal, ChatSignalType, ChatSignalSourceType

def _event_out_loop(self):
    while self.loop_running:
        try:
            event: Tts2FaceEvent = self.lite_avatar_worker.event_out_queue.get(timeout=0.1)
            logger.info("receive output event: {}", event)
            if event == Tts2FaceEvent.SPEAKING_TO_LISTENING:
                self.shared_state.enable_vad = True
                # 发送 INPUT_ENABLE 信号
                enable_signal = ChatSignal(
                    source_type=ChatSignalSourceType.HANDLER,
                    source_name="LiteAvatar",
                    type=ChatSignalType.INPUT_ENABLE,
                )
                self.emit_signal(enable_signal)
        except Exception:
            continue
```

### client_handler_rtc 完整修改

```python
# client_handler_rtc.py

def put_data(self, modality: EngineChannelType, data, timestamp=None, samplerate=None, loopback=False):
    if timestamp is None:
        timestamp = self.get_timestamp()
    if self.data_submitter is None:
        return
    definition = self.input_data_definitions.get(modality)
    chat_data_type = self.modality_mapping.get(modality)
    if chat_data_type is None or definition is None:
        return
    data_bundle = DataBundle(definition)
    is_last_data = False  # 添加
    if modality == EngineChannelType.AUDIO:
        data_bundle.set_main_data(data.squeeze()[np.newaxis, ...])
    elif modality == EngineChannelType.VIDEO:
        data_bundle.set_main_data(data[np.newaxis, ...])
    elif modality == EngineChannelType.TEXT:
        data_bundle.add_meta('human_text_end', True)
        data_bundle.add_meta('speech_id', str(uuid4()))
        data_bundle.set_main_data(data)
        is_last_data = True  # 添加
    else:
        return
    chat_data = ChatData(
        source="client",
        type=chat_data_type,
        data=data_bundle,
        timestamp=timestamp,
    )
    self.data_submitter.submit(chat_data, finish_stream=is_last_data)  # 修改
```

## 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| DASHSCOPE_API_KEY | 百炼 API 密钥 | sk-xxx |
| CUDA_VISIBLE_DEVICES | 指定 GPU | 0 |
