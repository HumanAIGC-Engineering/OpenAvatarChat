# MuseTalk Avatar Handler 技术文档

## 1. 模块概览

MuseTalk 是一个基于扩散模型的实时数字人唇动驱动方案。它接收上游 TTS 输出的 `AVATAR_AUDIO` 音频流，通过多线程 Pipeline 实时生成唇形同步的视频帧和音频帧，输出 `AVATAR_VIDEO` + `AVATAR_AUDIO` 供下游 Client Handler 渲染。

### 1.1 文件结构

```
src/handlers/avatar/musetalk/
├── avatar_handler_musetalk.py      # Handler 入口 + ProcessorPool + Context
├── musetalk_processor.py           # 多线程 Pipeline（4~5 个 Worker）
├── musetalk_algo.py                # GPU 算法核心（MuseTalkAlgoV15）
├── musetalk_config.py              # Pydantic 配置模型
├── musetalk_data_models.py         # 数据结构定义（队列项、回调、状态枚举）
├── musetalk_utils_preprocessing.py # 人脸预处理（DWPose ONNX + S3FD face_detection）
├── MuseTalk/                       # 原始 MuseTalk 第三方代码（git submodule）
└── __init__.py
```

### 1.2 类关系图

```
HandlerAvatarMuseTalk (HandlerBase)          ← ChatEngine 加载的 Handler 入口
 ├── MuseTalkAlgoV15                          ← 唯一实例，所有 GPU 操作（线程安全）
 ├── MuseTalkProcessorPool                    ← Processor 对象池
 │    └── AvatarMuseTalkProcessor × N         ← 每个 Processor 拥有独立的线程 Pipeline
 └── AvatarMuseTalkConfig                     ← 配置

AvatarMuseTalkContext (HandlerContext)        ← 每个会话（session）一个
 ├── processor: AvatarMuseTalkProcessor       ← 从 Pool 中租借
 ├── input_slice_context: SliceContext         ← 音频切片器
 └── MuseTalkProcessorCallbacks               ← 回调桥接 Processor → Engine
```

---

## 2. 核心类详解

### 2.1 HandlerAvatarMuseTalk

**文件**: `avatar_handler_musetalk.py`  
**父类**: `HandlerBase`

Handler 的生命周期方法：

| 方法 | 调用时机 | 说明 |
|------|----------|------|
| `load()` | 服务启动 | 初始化 `MuseTalkAlgoV15`（加载所有 GPU 模型）和 `MuseTalkProcessorPool` |
| `create_context()` | 新会话接入 | 从 Pool 中 `acquire()` 一个 Processor，创建 `AvatarMuseTalkContext` |
| `start_context()` | 会话开始 | 调用 `init_playback_streamer()` + `processor.start()` 启动所有 Worker 线程 |
| `get_handler_detail()` | 引擎查询 | 返回 I/O 声明和信号过滤规则 |
| `handle()` | 收到 AVATAR_AUDIO | 音频切片 → `processor.add_audio()` |
| `on_signal()` | 收到 STREAM_CANCEL | 调用 `context.interrupt()` 打断当前语音 |
| `destroy_context()` | 会话断开 | 停止 Processor，释放回 Pool |
| `destroy()` | 服务关闭 | 销毁整个 Pool |

#### 2.1.1 get_handler_info()

```python
HandlerBaseInfo(
    config_model=AvatarMuseTalkConfig,
    load_priority=-999,  # 低优先级，确保其他 Handler 先加载
)
```

#### 2.1.2 load() 详细流程

```
1. 验证/创建 handler_config（AvatarMuseTalkConfig）
2. 构建 DataBundleDefinition:
   ├── AVATAR_AUDIO: 单通道音频, sample_rate=output_audio_sample_rate
   └── AVATAR_VIDEO: 可变尺寸视频帧 [VariableSize, VariableSize, VariableSize, 3], fps=config.fps
3. 组装模型路径:
   ├── unet_model_path = {project_root}/{model_dir}/musetalkV15/unet.pth
   ├── unet_config     = {project_root}/{model_dir}/musetalkV15/musetalk.json
   └── whisper_dir     = {project_root}/{model_dir}/whisper
4. 自动生成 avatar_id = "avatar_{video_basename}_{md5(video_path)[:8]}"
5. 创建 MuseTalkAlgoV15 实例（包括所有 GPU 模型加载和 Avatar 数据准备）
6. 创建 MuseTalkProcessorPool（pool_size = concurrent_limit）
```

`MuseTalkAlgoV15.__init__()` 内部会调用 `init()`，`init()` 中加载所有 GPU 模型并准备/加载 Avatar 数据，因此 `load()` 是一个耗时操作。

#### 2.1.3 create_context() 详细流程

```python
def create_context(self, session_context, handler_config) -> HandlerContext:
    # 1. 从 Pool 中获取空闲 Processor
    processor = self.processor_pool.acquire()
    # → 如果无空闲，抛出 RuntimeError

    try:
        # 2. 创建 Context
        context = AvatarMuseTalkContext(session_id, processor)
        context.output_data_definitions = self.output_data_definitions
        context.config = handler_config

        # 3. 构建回调桥接
        callbacks = context._build_callbacks()
        processor.set_callbacks(callbacks)

        # 4. 验证采样率/帧率对齐（防御性断言）
        assert output_audio_sample_rate % fps == 0

        # 5. 初始化音频切片器
        context.input_slice_context = SliceContext.create_numpy_slice_context(
            slice_size=output_audio_sample_rate,  # 每段 1 秒
            slice_axis=0,
        )
        return context
    except Exception:
        # 创建失败时释放 Processor 回 Pool，防止泄漏
        processor.set_callbacks(None)
        self.processor_pool.release(processor)
        raise
```

#### 2.1.4 start_context() 详细流程

```python
def start_context(self, session_context, handler_context):
    context = cast(AvatarMuseTalkContext, handler_context)
    context.init_playback_streamer()  # 预创建 CLIENT_PLAYBACK 生命周期流
    context.processor.start()          # 启动所有 Worker 线程
```

`init_playback_streamer()` 在 `start_context()` 中提前创建（eager），而不是在第一次使用时懒创建，确保 `stream_manager` 已就绪。

#### 2.1.5 get_handler_detail() 详细说明

```python
def get_handler_detail(self, session_context, context) -> HandlerDetail:
    inputs = {
        ChatDataType.AVATAR_AUDIO: HandlerDataInfo(
            type=ChatDataType.AVATAR_AUDIO,
            input_consume_mode=ChatDataConsumeMode.ONCE,  # 每条数据只消费一次
        )
    }
    outputs = {
        ChatDataType.AVATAR_AUDIO: HandlerDataInfo(...),
        ChatDataType.AVATAR_VIDEO: HandlerDataInfo(
            ...,
            output_stream_config=ChatStreamConfig(
                cancelable=False,       # 视频流不可被上游取消
                auto_link_input=False,  # 不自动关联输入流
            ),
        ),
    }
    signal_filters = [
        # 仅监听 CLIENT_PLAYBACK 的 STREAM_CANCEL 信号
        SignalFilterRule(ChatSignalType.STREAM_CANCEL, None, ChatDataType.CLIENT_PLAYBACK),
    ]
```

Handler 只关心 `CLIENT_PLAYBACK` 类型流的 `STREAM_CANCEL` 信号。这个信号在上游 TTS/LLM 被打断时由 Engine 发出。Handler 不直接监听 `INTERRUPT` 信号——打断通过 CLIENT_PLAYBACK 流的取消间接传达。

#### 2.1.6 handle() 详细流程

```
handle(context, inputs, output_definitions):
    │
    ├── 1. 类型检查: inputs.type != AVATAR_AUDIO → 直接返回
    │
    ├── 2. stream_key 变化检测（线程安全，使用 _stream_key_lock）
    │      │
    │      ├── 获取 stream_key_str (from inputs.stream_id)
    │      ├── 与 context._current_tts_stream_key 比较
    │      ├── need_switch = (stream_key_str 存在 且 与当前不同)
    │      │
    │      └── if need_switch:
    │            ├── flush 切片器残余音频（丢弃，不处理）
    │            ├── 关闭上一个 CLIENT_PLAYBACK 流 (streamer.finish_current())
    │            └── 为新 stream 打开 CLIENT_PLAYBACK 流 (streamer.open_stream())
    │
    ├── 3. 输入验证
    │      ├── 检查 sample_rate 是否匹配 output_audio_sample_rate（不匹配则返回）
    │      ├── 音频数据 dtype 转 float32（如需要）
    │      └── 音频数据为 None 时填充 1 秒静音（容错）
    │
    ├── 4. 音频切片（SliceContext，按 output_audio_sample_rate 切为 1 秒段）
    │      对每段:
    │        audio_segment → MuseTalkSpeechAudio(speech_id, end_of_speech=False, audio_data=bytes)
    │        → context.processor.add_audio(speech_audio)
    │
    └── 5. speech_end 处理（inputs.is_last_data == True）
           ├── flush 切片器残余音频
           │   ├── 有残余 → 使用残余数据
           │   └── 无残余 → 用 2 帧长度的静音填充（确保 speech_end 信号有足够帧来传递）
           └── MuseTalkSpeechAudio(speech_id, end_of_speech=True, audio_data=...)
               → context.processor.add_audio(speech_audio)
```

**speech_end 静音填充原因**: 当最后一段数据刚好被切片器完整消费时，flush 返回 None。此时仍需一个非空的 `end_of_speech=True` 音频段来驱动 Pipeline 产生 `on_speech_end` 回调。填充 2 帧长度（`2 * input_sample_rate // fps`）的静音确保 Feature Extractor 至少能产生 2 个 WhisperQueueItem，其中最后一个携带 `end_of_speech=True`。

#### 2.1.7 on_signal() 详细说明

```python
def on_signal(self, context, signal):
    if signal.type == ChatSignalType.STREAM_CANCEL \
       and signal.related_stream.data_type == ChatDataType.CLIENT_PLAYBACK:
        context.interrupt()
```

没有单独的 `INTERRUPT` 信号处理。打断机制完全通过 `CLIENT_PLAYBACK` 流的取消来实现。

#### 2.1.8 destroy_context() 详细流程

```python
def destroy_context(self, context):
    if isinstance(context, AvatarMuseTalkContext):
        # 1. 关闭 CLIENT_PLAYBACK 流（容错，忽略异常）
        if context._playback_streamer is not None:
            context._playback_streamer.finish_current()

        # 2. 停止 Processor + 清除回调 + 归还 Pool
        processor = context.processor
        if processor:
            processor.stop()
            processor.set_callbacks(None)
            self.processor_pool.release(processor)

        # 3. 清理 Context
        context.clear()
```

执行顺序很重要：先 `stop()` 确保没有线程在运行回调，再 `set_callbacks(None)` 断开引用，最后 `release()` 允许 Pool 复用。

---

### 2.2 MuseTalkProcessorPool

**文件**: `avatar_handler_musetalk.py`

简单的对象池模式，管理 N 个 `AvatarMuseTalkProcessor` 实例：

- `acquire()`: 获取空闲 Processor（线程安全，使用 `_lock`）
- `release()`: 归还 Processor（线程安全，使用 `_lock`）
- `destroy()`: 无条件停止所有 Processor（无论是否正在运行），逐个 try/except 容错

Pool 大小由配置中的 `concurrent_limit` 决定（默认为 2）。所有 Processor **共享同一个 `MuseTalkAlgoV15` 实例**，GPU 操作通过 `_inference_lock` 串行化。

```python
class MuseTalkProcessorPool:
    _lock: threading.Lock         # 保护 acquire/release
    _processors: List[Processor]  # 所有 Processor 实例
    _active: List[bool]           # 每个 Processor 的占用状态
```

- `acquire()` 线性扫描 `_active` 列表，找到第一个 `False` 的位置
- `release()` 线性扫描 `_processors` 列表，找到匹配的实例并标记为 `False`
- 当所有 Processor 都被占用时，`acquire()` 返回 `None`（不阻塞等待）

---

### 2.3 AvatarMuseTalkContext

**文件**: `avatar_handler_musetalk.py`  
**父类**: `HandlerContext`

每个会话（WebRTC 连接）对应一个 Context。核心职责：

1. **持有 Processor 引用**: 会话期间独占一个 Processor
2. **构建回调桥接**: `_build_callbacks()` 创建 `MuseTalkProcessorCallbacks`
3. **管理 CLIENT_PLAYBACK 流**: 通过 `init_playback_streamer()` / `get_playback_streamer()` 管理生命周期
4. **音频切片**: `input_slice_context` 将变长音频切为固定 1 秒段
5. **打断**: `interrupt()` 清空 Processor 队列 + flush 切片器

#### 2.3.1 关键成员变量

```python
class AvatarMuseTalkContext(HandlerContext):
    config: Optional[AvatarMuseTalkConfig]              # 会话级配置
    processor: AvatarMuseTalkProcessor                   # 从 Pool 租借的 Processor
    input_slice_context: Optional[SliceContext]           # 音频切片器
    output_data_definitions: Dict[ChatDataType, DataBundleDefinition]  # 输出格式定义

    _current_tts_stream_key: Optional[str]               # 当前 TTS 流的 stream_key
    _stream_key_lock: threading.Lock                     # 保护 _current_tts_stream_key
    _playback_streamer                                   # CLIENT_PLAYBACK 生命周期流
```

#### 2.3.2 回调桥接 (_build_callbacks)

```
Processor Worker 线程                      Context 回调                          Engine
    │                                          │                                    │
    ├── _notify_video(frame)    ──→   on_video_frame()   ──→  _return_data()  ──→  submit_data(AVATAR_VIDEO)
    │                                                          ├── DataBundle 封装
    │                                                          ├── video: data[np.newaxis, ...]
    │                                                          └── shape: [1, H, W, 3]
    │
    ├── _notify_audio(audio)    ──→   on_audio_frame()   ──→  _return_data()  ──→  submit_data(AVATAR_AUDIO)
    │                                                          ├── DataBundle 封装
    │                                                          ├── dtype 检查: 非 float32 → 转换
    │                                                          ├── ndim 检查: 1D → [1, N]
    │                                                          ├── shape 检查: [C, N] 且 C≠1 → 截取 [:1, ...]
    │                                                          └── None → zeros [1, 0]
    │
    └── _notify_speech_end(id)  ──→   on_speech_end()
                                       ├── 获取 _stream_key_lock
                                       ├── 检查 _current_tts_stream_key:
                                       │   ├── None → 忽略（已被打断）
                                       │   └── speech_id 不匹配 current_key → 忽略 + warning
                                       ├── 清空 _current_tts_stream_key = None
                                       └── streamer.finish_current() → 关闭 CLIENT_PLAYBACK 流
```

**on_speech_end 的 speech_id 校验**: Processor 的 `_frame_collector_worker` 在遇到 `end_of_speech=True` 时回调 `on_speech_end(speech_id)`。Context 会将 `speech_id` 与当前活跃的 `_current_tts_stream_key` 比较：
- **匹配**: 正常关闭 CLIENT_PLAYBACK 流
- **不匹配**: 说明这是一条过时的回调（来自已被打断的旧 speech），跳过关闭
- **current_key 为 None**: 说明已经被打断过（`interrupt()` 会清空 `_current_tts_stream_key`），跳过

#### 2.3.3 _return_data() 数据封装

```python
def _return_data(self, data: np.ndarray, chat_data_type: ChatDataType):
    definition = self.output_data_definitions.get(chat_data_type)
    data_bundle = DataBundle(definition)

    if channel_type == AUDIO:
        # 格式规范化:
        # - dtype 必须为 float32
        # - shape 必须为 [1, N]（单通道）
        # - None → zeros [1, 0]
        data_bundle.set_main_data(data)

    elif channel_type == VIDEO:
        # 增加 batch 维度: [H, W, 3] → [1, H, W, 3]
        data_bundle.set_main_data(data[np.newaxis, ...])

    chat_data = ChatData(type=chat_data_type, data=data_bundle)
    self.submit_data(chat_data)
```

#### 2.3.4 interrupt() 详细流程

```python
def interrupt(self):
    # 1. 清除当前 stream_key（线程安全）
    with self._stream_key_lock:
        self._current_tts_stream_key = None

    # 2. 关闭 CLIENT_PLAYBACK 流（幂等，重复调用安全）
    if self._playback_streamer is not None:
        self._playback_streamer.finish_current()

    # 3. 打断 Processor pipeline
    if self.processor is not None:
        self.processor.interrupt()

    # 4. 清空音频切片器残余数据（丢弃）
    if self.input_slice_context is not None:
        discarded = self.input_slice_context.flush()
```

**打断的完整链路**: 
```
STREAM_CANCEL 信号 → on_signal() → context.interrupt()
    → _current_tts_stream_key = None  (阻止后续 on_speech_end 关闭流)
    → _playback_streamer.finish_current()  (立即关闭客户端播放)
    → processor.interrupt()  (清空所有 Pipeline 队列)
    → input_slice_context.flush()  (丢弃切片器缓存)
```

---

### 2.4 AvatarMuseTalkProcessor

**文件**: `musetalk_processor.py`

这是整个模块的**核心引擎**，实现了一个多线程 Pipeline 将音频流转换为同步的音视频帧。

#### 2.4.1 关键成员变量

```python
class AvatarMuseTalkProcessor:
    _avatar: MuseTalkAlgoV15              # 共享的 GPU 算法实例
    _config: AvatarMuseTalkConfig         # 配置
    _callbacks: MuseTalkProcessorCallbacks # 输出回调

    # 队列
    _audio_queue: Queue                    # AudioQueueItem
    _whisper_queue: Queue                  # WhisperQueueItem
    _unet_queue: Queue                     # UNetQueueItem (仅 multi_thread_inference 模式)
    _frame_id_queue: Queue                 # int (Frame Collector → Frame Generator 的背压队列)
    _compose_queue: Queue                  # ComposeQueueItem
    _output_queue: Queue                   # ComposeQueueItem (with frame field set)

    # 线程
    _feature_thread: Thread                # Feature Extractor Worker
    _frame_gen_thread: Thread              # Frame Generator (single-thread mode)
    _frame_gen_unet_thread: Thread         # UNet Worker (multi-thread mode)
    _frame_gen_vae_thread: Thread          # VAE Worker (multi-thread mode)
    _compose_thread: Thread                # Compose Worker
    _frame_collect_thread: Thread          # Frame Collector Worker

    # 状态
    _stop_event: threading.Event           # 停止信号
    _session_running: bool                 # 是否正在运行
    _interrupted: threading.Event          # 打断标志
    _generation_id: int                    # 单调递增计数器（用于区分新旧数据）
    _generation_lock: threading.Lock       # 保护 _generation_id
    _frame_id_lock: threading.Lock         # 保护队列清空操作
```

#### 2.4.2 生命周期

```
创建(Pool.__init__)  →  set_callbacks()  →  start()  →  add_audio() ...  →  stop()  →  release()
                                                         interrupt() ...
```

#### 2.4.3 start() 详细流程

```python
def start(self):
    # 1. 防重入检查
    if self._session_running:
        return

    # 2. 重置运行时状态
    _reset_runtime_state()  # 清空所有队列 + 清除 _interrupted

    # 3. 设置运行标志
    _session_running = True
    _stop_event.clear()

    # 4. 创建并启动 Worker 线程
    try:
        # 根据 multi_thread_inference 配置决定线程结构:
        # True:  Feature + UNet + VAE + Compose + Collector = 5 线程
        # False: Feature + FrameGen + Compose + Collector = 4 线程
        ...
    except Exception:
        # 回滚状态，避免 stop() 混淆
        _session_running = False
        _stop_event.set()
        raise
```

Worker 线程不设置 `daemon=True`，确保进程关闭时线程能被完整回收。`stop()` 通过 `join(timeout=5)` 优雅等待退出。

#### 2.4.4 stop() 详细流程

```python
def stop(self):
    # 1. 防重入检查
    if not self._session_running:
        return

    # 2. 标记停止
    _session_running = False
    _stop_event.set()

    # 3. 等待所有线程退出 (timeout=5s each)
    for thread in all_threads:
        if thread is not None:
            thread.join(timeout=5)
            if thread.is_alive():
                logger.error(f"{name} thread did not exit in time.")

    # 4. 清空所有队列
    _clear_queues()

    # 5. 重置线程引用为 None（允许下次 start() 干净启动）
```

#### 2.4.5 add_audio() 详细流程

```python
def add_audio(self, speech_audio: MuseTalkSpeechAudio):
    # 1. 数据格式转换: bytes → np.frombuffer(float32) 或 ndarray → astype(float32)

    # 2. 输入验证
    #    ├── 空音频 → 返回
    #    ├── 超过 1 秒 (len > output_audio_sample_rate) → 返回
    #    └── 采样率不匹配 → 返回

    # 3. 音频延迟检测（WARNING 级别）
    #    跟踪 cumulative_audio_duration vs wall_clock
    #    如果 cumulative < wall_clock → logger.warning("[AUDIO_LAG]")
    #    end_of_speech 时重置统计

    # 4. 获取当前 generation_id（加锁）
    with self._generation_lock:
        gen_id = self._generation_id

    # 5. 放入 _audio_queue（timeout=1s）
    self._audio_queue.put(AudioQueueItem(
        audio_data=audio_data,
        speech_id=speech_audio.speech_id,
        end_of_speech=speech_audio.end_of_speech,
        generation_id=gen_id,
    ), timeout=1)

    # 6. 条件清除中断标志
    with self._generation_lock:
        if self._generation_id == gen_id:
            self._interrupted.clear()
```

**generation_id 机制**:
- `interrupt()` 会递增 `_generation_id` 并设置 `_interrupted`
- `add_audio()` 在放入数据**前**读取 `_generation_id`，在放入**后**检查是否仍是同一代
- 如果 `add_audio()` 和 `interrupt()` 发生竞态:
  - `add_audio()` 先读到 gen_id=N，然后 `interrupt()` 将其改为 N+1
  - 放入队列后检查发现 `_generation_id != gen_id`，**不清除** `_interrupted`
  - Feature Extractor 检查 `item.generation_id != self._generation_id` 也会丢弃这个过时数据
- 这解决了传统方案中 `add_audio()` 简单 `clear()` `_interrupted` 可能覆盖并发 `interrupt()` 的竞态问题

#### 2.4.6 interrupt() 详细流程

```python
def interrupt(self):
    # 1. 递增 generation_id（使所有已入队数据失效）
    with self._generation_lock:
        self._generation_id += 1

    # 2. 设置中断标志
    self._interrupted.set()

    # 3. 清空所有队列（加锁防止与 _clear_queues 并发）
    with self._frame_id_lock:
        for q in [_audio_queue, _whisper_queue, _unet_queue,
                  _frame_id_queue, _compose_queue, _output_queue]:
            while not q.empty():
                q.get_nowait()

    # 4. 重置音频统计
    _audio_duration_sum = 0.0
    _first_add_audio_time = None
```

**两级中断机制**:
1. **generation_id**: 让 Feature Extractor 可以识别并丢弃过时数据（即使已经在队列中但尚未被清空）
2. **_interrupted Event**: 让所有 Worker 在处理循环中快速跳过当前数据

---

#### 2.4.7 线程架构（multi_thread_inference=True，默认）

UNet 和 VAE 拆分为独立线程，形成 5 线程 Pipeline：

```
add_audio()
    │
    ▼
┌──────────────────┐
│  _audio_queue     │  AudioQueueItem (float32 ndarray, output_sample_rate)
└────────┬─────────┘      + generation_id（用于过时数据检测）
         │
         ▼
┌──────────────────┐
│ Feature Extractor │  Thread #1: librosa 重采样 → Whisper 特征提取 → 按帧拆分
│ Worker            │  每帧一个 WhisperQueueItem
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  _whisper_queue   │  WhisperQueueItem (whisper_chunk[1,50,384] + audio_segment)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ UNet Worker       │  Thread #2: 收集 batch_size 个 chunk → 批量 UNet 推理
│                   │  等待 _frame_id_queue 获取帧号（背压控制）
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  _unet_queue      │  UNetQueueItem (pred_latents[B,4,32,32] + metadata)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ VAE Worker        │  Thread #3: VAE 解码 pred_latents → 人脸裁剪图
│                   │  拆分 batch 为单帧 ComposeQueueItem
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  _compose_queue   │  ComposeQueueItem (recon[256,256,3] + idx + audio_segment)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Compose Worker    │  Thread #4: res2combined()，将人脸裁剪合成到全帧
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  _output_queue    │  ComposeQueueItem (with frame field set, 完整帧)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Frame Collector   │  Thread #5: 严格按 fps 定时输出
│ Worker            │  有说话帧 → 输出说话帧 + 音频
│                   │  无说话帧 → 输出 idle 静态帧（无音频）
│                   │  分配 frame_id → _frame_id_queue（反馈给 UNet Worker）
└──────────────────┘
         │
         ▼
    回调输出: on_video_frame() / on_audio_frame() / on_speech_end()
```

#### 2.4.8 multi_thread_inference=False 模式

UNet + VAE 合并为单个 `_frame_generator_worker`（Thread #2），直接输出到 `_compose_queue`，跳过 `_unet_queue`。线程总数从 5 个减少到 4 个。

```
_whisper_queue → Frame Generator Worker (UNet+VAE) → _compose_queue → ...
                  (跳过 _unet_queue)
```

---

#### 2.4.9 Feature Extractor Worker 详细逻辑

```python
def _feature_extractor_worker(self):
    # CUDA 预热: 1 秒静音 dummy → extract_whisper_feature()

    while not _stop_event.is_set():
        # 1. 从 _audio_queue 取数据 (timeout=1s)
        item: AudioQueueItem = _audio_queue.get(timeout=1)

        # 2. generation_id 校验: 过时数据直接丢弃
        if item.generation_id != self._generation_id:
            continue

        # 3. librosa 重采样: output_audio_sample_rate → algo_audio_sample_rate (e.g. 24kHz→16kHz)
        segment = librosa.resample(audio_data, orig_sr=..., target_sr=16000)

        # 4. 长度规范化: padding 到正好 algo_audio_sample_rate (1秒) 的长度
        if len(segment) < target_len:
            segment = np.pad(segment, ...)  # 零填充

        # 5. Whisper 特征提取 (GPU 操作，通过 _inference_lock)
        whisper_chunks = self._avatar.extract_whisper_feature(segment, 16000)
        # whisper_chunks shape: [num_frames, 50, 384]

        # 6. 帧对齐计算
        samples_per_frame = output_audio_sample_rate // fps
        num_frames = ceil(actual_audio_len / samples_per_frame)
        whisper_chunks = whisper_chunks[:num_frames]

        # 7. 原始音频对齐（padding 到帧边界）
        target_audio_len = num_frames * samples_per_frame
        audio_data = pad_or_truncate(audio_data, target_audio_len)

        # 8. 中断检查
        if _interrupted.is_set():
            continue

        # 9. 按帧拆分入队
        for i in range(num_chunks):
            if _interrupted.is_set():
                break
            whisper_chunk = whisper_chunks[i:i+1]  # shape: [1, 50, 384]
            audio_segment = audio_data[i*samples_per_frame : (i+1)*samples_per_frame]
            is_last_chunk = (i == num_chunks - 1)
            _whisper_queue.put(WhisperQueueItem(
                whisper_chunks=whisper_chunk,
                speech_id=speech_id,
                end_of_speech=end_of_speech and is_last_chunk,
                audio_data=audio_segment,
            ))
```

**帧对齐关键计算**:
- `samples_per_frame = output_audio_sample_rate // fps` (例: 24000 // 20 = 1200)
- `num_frames = ceil(actual_audio_len / samples_per_frame)` (例: ceil(24000/1200) = 20)
- 每个 Whisper chunk 对应一帧视频，携带对应的 1200 samples 原始音频

**end_of_speech 传递**: `end_of_speech=True` 仅在最后一个 chunk（`is_last_chunk`）上标记，确保只触发一次 speech_end 回调。

---

#### 2.4.10 _collect_batch() 共享方法

`_collect_batch()` 被 UNet Worker（`_frame_generator_unet_worker`）和单线程 Frame Generator（`_frame_generator_worker`）共用。

```python
def _collect_batch(self):
    """从 _whisper_queue 收集完整 batch，支持 padding。"""
    batch_size = config.batch_size
    max_speaking_buffer = batch_size * 5  # _output_queue 背压阈值

    while not _stop_event.is_set():
        # 中断处理: 清空已收集的 partial batch
        if _interrupted.is_set():
            batch.clear()
            time.sleep(0.01)
            continue

        # 背压: _output_queue 过满时暂停
        while _output_queue.qsize() > max_speaking_buffer:
            time.sleep(0.01)

        # 从 _whisper_queue 取数据 (timeout=1s)
        item: WhisperQueueItem = _whisper_queue.get(timeout=1)

        # 二次中断检查（取到数据后）
        if _interrupted.is_set():
            batch.clear()
            continue

        batch.append(item)

        # 当收集满 batch_size 或遇到 end_of_speech 时提交
        if len(batch) == batch_size or item.end_of_speech:
            valid_num = len(batch)

            # 不足 batch_size 时 padding（零填充）
            if valid_num < batch_size:
                batch.extend(zero_padding)

            # 拼接 whisper_batch: [B, 50, 384]
            whisper_batch = torch.cat(batch_chunks, dim=0)

            # 获取 frame_ids（背压核心：阻塞等待 Frame Collector 分配）
            frame_ids = []
            for _ in range(batch_size):
                while not _stop_event.is_set():
                    if _interrupted.is_set():
                        return None
                    frame_id = _frame_id_queue.get(timeout=0.5)
                    frame_ids.append(frame_id)
                    break

            return (whisper_batch, batch_audio, batch_speech_id,
                    batch_end_of_speech, valid_num, frame_ids)
```

**背压（backpressure）机制**:
1. **_output_queue 背压**: `_output_queue.qsize() > batch_size * 5` 时暂停收集新 batch
2. **_frame_id_queue 背压**: 等待 Frame Collector 分配 frame_id，如果推理过快，这里会阻塞

**end_of_speech 触发 batch 提交**: 即使 batch 未满，遇到 `end_of_speech=True` 也会立即提交，避免 speech_end 信号被延迟。不足的部分用零 padding 填充。

---

#### 2.4.11 UNet Worker (_frame_generator_unet_worker)

```python
def _frame_generator_unet_worker(self):
    # CUDA 预热: dummy_whisper[batch_size, 50, 384] → generate_frames_unet()

    while not _stop_event.is_set():
        # 1. 收集 batch（复用 _collect_batch()）
        result = _collect_batch()
        if result is None:
            continue

        # 2. UNet 推理 (GPU, 通过 _inference_lock)
        try:
            pred_latents, idx_list = _avatar.generate_frames_unet(
                whisper_batch, frame_ids[0], batch_size)
        except Exception:
            # 异常容错: 返回零 latent
            pred_latents = torch.zeros(batch_size, 4, 32, 32, ...)
            idx_list = [frame_ids[0] + i for i in range(batch_size)]

        # 3. 中断检查
        if _interrupted.is_set():
            continue

        # 4. 放入 _unet_queue（整个 batch 作为一个 UNetQueueItem）
        _unet_queue.put(UNetQueueItem(
            pred_latents=pred_latents,
            speech_id=batch_speech_id,
            end_of_speech=batch_end_of_speech,
            audio_data=batch_audio,
            valid_num=valid_num,
            idx_list=idx_list,
            timestamp=time.time(),
        ))
```

#### 2.4.12 VAE Worker (_frame_generator_vae_worker)

```python
def _frame_generator_vae_worker(self):
    # CUDA 预热: dummy_latents[batch_size, 4, 32, 32] → generate_frames_vae()

    while not _stop_event.is_set():
        if _interrupted.is_set():
            time.sleep(0.01)
            continue

        # 1. 从 _unet_queue 取数据 (timeout=1s)
        item: UNetQueueItem = _unet_queue.get(timeout=1)
        if _interrupted.is_set():
            continue

        # 2. VAE 解码 (GPU, 通过 _inference_lock)
        try:
            recon_idx_list = _avatar.generate_frames_vae(
                item.pred_latents, item.idx_list, cur_batch)
        except Exception:
            recon_idx_list = [(zeros(256,256,3), idx) for ...]

        if _interrupted.is_set():
            continue

        # 3. 拆分 batch 为单帧，逐帧放入 _compose_queue
        for i in range(item.valid_num):  # 只处理有效帧，跳过 padding
            if _interrupted.is_set():
                break
            _compose_queue.put(ComposeQueueItem(
                recon=recon, idx=idx,
                speech_id=item.speech_id[i],
                end_of_speech=item.end_of_speech[i],
                audio_segment=item.audio_data[i],
            ))
```

VAE Worker 只处理 `valid_num` 个有效帧，跳过 padding 帧。

#### 2.4.13 Frame Generator Worker (single-thread mode)

```python
def _frame_generator_worker(self):
    # CUDA 预热: dummy_whisper → generate_frames() (UNet+VAE 一体)

    while not _stop_event.is_set():
        result = _collect_batch()
        if result is None:
            continue

        # UNet + VAE 一体推理
        recon_idx_list = _avatar.generate_frames(whisper_batch, frame_ids[0], batch_size)

        if _interrupted.is_set():
            continue

        # 逐帧放入 _compose_queue（只处理 valid_num 个）
        for i in range(valid_num):
            ...
```

#### 2.4.14 Compose Worker (_compose_worker)

```python
def _compose_worker(self):
    while not _stop_event.is_set():
        # 从 _compose_queue 取数据 (timeout=0.1s，较短，保持响应)
        item: ComposeQueueItem = _compose_queue.get(timeout=0.1)

        if _interrupted.is_set():
            continue

        # CPU 操作: res2combined（不需要 _inference_lock）
        frame = _avatar.res2combined(item.recon, item.idx)
        item.frame = frame

        # 放入 _output_queue
        _output_queue.put(item)
```

---

#### 2.4.15 Frame Collector Worker (_frame_collector_worker)

Frame Collector 是帧率的唯一控制点，也是输出节拍器。

```python
def _frame_collector_worker(self):
    fps = config.fps
    frame_interval = 1.0 / fps
    start_time = time.perf_counter()
    local_frame_id = 0
    max_frame_id_buffer = batch_size * 3

    while not _stop_event.is_set():
        # ── 1. 精确定时 ──
        target_time = start_time + local_frame_id * frame_interval
        now = time.perf_counter()
        sleep_time = target_time - now
        if sleep_time > 0.002:
            time.sleep(sleep_time - 0.001)  # 粗等待（留 1ms 余量）
        while time.perf_counter() < target_time:
            pass  # 自旋精确等待

        # ── 2. 分配 frame_id（背压控制）──
        if not _interrupted.is_set() and _frame_id_queue.qsize() < max_frame_id_buffer:
            _frame_id_queue.put(local_frame_id)

        # ── 3. 尝试获取说话帧 ──
        output_item = _output_queue.get_nowait()  # 非阻塞
        if output_item is not None and _interrupted.is_set():
            output_item = None  # 中断时丢弃

        # ── 4. 决定输出内容 ──
        if output_item is not None:
            # 说话帧: 使用推理生成的帧 + 对应音频
            frame = output_item.frame
            audio_segment = output_item.audio_segment
        else:
            # 空闲帧: 使用原始循环帧（无音频）
            frame = _avatar.generate_idle_frame(local_frame_id)
            audio_segment = None

        # ── 5. 输出 ──
        _notify_video(frame)                         # 每帧都输出视频
        if audio_segment is not None and len > 0:
            _notify_audio(audio_segment)             # 仅说话帧输出音频
        if end_of_speech:
            _notify_speech_end(speech_id)            # 语音结束信号

        # ── 6. 帧计数 ──
        local_frame_id += 1
```

**定时策略**:
- 使用 `time.perf_counter()` 基于绝对时间（`start_time + frame_id * interval`），避免累积漂移
- 粗等待 `time.sleep()` + 精等待自旋 `while perf_counter() < target`，平衡 CPU 使用和精度
- `sleep_time - 0.001` 提前 1ms 唤醒，剩余时间靠自旋补偿系统调度延迟

**frame_id 分配**:
- `_frame_id_queue.qsize() < max_frame_id_buffer`（默认 `batch_size * 3`）时才分配
- 推理线程必须先获得 frame_id 才能开始处理，形成自然背压
- 中断时不分配 frame_id，推理线程在 `_collect_batch()` 中等待 frame_id 时检测到中断会返回 None

**idle 帧与说话帧切换日志**:
- 如果上一帧是 speaking 且当前是 idle:
  - `last_end_of_speech=True`: 正常过渡（"Start after speaking"）
  - `last_end_of_speech=False`: 异常！推理速度不够快（WARNING: "Inserted idle during speaking"）

---

#### 2.4.16 Worker 中断响应点汇总

| Worker | 中断检查点 | 行为 |
|--------|-----------|------|
| Feature Extractor | 取到 AudioQueueItem 后检查 `generation_id` | 不匹配 → `continue` 丢弃 |
| Feature Extractor | Whisper 提取完毕后 | `_interrupted.is_set()` → 丢弃整个结果 |
| Feature Extractor | 逐帧入队前 | `_interrupted.is_set()` → `break` 停止拆分 |
| _collect_batch() | 外层循环开头 | `_interrupted.is_set()` → 清空 partial batch, sleep |
| _collect_batch() | 取到 WhisperQueueItem 后 | `_interrupted.is_set()` → 清空 batch |
| _collect_batch() | 等待 frame_id 时 | `_interrupted.is_set()` → `return None` |
| UNet Worker | 推理完成后 | `_interrupted.is_set()` → `continue` 不入队 |
| VAE Worker | 循环开头 | `_interrupted.is_set()` → sleep |
| VAE Worker | 取到 UNetQueueItem 后 | `_interrupted.is_set()` → `continue` |
| VAE Worker | 解码完成后 | `_interrupted.is_set()` → `continue` |
| VAE Worker | 逐帧入队时 | `_interrupted.is_set()` → `break` |
| Compose Worker | 取到 ComposeQueueItem 后 | `_interrupted.is_set()` → `continue` |
| Frame Collector | frame_id 分配条件 | `_interrupted.is_set()` → 不分配 |
| Frame Collector | 取到 output_item 后 | `_interrupted.is_set()` → 置为 None（输出 idle 帧） |

#### 2.4.17 CUDA 预热

各 Worker 在进入主循环前各自执行一次 dummy 推理预热：

| Worker | 预热内容 | 目的 |
|--------|---------|------|
| Feature Extractor | 1秒静音 → `extract_whisper_feature()` | Whisper GPU 预热 |
| UNet Worker | zeros[B,50,384] → `generate_frames_unet()` | UNet GPU 预热 |
| VAE Worker | zeros[B,4,32,32] → `generate_frames_vae()` | VAE GPU 预热 |
| Frame Generator | zeros[B,50,384] → `generate_frames()` | UNet+VAE GPU 预热 |

预热确保 CUDA context 和显存已分配，避免首帧延迟。每个 Worker 在**自己的线程**中预热，确保 CUDA 上下文绑定到正确的线程。

---

### 2.5 MuseTalkAlgoV15

**文件**: `musetalk_algo.py`

封装所有 GPU 模型操作的算法类。**全局唯一实例**，被所有 Processor 共享。

#### 2.5.1 构造函数参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `avatar_id` | str | Avatar 唯一标识 |
| `video_path` | str | 数字人形象视频路径 |
| `bbox_shift` | int | 人脸 bbox 偏移量 |
| `batch_size` | int | 批量推理大小 |
| `force_preparation` | bool | 是否强制重新生成数据 |
| `parsing_mode` | str | 人脸解析模式，默认 'jaw' |
| `left_cheek_width` | int | 左脸颊宽度（用于 FaceParsing V15） |
| `right_cheek_width` | int | 右脸颊宽度 |
| `audio_padding_length_left` | int | 音频左 padding 长度 |
| `audio_padding_length_right` | int | 音频右 padding 长度 |
| `fps` | int | 视频帧率 |
| `version` | str | "v15" 或 "v1" |
| `result_dir` | str | Avatar 数据缓存根目录 |
| `extra_margin` | int | 人脸裁剪额外边距（V15 下方扩展） |
| `vae_type` | str | VAE 模型类型 |
| `unet_model_path` | str | UNet 权重路径 |
| `unet_config` | str | UNet 配置文件路径 |
| `whisper_dir` | str | Whisper 模型目录 |
| `gpu_id` | int | GPU 设备 ID |
| `debug` | bool | 是否开启详细日志 |

#### 2.5.2 初始化流程（`init()`）

```
1. 检查 avatar 目录完整性
   ├── 所有文件存在 + bbox_shift 未变 → 直接加载
   └── 文件缺失 / bbox_shift 变化 / force_preparation → 重新生成

2. 加载 GPU 模型
   ├── VAE (sd-vae)                → half precision → device
   ├── UNet (musetalkV15)          → half precision → device
   ├── PE (Positional Encoder)     → half precision → device
   ├── AudioProcessor              → feature_extractor (Whisper preprocessing)
   ├── Whisper (HuggingFace)       → half precision → device, eval(), no_grad
   └── FaceParsing                 → jaw 模式 (left/right_cheek_width=90)

3. 准备或加载 Avatar 数据
   ├── need_preparation=True → 删除旧目录 → prepare_material()
   └── need_preparation=False → 加载缓存:
       ├── latents.pt (torch.load)
       ├── coords.pkl (pickle)
       ├── frames.pkl (pickle)
       ├── mask_coords.pkl (pickle)
       └── masks.pkl (pickle)
```

`init()` 结尾不做预热，改为每个 Worker 线程在启动时自行预热，确保 CUDA 上下文在正确线程中初始化。

#### 2.5.3 Avatar 数据准备（`prepare_material()`）

首次使用某个视频时执行，耗时较长。执行期间会临时覆盖 `builtins.input` 以跳过 MuseTalk 内部的交互提示，完成后自动恢复：

```python
def prepare_material(self):
    builtins.input = lambda prompt='': "y"
    try:
        self._prepare_material_impl()
    finally:
        builtins.input = _original_input
```

`_prepare_material_impl()` 的步骤：

```
Step 1: 保存 avatar 基本配置信息 (avator_info.json)
Step 2: 处理输入源
   ├── 视频文件 → video2imgs() 抽帧 → full_imgs/
   └── 图片目录 → 直接复制 png 文件
Step 3: 人脸关键点 + bbox 提取
   └── get_landmark_and_bbox() (DWPose ONNX + S3FD)
Step 4: VAE latent 特征提取
   ├── 对每帧: crop face → resize 256×256 → vae.get_latents_for_unet()
   └── V15 额外处理: y2 += extra_margin (扩展下巴区域)
Step 5: 构建正序+倒序循环序列 (pingpong)
   ├── frame_list_cycle = frames + frames[::-1]
   ├── coord_list_cycle = coords + coords[::-1]
   └── input_latent_list_cycle = latents + latents[::-1]
Step 6: 生成人脸掩膜 (FaceParsing)
   ├── V15: 使用 parsing_mode (jaw)
   ├── V1: 使用 raw 模式
   └── 每帧: get_image_prepare_material() → mask + crop_box
Step 7: 保存所有数据
   ├── mask_coords.pkl, coords.pkl → pickle
   ├── latents.pt → torch.save
   └── frames.pkl, masks.pkl → pickle
```

**Pingpong 循环序列**: 正序帧 + 倒序帧组成一个完整循环，使空闲帧在两端平滑过渡（避免跳变）。

#### 2.5.4 核心推理方法

| 方法 | 签名 | 说明 | 线程安全 |
|------|------|------|----------|
| `extract_whisper_feature()` | `(segment: ndarray, sr: int) → Tensor[N,50,384]` | 音频 → Whisper 特征 | 是（`_inference_lock`） |
| `generate_frame()` | `(whisper_chunk: Tensor, idx: int) → ndarray` | 单帧全流程: Whisper→UNet+VAE+res2combined | 是（`_inference_lock`） |
| `generate_frames()` | `(chunks: Tensor[B,50,384], start_idx, bs) → List[(ndarray, int)]` | 批量 UNet+VAE → 人脸裁剪列表 | 是（`_inference_lock`） |
| `generate_frames_unet()` | `(chunks: Tensor[B,50,384], start_idx, bs) → (Tensor[B,4,32,32], List[int])` | 仅 UNet 阶段 | 是（`_inference_lock`） |
| `generate_frames_vae()` | `(latents: Tensor[B,4,32,32], idx_list, bs) → List[(ndarray, int)]` | 仅 VAE 阶段 | 是（`_inference_lock`） |
| `res2combined()` | `(res_frame: ndarray, idx: int) → ndarray` | 人脸裁剪→合成全帧 (CPU, in-place blending) | 否（使用 .copy()） |
| `generate_idle_frame()` | `(idx: int) → ndarray` | 返回循环帧副本（无推理） | 否（.copy()） |

所有 GPU 操作通过 `_inference_lock`（`threading.Lock`）串行化，确保多 Processor 并发时不会产生 CUDA 冲突。

#### 2.5.5 推理管线数据流

```
音频 (float32, 16kHz)
    │
    ▼  extract_whisper_feature()
    │   AudioProcessor.feature_extractor() → input_features
    │   AudioProcessor.get_whisper_chunk() → whisper_chunks
    │
Whisper 特征 [B, 50, 384]
    │
    ▼  generate_frames() / generate_frames_unet()
    │   ├── PE 编码: whisper → audio_feature
    │   ├── 取循环 latent: input_latent_list_cycle[idx % len]
    │   ├── UNet 推理: (latent + audio_feature) → pred_latents [B, 4, 32, 32]
    │   │     unet.model(latent, timesteps=[0], encoder_hidden_states=audio_feature)
    │   └── [generate_frames only] VAE 解码: pred_latents → recon [B, 256, 256, 3]
    │
    ▼  generate_frames_vae() (仅 multi_thread_inference 模式)
    │   pred_latents → vae.decode_latents() → recon [B, 256, 256, 3]
    │
    ▼  res2combined()
    │   ├── .copy() 原始帧 (frame_list_cycle[idx % len])
    │   ├── resize 推理帧到 bbox 大小
    │   ├── 全零帧检测 → 直接返回原始帧
    │   ├── acc_get_image_blending (in-place alpha blending):
    │   │     mask_f[:,:,newaxis] broadcast → blended = face * mask + body * (1 - mask)
    │   └── 直接写回 ori_frame
    │
    ▼
完整帧 [H, W, 3] (BGR, uint8)
```

#### 2.5.6 acc_get_image_blending() 详细逻辑

这是 `res2combined()` 使用的核心混合函数。**调用者必须传入原始帧的 `.copy()`**，因为该方法直接修改 `image` 以避免额外的全帧内存分配：

```python
def acc_get_image_blending(self, image, face, face_box, mask_array, crop_box):
    x, y, x1, y1 = face_box        # 人脸 bbox
    x_s, y_s, x_e, y_e = crop_box  # 掩膜裁剪框（通常比 face_box 大）

    # 1. 从原图裁剪大区域（两份 copy：一份贴人脸，一份保留原始用于混合）
    body_crop = image[y_s:y_e, x_s:x_e].copy()
    face_large = body_crop.copy()

    # 2. 将推理人脸贴入 face_large
    face_large[y-y_s:y1-y_s, x-x_s:x1-x_s] = face

    # 3. 构造 float mask（使用 broadcasting 而非 stack，减少内存分配）
    mask_f = mask_array.astype(float32) * (1.0 / 255.0)
    mask_f = mask_f[:, :, np.newaxis]  # (H, W, 1) — broadcasts to 3-ch

    # 4. 尺寸对齐（容错）
    if face_large.shape[:2] != mask_f.shape[:2]:
        min_h, min_w = ...
        face_large, body_crop, mask_f = truncate_to_min(...)

    # 5. Alpha blending
    blended = (face_large * mask_f + body_crop * (1.0 - mask_f)).astype(uint8)

    # 6. 直接写回原图（in-place，无额外全帧拷贝）
    image[y_s:y_e, x_s:x_e] = blended
    return image
```

**性能优化要点**：
- `mask_f[:, :, np.newaxis]` 利用 numpy broadcasting 自动扩展到 3 通道，避免 `np.stack([mask_f]*3)` 的额外分配
- In-place 写回 `image` 而非 `out = image.copy()`，减少一次全帧拷贝
- 调用方 `res2combined()` 中使用 `ori_frame.copy()` 代替 `copy.deepcopy()`，对 numpy 数组同样是全量拷贝但开销更低

#### 2.5.7 错误容错

- `generate_frames()`: `B != batch_size` 时返回 zeros(256,256,3) 列表
- `generate_frames_unet()`: `B != batch_size` 时返回 zeros latent
- `generate_frames_vae()`: `B != batch_size` 时返回 zeros 列表
- `res2combined()`: resize 异常时返回原始帧
- `res2combined()`: 全零推理帧时返回原始帧（避免黑脸）

#### 2.5.8 音频特征提取：实时 vs 离线

MuseTalkAlgoV15 提供两条音频特征提取路径，分别服务于实时推理和离线合成。

**实时路径: `extract_whisper_feature()`**

每次处理 1 秒音频段，用于 `musetalk_processor.py` 的 Feature Extractor Worker：

```
输入: audio_segment (1s, 16kHz float32)
    │
    ▼
feature_extractor(segment) → mel spectrogram [1, 80, 3000]
    │
    ▼
whisper.encoder(mel, output_hidden_states=True)
    │  → hidden_states: 多层特征
    │  → torch.stack → [1, T, layers, 384]
    ▼
get_whisper_chunk(): 按 fps 切分为每帧一段
    │  每帧取 audio_padding_length_left + 1 + audio_padding_length_right 个窗口
    │  → rearrange → [num_frames, 50, 384]
    ▼
输出: whisper_chunks [num_frames, 50, 384]
```

特点：每段独立 padding，段边界处可能有不连续；受 `_inference_lock` 保护，支持多会话 GPU 共享。

**离线路径: `audio_processor.get_audio_feature()` + `get_whisper_chunk()`**

用于 `offline_inference()` 处理完整音频文件：

```
输入: audio_path (WAV/MP3 文件)
    │
    ▼
librosa.load(path, sr=16000) → 完整音频
    │
    ▼
按 30s 分段提取 mel features（仅因 Whisper 输入长度限制）
    │
    ▼
whisper.encoder() → 拼接所有段的 hidden_states → trim 到实际音频长度
    │
    ▼
get_whisper_chunk(): 为整段音频一次性生成所有帧的 whisper 特征
    │  → 首尾 padding，按 fps 切分
    ▼
输出: whisper_chunks [total_frames, 50, 384]
```

特点：完整音频上下文，无段间边界效应；30s 分段仅用于 mel 提取（Whisper 输入长度限制），最终特征是连续拼接的。

**差异对照**

| 维度 | 实时 (`extract_whisper_feature`) | 离线 (`get_audio_feature` + `get_whisper_chunk`) |
|------|----------------------------------|--------------------------------------------------|
| 输入粒度 | 1 秒段 | 完整音频文件 |
| Whisper 上下文 | 每段独立 | 全局连续（30s 分段仅因 mel 限制） |
| 段间 padding | 每段独立 zero-pad 到 1s | 仅首尾 padding |
| 帧级特征连续性 | 段边界处可能不连续 | 全局连续 |

#### 2.5.9 VAE Latent 准备细节

`prepare_material()` 中，`vae.get_latents_for_unet()` 内部流程：

```python
ref_image_masked = preprocess(img, half_mask=True)   # 上半脸遮盖
masked_latents = vae.encode(ref_image_masked)         # [1, 4, 32, 32]
ref_image_full = preprocess(img, half_mask=False)     # 完整脸
ref_latents = vae.encode(ref_image_full)              # [1, 4, 32, 32]
latent_input = cat([masked_latents, ref_latents])     # [1, 8, 32, 32]
```

上半脸遮盖的设计意图：模型学习根据音频条件"补全"下半脸的说话动作。

#### 2.5.10 离线合成 (`offline_inference`)

离线合成使用**与实时推理完全相同的推理和帧合成路径**，差异仅在音频特征提取（全局 Whisper vs 逐段 Whisper）：

```
完整音频文件
    │
    ▼
audio_processor.get_audio_feature() → whisper mel features (30s 分段)
    │
    ▼
audio_processor.get_whisper_chunk() → 全量 per-frame features [N, 50, 384]
    │
    ▼
batch loop: generate_frames(whisper_batch, batch_start, batch_size) → [(recon, idx), ...]
    │  （UNet + VAE，与实时完全相同的 generate_frames() 方法）
    │  不满 batch_size 时零 padding（与实时 _collect_batch 逻辑一致）
    ▼
per frame: res2combined(recon, idx)
    │  → acc_get_image_blending (预计算 mask, blur=0.1)
    │  （与实时完全相同的帧合成路径）
    ▼
ffmpeg: 帧序列 + 音频 → MP4
```

**离线 vs 实时差异对照表**

| 环节 | 离线 (`offline_inference`) | 实时 (`musetalk_processor`) |
|------|--------------------------|----------------------------|
| 音频输入 | 完整文件 (16kHz) | 1s 流式段 (24kHz → resample → 16kHz) |
| Whisper 上下文 | 全局连续（全音频一次性提取特征） | 每段独立（1s 段间无上下文共享） |
| Batch 处理 | 按 batch_size 分组 + 零 padding | `_collect_batch()` 收集 + 零 padding |
| 推理 (UNet+VAE) | `generate_frames()` ✓ 相同 | `generate_frames()` ✓ 相同 |
| 帧合成 | `res2combined()` ✓ 相同 | `res2combined()` ✓ 相同 |
| 输出 | ffmpeg → MP4 文件 | 实时帧流 → 回调 |

**离线测试 CLI**

`musetalk_algo.py` 的 `__main__` 入口直接复用实时推理的 YAML 配置文件，自动从中读取 `AvatarMusetalk` handler 配置段，保证离线测试使用与线上完全一致的 avatar 参数。

| 参数 | 说明 | 来源 |
|------|------|------|
| `--config` | YAML 配置文件路径 | **必选** — 与实时推理相同的配置文件 |
| `--audio_path` | 单个音频文件 | 二选一 |
| `--audio_dir` | 音频文件目录（批量合成） | 二选一 |
| `--output_dir` | 输出目录 | 可选（默认使用 avatar 输出目录） |
| `--batch_size` | 覆盖配置中的 batch_size | 可选（离线建议设大，如 20） |
| `--gpu_id` | GPU 设备号 | 可选（默认 0） |
| `--force_preparation` | 强制重新生成 avatar 数据 | 可选（flag） |

```bash
# 单个音频文件合成
python src/handlers/avatar/musetalk/musetalk_algo.py \
    --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \
    --audio_path tests/inttest/musetalk/assets/audio/test-audio-1.wav \
    --output_dir tests/inttest/musetalk/outputs/offline

# 批量合成
python src/handlers/avatar/musetalk/musetalk_algo.py \
    --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \
    --audio_dir tests/inttest/musetalk/assets/audio/ \
    --output_dir tests/inttest/musetalk/outputs/offline

# 覆盖 batch_size 加速离线处理
python src/handlers/avatar/musetalk/musetalk_algo.py \
    --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \
    --audio_path tests/inttest/musetalk/assets/audio/test-audio-1.wav \
    --output_dir tests/inttest/musetalk/outputs/offline \
    --batch_size 20
```

---

### 2.6 AvatarMuseTalkConfig

**文件**: `musetalk_config.py`

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|------|------|--------|------|------|
| `fps` | int | 25 | 自动校正为 `output_audio_sample_rate` 的因子 | 输出视频帧率 |
| `batch_size` | int | 5 | ≥2（field_validator 强制） | 批量推理大小。越大 GPU 利用率越高但延迟越大 |
| `avatar_video_path` | str | "" | - | 数字人形象视频路径 |
| `avatar_model_dir` | str | "models/musetalk/avatar_model" | - | Avatar 预处理数据缓存目录 |
| `force_create_avatar` | bool | false | - | 是否强制重新生成 Avatar 数据 |
| `debug` | bool | false | - | 开启详细日志（每帧日志、性能分析） |
| `algo_audio_sample_rate` | int | 16000 | 固定 | 算法内部采样率（Whisper 需要 16kHz） |
| `output_audio_sample_rate` | int | 24000 | - | 输出音频采样率，需与上游 TTS 匹配 |
| `model_dir` | str | "models/musetalk" | - | 模型文件根目录 |
| `multi_thread_inference` | bool | true | - | 将 UNet 和 VAE 拆分到独立线程进行流水线推理 |
| `concurrent_limit` | int | 2 | 继承自 HandlerBaseConfigModel | 最大并发会话数，决定 Pool 大小 |

#### 2.6.1 Pydantic Validators

**`@field_validator("batch_size")`**: 强制 `batch_size >= 2`，否则抛出 `ValueError`。UNet/VAE 推理的 padding 逻辑要求至少 2 个元素。

**`@model_validator("after") _align_fps_to_sample_rate()`**: 自动校正 `fps` 使 `output_audio_sample_rate % fps == 0`。Processor 使用整数除法 `samples_per_frame = sample_rate // fps` 拆分每帧音频，如果有余数则每秒丢失采样点导致音视频漂移。校正策略是搜索距离原始 fps 最近的 `output_audio_sample_rate` 因子，并以 WARNING 级别日志通知用户。

```
配置 fps=27, output_audio_sample_rate=24000
    → 24000 % 27 != 0
    → 搜索最近因子: 25 (24000 / 25 = 960)
    → 自动校正 fps: 27 → 25
    → WARNING: [FPS AUTO-CORRECTION] fps 27 -> 25
```

---

### 2.7 数据模型

**文件**: `musetalk_data_models.py`

#### 2.7.1 状态枚举

```python
class MuseTalkAvatarStatus(Enum):
    SPEAKING = 0    # 说话中（输出推理帧 + 音频）
    LISTENING = 1   # 空闲中（输出 idle 帧，无音频）
```

#### 2.7.2 外部接口模型

| 类 | 类型 | 用途 |
|----|------|------|
| `MuseTalkSpeechAudio` | Pydantic BaseModel | Handler → Processor 的音频输入 |
| `MuseTalkProcessorCallbacks` | dataclass | Processor → Context 的回调接口 |

**MuseTalkSpeechAudio 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `speech_id` | Any | 语音标识，默认 "" |
| `end_of_speech` | bool | 是否为该语音的最后一段 |
| `sample_rate` | int | 采样率，默认 16000 |
| `audio_data` | Any | 音频数据（bytes 或 np.ndarray） |

`get_audio_duration()` 方法根据数据类型计算时长:
- bytes: `len / sample_rate / 4`（float32 = 4 bytes）
- ndarray: `len / sample_rate`

**MuseTalkProcessorCallbacks 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `on_video_frame` | Callable[[ndarray], None] | 视频帧回调 |
| `on_audio_frame` | Callable[[ndarray], None] | 音频帧回调 |
| `on_speech_end` | Callable[[str], None] | 语音结束回调 |

#### 2.7.3 Pipeline 内部队列项

| 类 | 装饰器 | 队列 | 生产者 → 消费者 |
|----|--------|------|------------------|
| `AudioQueueItem` | `@dataclass(slots=True)` | `_audio_queue` | `add_audio()` → Feature Extractor |
| `WhisperQueueItem` | `@dataclass(slots=True)` | `_whisper_queue` | Feature Extractor → UNet/FrameGen Worker |
| `UNetQueueItem` | `@dataclass(slots=True)` | `_unet_queue` | UNet Worker → VAE Worker |
| `ComposeQueueItem` | `@dataclass(slots=True)` | `_compose_queue` / `_output_queue` | VAE/FrameGen → Compose → Collector |

**AudioQueueItem 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `audio_data` | ndarray float32 | 原始音频数据（output_sample_rate） |
| `speech_id` | Any | 语音标识 |
| `end_of_speech` | bool | 是否为最后一段 |
| `generation_id` | int | 代际 ID（用于过时数据检测） |

**WhisperQueueItem 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `whisper_chunks` | Tensor [1,50,384] | 单帧 Whisper 特征 |
| `speech_id` | Any | 语音标识 |
| `end_of_speech` | bool | 是否为该语音的最后一帧 |
| `audio_data` | ndarray | 该帧对应的原始音频段 |

**UNetQueueItem 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `pred_latents` | Tensor [B,4,32,32] | UNet 输出的 latent |
| `speech_id` | List[str] | 每帧的语音标识 |
| `avatar_status` | MuseTalkAvatarStatus | 始终为 SPEAKING |
| `end_of_speech` | List[bool] | 每帧的结束标志 |
| `audio_data` | List[ndarray] | 每帧对应的音频段 |
| `valid_num` | int | 有效帧数（batch 中非 padding 的部分） |
| `idx_list` | List[int] | 帧索引列表 |
| `timestamp` | float | 创建时间戳 |

**ComposeQueueItem 字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `recon` | ndarray [256,256,3] | VAE 重建的人脸裁剪 |
| `idx` | int | 循环序列索引 |
| `speech_id` | Any | 语音标识 |
| `avatar_status` | MuseTalkAvatarStatus | 状态（SPEAKING/LISTENING） |
| `end_of_speech` | bool | 是否为最后一帧 |
| `audio_segment` | ndarray | 对应音频段 |
| `frame_id` | int | 输出帧号 |
| `timestamp` | float | 创建时间戳 |
| `frame` | ndarray | **合成后的完整帧**（由 Compose Worker 填充） |

---

## 3. 数据流全景

```
上游 TTS (AVATAR_AUDIO, 24kHz, float32, shape=[1, N])
    │
    ▼
HandlerAvatarMuseTalk.handle()
    │  1. stream_key 变化检测 → CLIENT_PLAYBACK 流管理
    │  2. 输入验证（采样率、dtype、非空）
    │  3. 音频切片（SliceContext，每段 output_audio_sample_rate samples = 1秒）
    │     每段 → MuseTalkSpeechAudio.audio_data = bytes
    │  4. speech_end → flush 切片器 + end_of_speech=True
    │
    ▼
AvatarMuseTalkProcessor.add_audio()
    │  数据验证 → generation_id 打标 → AudioQueueItem 入队 → 条件 clear _interrupted
    │
    ▼  ────── Processor 内部 Pipeline ──────
    │
    │  Thread 1: Feature Extractor
    │    ├── generation_id 校验（丢弃过时数据）
    │    ├── librosa 重采样 24kHz → 16kHz
    │    ├── 零填充到 1 秒 (16000 samples)
    │    ├── Whisper 特征提取 → [num_frames, 50, 384]
    │    ├── 帧对齐: num_frames = ceil(audio_len / (24000/fps))
    │    ├── 音频对齐: padding/truncate 到 num_frames * (24000/fps)
    │    └── 按帧拆分 → 逐帧 WhisperQueueItem
    │         (end_of_speech 仅标记最后一帧)
    │
    │  Thread 2/2+3: Frame Generator (UNet [+VAE])
    │    ├── _collect_batch(): 收集 batch_size 个 chunk
    │    │   ├── 不足时零 padding
    │    │   ├── end_of_speech 时提前提交
    │    │   ├── _output_queue 背压 (qsize > batch_size*5 → wait)
    │    │   └── 等待 frame_id (背压: Frame Collector 控速)
    │    ├── UNet 推理 → pred_latents [B, 4, 32, 32]
    │    └── [multi_thread] → UNetQueueItem 入 _unet_queue
    │        [single_thread] → VAE 解码 + 逐帧 ComposeQueueItem
    │
    │  Thread 3 (multi_thread only): VAE Worker
    │    ├── VAE 解码 → recon [B, 256, 256, 3]
    │    └── 拆分 batch → 逐帧 ComposeQueueItem (仅 valid_num 个)
    │
    │  Thread 4: Compose Worker
    │    └── res2combined() → 完整帧 → _output_queue
    │
    │  Thread 5: Frame Collector
    │    ├── 精确按 fps 定时 (perf_counter + sleep + spin)
    │    ├── 分配 frame_id → _frame_id_queue (背压)
    │    ├── 非阻塞取 _output_queue:
    │    │   ├── 有帧 → callback(video + audio)
    │    │   └── 无帧 → callback(idle video, no audio)
    │    └── end_of_speech → callback(speech_end)
    │
    ▼  ────── Processor 输出回调 ──────
    │
AvatarMuseTalkContext callbacks
    │  on_video_frame:
    │    [H,W,3] → [1,H,W,3] → DataBundle → submit_data(AVATAR_VIDEO)
    │
    │  on_audio_frame:
    │    [1,N] float32 → DataBundle → submit_data(AVATAR_AUDIO)
    │
    │  on_speech_end:
    │    speech_id 校验 → _current_tts_stream_key=None
    │    → streamer.finish_current() → 关闭 CLIENT_PLAYBACK
    │
    ▼
下游 RtcClient → WebRTC → 浏览器
```

---

## 4. 多会话与线程安全

### 4.1 并发模型

```
                   ┌─────────────────────────┐
                   │   MuseTalkAlgoV15        │  唯一实例
                   │   (GPU 模型 + 数据)       │
                   │   _inference_lock 🔒      │
                   └──────────┬──────────────┘
                              │ 共享
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────┴──────┐ ┌─────┴──────┐ ┌──────┴─────────┐
    │ Processor #0    │ │ Processor #1│ │ Processor #N-1 │
    │ (4~5 threads)   │ │ (4~5 thds) │ │ (idle)         │
    │ Session A       │ │ Session B   │ │                │
    └────────────────┘ └────────────┘ └────────────────┘
```

- GPU 操作通过 `_inference_lock` 串行化
- 每个 Processor 拥有独立的队列和 Worker 线程
- CPU 操作（`res2combined()`、帧收集）可以真正并行
- Pool 通过 `_lock` 保护 acquire/release 的线程安全

### 4.2 锁清单与用途

| 锁 | 所在类 | 保护对象 | 类型 |
|----|--------|---------|------|
| `_inference_lock` | MuseTalkAlgoV15 | 所有 GPU 操作 | threading.Lock |
| `_lock` | MuseTalkProcessorPool | acquire/release | threading.Lock |
| `_generation_lock` | AvatarMuseTalkProcessor | `_generation_id` | threading.Lock |
| `_frame_id_lock` | AvatarMuseTalkProcessor | 队列清空操作 | threading.Lock |
| `_stream_key_lock` | AvatarMuseTalkContext | `_current_tts_stream_key` | threading.Lock |

### 4.3 线程属性

Worker 线程**不设置** `daemon=True`，确保进程关闭时线程能被完整回收。`stop()` 方法通过 `join(timeout=5)` 优雅等待线程结束，超时未退出会 log `logger.error`。join 后重置线程引用为 `None`，允许下次 `start()` 干净启动。`demo.py` 的 `os._exit(0)` 作为最终兜底，防止残留线程阻塞进程退出。

---

## 5. 采样率与音视频同步

### 5.1 采样率链路

```
上游 TTS 输出: 24000 Hz (output_audio_sample_rate)
    │
    ▼  Handler 切片: 每段 24000 samples = 1秒
    │
    ▼  Feature Extractor: librosa 重采样 24000 → 16000 Hz
    │  Whisper 特征提取使用 16000 Hz
    │
    ▼  帧对齐: 每帧音频长度 = output_audio_sample_rate / fps
    │  例: 24000 / 20 = 1200 samples/帧
    │
    ▼  输出音频: 每帧 1200 samples @ 24000 Hz
```

### 5.2 音视频同步

Frame Collector 是唯一的输出节拍器：

1. 每个时钟周期（1/fps 秒）输出一帧视频
2. 同时输出对应的音频段（output_audio_sample_rate / fps samples）
3. 视频帧和音频帧**同步发送**，天然对齐

**重要约束**: `output_audio_sample_rate % fps` 必须为 0，否则会出现音视频漂移。`AvatarMuseTalkConfig` 的 `_align_fps_to_sample_rate` model_validator 会自动校正 fps 为最近因子，`create_context()` 中通过 `assert` 做防御性检查。

---

## 6. Avatar 数据缓存

### 6.1 缓存结构

```
models/musetalk/avatar_model/v15/avatars/{avatar_id}/
├── avator_info.json     # 配置元数据（avatar_id, video_path, bbox_shift, version）
├── latents.pt           # VAE latent 特征列表（torch 张量）
├── coords.pkl           # 人脸 bbox 坐标列表
├── frames.pkl           # 原始视频帧列表（numpy）
├── masks.pkl            # 人脸掩膜列表
├── mask_coords.pkl      # 掩膜裁剪坐标列表
├── full_imgs/           # 抽帧图片
└── mask/                # 掩膜图片
```

### 6.2 avatar_id 生成规则

`avatar_id` 由视频文件名 + 路径哈希自动生成：

```python
video_basename = os.path.splitext(os.path.basename(video_path))[0]
video_hash = hashlib.md5(video_path.encode()).hexdigest()[:8]
avatar_id = f"avatar_{video_basename}_{video_hash}"
```

例: `avatar_bg_video_silence_3aa6faa7`

### 6.3 缓存失效条件

以下情况会触发重新生成：
- `force_create_avatar: true`
- 缓存目录不存在
- 任何必需文件缺失（latents.pt, coords.pkl, mask_coords.pkl, avator_info.json, frames.pkl, masks.pkl）
- `bbox_shift` 配置变化（与 `avator_info.json` 中记录的值比较）

重新生成会先 `shutil.rmtree()` 删除整个缓存目录，再重新创建。

---

## 7. 调试功能

`debug: true` 开启后的额外日志：

### 7.1 Processor 层

- `add_audio()`: [始终] 累计音频时长 < 总间隔时报 WARNING（`[AUDIO_LAG]`，含 lag 数值）
- `add_audio()`: [debug] 每次接收音频的详细信息（speech_id、时长、累计时长、总间隔）
- `_feature_extractor_worker`: 每段处理完毕后的详细耗时（总时间、chunk数、原始/padding长度）
- `_collect_batch()`: output buffer 满时的等待日志
- `_frame_generator_*`: UNet/VAE/Full batch 耗时
- `_frame_collector_worker`:
  - 每个说话帧的详细状态（frame_id, speech_id, status, end_of_speech, timestamp）
  - 说话帧 START/END 标记
  - 帧超时 WARNING（处理时间超过帧间隔）

### 7.2 Algo 层

- `extract_whisper_feature()`: 提取耗时
- `generate_frames()`: 各阶段耗时（prep_whisper, prep_latent, pe, latent_to, unet, vae, total, fps）
- `generate_frames()`: latent/pred_latents/recon 的统计信息（min, max, mean, nan_count）
- `generate_frames_unet()`: UNet 各阶段耗时
- `generate_frames_vae()`: VAE 耗时
- `generate_frame()`: 每 1 秒输出平均 profile（单帧模式）
- `res2combined()`: 各步骤耗时（ori_copy, resize, mask_fetch, blend, total, fps）

### 7.3 非 debug 模式仍输出的日志

- 说话帧 START/END 状态变化
- idle 帧插入事件（区分正常过渡和异常中断）
- `res2combined()` fps 不足时的 WARNING
- 全零推理帧 WARNING
- 音频延迟检测（`[AUDIO_LAG]`）

---

## 8. 配置示例

```yaml
AvatarMusetalk:
  module: avatar/musetalk/avatar_handler_musetalk
  fps: 25                    # 会被自动校正为 output_audio_sample_rate 的因子
  batch_size: 2              # 低延迟场景建议 2，高吞吐场景可提高（必须 ≥2）
  avatar_video_path: "resource/avatar/liteavatar/20250408/sample_data/bg_video_silence.mp4"
  avatar_model_dir: "models/musetalk/avatar_model"
  force_create_avatar: false  # 首次使用新视频自动生成，之后加载缓存
  debug: false
  multi_thread_inference: true  # 将 UNet 和 VAE 拆分到独立线程，默认开启
  output_audio_sample_rate: 24000  # 需与上游 TTS 采样率一致
```

### 关键约束

1. **`output_audio_sample_rate % fps` 必须为 0**（`_align_fps_to_sample_rate` model_validator 自动校正，无需手动保证）
2. **`output_audio_sample_rate` 必须与上游 TTS 采样率一致**（默认 24000）
3. **`batch_size ≥ 2`**（`_check_batch_size` field_validator 强制，违反直接抛错）
4. **不依赖 mmcv/mmpose/mmdet/mmengine**（已由 ONNX Runtime 替代），减少包冲突和 CUDA 兼容性问题

---

## 9. 依赖模型

| 模型 | 路径 | 说明 |
|------|------|------|
| UNet | `models/musetalk/musetalkV15/unet.pth` | MuseTalk V1.5 扩散模型 |
| UNet Config | `models/musetalk/musetalkV15/musetalk.json` | UNet 架构配置 |
| VAE | `models/musetalk/sd-vae/` | Stable Diffusion VAE |
| Whisper | `models/musetalk/whisper/` | OpenAI Whisper 音频编码器 |
| DWPose | `models/musetalk/dwpose/dw-ll_ucoco_384.onnx` | 人脸关键点检测 ONNX 模型（懒加载，仅 prepare_material 时使用） |
| S3FD | `~/.cache/torch/hub/checkpoints/` | 人脸检测模型 |

下载命令：
```bash
uv run scripts/download_models.py --handler musetalk
```

### 9.1 DWPose ONNX 替换说明

DWPose（RTMPose-L wholebody-384x288）原先通过 mmpose + mmcv + mmdet + mmengine 加载 PyTorch 权重。由于 mmcv 停止维护且与新 CUDA 版本存在严重兼容性问题，已替换为直接使用 ONNX Runtime 推理同源导出的 ONNX 模型（`dw-ll_ucoco_384.onnx`，来自 HuggingFace `yzd-v/DWPose`）。

预处理流水线精确复刻 mmpose 行为：
- 全图作为 bbox（无检测器），padding=1.25
- 仿射变换到 (288, 384)
- BGR → RGB 颜色转换
- ImageNet 标准化（mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375]）
- SimCC 解码（split_ratio=2.0）

最终 keypoints 经 `astype(np.int32)` 取整，亚像素级浮点差异被完全吸收，确保与原 mmpose 输出一致。

### 9.2 DWPose ONNX Session 懒加载与 cuDNN 处理

```python
_dwpose_session = None  # 懒加载
_cudnn_preloaded = False

def _ensure_cudnn_available():
    """处理 pip 安装的 nvidia-cudnn-cu12 库路径问题。
    通过 ctypes 预加载 libcudnn*.so.9 并更新 LD_LIBRARY_PATH，
    确保 onnxruntime 的 CUDAExecutionProvider 能找到 cuDNN。"""

def _get_dwpose_session():
    """首次调用时初始化 ONNX Runtime session。
    优先使用 CUDAExecutionProvider，fallback 到 CPUExecutionProvider。"""
```

DWPose 和 S3FD 都采用懒加载策略，仅在 `prepare_material()` 首次调用时初始化，后续使用缓存数据时不会加载。

---

## 10. 进程关闭

```
Ctrl+C → uvicorn shutdown
    │
    ▼
OpenAvatarChatWebServer.shutdown()
    │
    ▼
ChatEngine.shutdown() → handler_manager.destroy()
    │
    ├── 各 Handler.destroy()
    │   └── HandlerAvatarMuseTalk.destroy()
    │       └── MuseTalkProcessorPool.destroy()
    │           └── 每个 Processor.stop()  # try/except 逐个容错
    │               ├── _stop_event.set()
    │               ├── join 所有线程 (timeout=5s)
    │               ├── _clear_queues()
    │               └── 重置线程引用 = None
    │
    ▼
uvicorn 关闭完成
    │
    ▼
demo.py finally 块
    ├── 重置信号处理器
    └── os._exit(0)  # 兜底强制退出，防止残留线程阻塞
```

Worker 线程不设置 `daemon=True`，`stop()` 通过 `join(timeout=5)` 等待退出。`os._exit(0)` 作为兜底保障，确保即使 join 超时进程也一定能退出。

---

## 11. 设计要点总结

### 11.1 线程安全设计

- `_current_tts_stream_key` 使用 `_stream_key_lock` 保护读写
- 所有 GPU 操作统一通过 `_inference_lock` 串行化，支持多会话安全共享
- `generation_id` 机制解决了 `add_audio()` / `interrupt()` 的竞态条件
- `_frame_id_lock` 保护队列清空操作，防止 `interrupt()` 与 `_clear_queues()` 并发冲突

### 11.2 背压控制

Pipeline 通过两级背压防止内存无限增长：
1. **_output_queue 背压**: 输出队列深度超过 `batch_size * 5` 时，`_collect_batch()` 暂停采集
2. **_frame_id_queue 背压**: Frame Collector 按实际帧率分配 frame_id，推理线程必须获取 frame_id 后才能开始处理

### 11.3 容错策略

- GPU 推理异常时返回全零帧/latent（不中断 Pipeline），可能产生短暂黑脸但不影响后续帧
- `add_audio()` 队列满时丢弃数据（timeout=1s）
- `create_context()` 中 try/except 确保 Processor 不泄漏
- `destroy_context()` 中先 stop 再 release，顺序严格
- `MuseTalkProcessorPool.destroy()` 逐个 try/except，不因单个 Processor 异常影响其他

### 11.4 帧率精度

- Frame Collector 使用绝对时间 (`start_time + frame_id * interval`)，避免累积漂移
- 粗等待 `time.sleep()` + 精等待自旋，平衡 CPU 使用和精度
- `AvatarMuseTalkConfig._align_fps_to_sample_rate()` 自动校正 fps 为采样率因子，消除音视频漂移风险
