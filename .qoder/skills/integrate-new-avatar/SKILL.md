---
name: integrate-new-avatar
description: Complete guide for integrating new avatar (digital human) handlers into OpenAvatarChat. Covers handler structure, audio-video synchronization via frame collector, RGB-to-BGR color conversion, idle animation with silent audio, dependency management, interrupt support, and lifecycle management. Use when creating new avatar handlers, debugging color issues, audio-video desync, idle animation problems, or dependency conflicts.
---

# 接入新数字人到 OpenAvatarChat

## 1. 数字人类型

| 类型 | 代表 | Client | 输出 |
|------|------|--------|------|
| 服务端渲染 | LiteAvatar, MuseTalk, FlashHead | `client/rtc_client` | `AVATAR_VIDEO` (BGR HxWx3) + `AVATAR_AUDIO` |
| 端侧渲染 | LAM (Gaussian Splatting) | `client/ws_lam_client` | `AVATAR_MOTION_DATA` (BlendShape 系数) |

## 2. 目录结构

```
src/handlers/avatar/<name>/
  __init__.py
  avatar_handler_<name>.py       # HandlerBase 子类（主入口）
  <name>_config.py               # Pydantic 配置模型
  <name>_processor.py            # 推理处理器（复杂逻辑建议拆分）
  pyproject.toml                 # Handler 专属依赖声明
  <AlgoRepo>/                    # git submodule（如有第三方算法）
```

第三方算法通过 git submodule 引入，在 `load()` 中加入 `sys.path`：

```python
algo_path = os.path.join(os.path.dirname(__file__), "<RepoName>")
if algo_path not in sys.path:
    sys.path.insert(0, algo_path)
```

## 3. Handler 实现要点

### 必须实现的方法

| 方法 | 说明 |
|------|------|
| `get_handler_info()` | 声明 handler_type（avatar）和 handler_name |
| `load()` | 加载模型权重、定义输出格式 |
| `create_context()` | 创建 per-session 上下文（processor 实例等） |
| `start_context()` | 启动处理线程（帧收集器、idle 推理） |
| `get_handler_detail()` | 声明输入/输出数据类型、信号过滤规则 |
| `handle()` | 处理 `AVATAR_AUDIO` 输入，驱动推理 |
| `on_signal()` | 响应 `STREAM_CANCEL` 打断信号 |
| `destroy_context()` | 清理上下文资源、停止线程 |

### 配置模型

```python
from chat_engine.data_models.chat_engine_config_data import HandlerBaseConfigModel

class NewAvatarConfig(HandlerBaseConfigModel, BaseModel):
    model_path: str = "models/<model_name>"
    fps: int = 25
    algo_audio_sample_rate: int = 16000
    output_audio_sample_rate: int = 24000
    # ... 其他算法特有参数
```

### 上下文

继承 `HandlerContext`，管理 per-session 状态：processor 实例、playback streamer、当前 stream key、打断方法。

## 4. 颜色空间：RGB → BGR

**fastrtc 假设输入为 BGR**（`tracks.py` 中 `VideoFrame.from_ndarray(array, format="bgr24")`）。

- LiteAvatar、MuseTalk 直接输出 BGR
- **如果模型输出 RGB**（如 FlashHead），必须转换：

```python
frame_bgr = frame_rgb[:, :, ::-1].copy()  # RGB → BGR, copy() 保证内存连续
```

**症状**：画面呈蓝紫色偏色 → 检查是否缺少 RGB→BGR 转换。

## 5. 音视频同步：帧收集器 + 配对队列

**禁止**音频直接透传 + 视频异步输出，这会导致音画不同步。

### 架构模式

```
TTS Audio ──► add_audio() ──► 推理 ──► FrameQueueItem(video, audio) ──► output_queue
                                                                              │
                                                           _frame_collector_worker (25 FPS 节拍器)
                                                                              │
                                                    on_video_frame / on_audio_frame / on_speech_end
```

### 关键要素

| 要素 | 说明 |
|------|------|
| **FrameQueueItem** | 视频帧 + 音频切片配对为原子单元 |
| **帧节拍器** | `_frame_collector_worker` 以绝对时间参考运行，防止累积漂移 |
| **音频切片** | `samples_per_frame = output_sr / fps`（如 24000/25 = 960），按帧切分原始 TTS 音频 |
| **精确计时** | `time.perf_counter()` 绝对时间 + 自旋等待实现亚毫秒精度 |
| **双缓冲** | 低采样率（如 16kHz）用于模型推理，原始采样率用于客户端回放，并行缓冲 |

### 计时模板

```python
start_time = time.perf_counter()
frame_id = 0
while not stop_event.is_set():
    target_time = start_time + frame_id * (1.0 / fps)
    now = time.perf_counter()
    if target_time - now > 0.002:
        time.sleep(target_time - now - 0.001)
    while time.perf_counter() < target_time:
        pass  # 自旋等待
    # ... 从队列取帧并输出 ...
    frame_id += 1
```

## 6. 空闲动画：空音频驱动

**禁止输出静态参考图**。TTS 静默时，必须用空音频（全零）驱动模型生成动态帧（呼吸、微动）。

- **idle 推理线程**：监控 output_queue，队列 < 一个 chunk 帧数且非说话状态时，喂全零音频
- **推理锁**：`_inference_lock` 串行化 speech 与 idle 推理，防止并发访问 pipeline
- **状态连续性**：idle 与 speech 共享 pipeline 状态（latent motion frames、audio buffer），保证过渡自然
- **静态帧兜底**：预计算一帧参考图作为 fallback（pipeline 未就绪时使用）

```python
need_idle = (
    output_queue.qsize() < slice_len      # 队列快空
    and not self._speaking                  # 非说话状态
    and not self._interrupted               # 非打断状态
)
```

## 7. 音频处理

### 采样率转换

| 组件 | 典型采样率 |
|------|-----------|
| TTS 输出（CosyVoice） | 24000 Hz |
| 算法输入（FlashHead/LAM） | 16000 Hz |
| WebRTC 传输 | 48000 Hz |

```python
import librosa
audio_16k = librosa.resample(audio_24k, orig_sr=24000, target_sr=16000)
```

### 音频切片

流式推理需按 chunk 切分音频，使用缓冲区累积，达到 chunk 大小后触发推理：
- **FlashHead**：15360 samples @16kHz（~0.96s，24 帧）
- **MuseTalk**：按 batch_size 决定
- **LAM**：实时逐帧

## 8. 打断与生命周期

### CLIENT_PLAYBACK 流管理

每次 TTS 说话时创建 playback 流，用 `stream_key` 唯一标识：

```python
# 新语音开始 → 打开 playback stream
streamer.open_stream(sources=[input_stream_id], name=f"playback:{stream_key}")
# 持续输出帧 ...
# 语音结束 → 关闭
streamer.finish_current()
```

### 打断处理

在 `get_handler_detail()` 中声明信号过滤：

```python
signal_filters=[SignalFilterRule(
    ChatSignalType.STREAM_CANCEL, None, ChatDataType.CLIENT_PLAYBACK
)]
```

`on_signal()` 中响应：

```python
def on_signal(self, context, signal):
    if (signal.type == ChatSignalType.STREAM_CANCEL
            and signal.related_stream.data_type == ChatDataType.CLIENT_PLAYBACK):
        context.interrupt()
```

打断时必须：
- 设置 `_interrupted = True`
- 清空所有队列（pending audio、output queue）
- 帧收集器丢弃队列帧，切换到 idle 帧输出
- 关闭 playback stream
- 新语音到来时 `reset_interrupt()` 恢复

## 9. 依赖管理

### pyproject.toml 规范

| 规则 | 说明 |
|------|------|
| 不声明 torch 系列 | 由根 pyproject.toml 统一管理（`PROTECTED_PACKAGES`） |
| 不锁死 torch 耦合包 | `xformers`（不加版本），让 pip 自动匹配 |
| 版本约束宽松 | `diffusers>=0.34.0` 而非 `==0.35.0` |
| 注意传递依赖 | 如 mediapipe 对 protobuf、diffusers 对 transformers 的约束 |

### install.py 机制

| 机制 | 说明 |
|------|------|
| `VERSION_OVERRIDES` | 跨 handler 版本冲突时的全局统一版本 |
| `PROTECTED_PACKAGES` | 禁止降级的包（torch 等） |
| `NO_BUILD_ISOLATION_PKGS` | 需要 `--no-build-isolation` 的编译包 |
| `PACKAGE_REPLACEMENTS` | 包名替换（如 onnxruntime → onnxruntime-gpu） |
| `MAX_COMPILE_JOBS` | 限制编译并发，防止 OOM |

### 常见冲突

| 依赖 | 问题 | 解决 |
|------|------|------|
| **flash-attn** | 可能与当前 torch ABI 不兼容 | 移除依赖，用 pytorch 原生 attention |
| **diffusers** | 高版本可能要求 transformers 升级 | 限制版本上界（如 `<0.36.0`） |
| **transformers** | 项目锁定版本（ASR 等组件要求） | 不升级 |
| **xformers** | 与 torch 版本强耦合 | 不锁版本 |

### 验证流程

```bash
uv run install.py --all --dry-run                          # 检查依赖合并
uv run install.py --all                                     # 安装
uv pip list | grep -E "torch|xformers|diffusers"           # 确认版本未被降级
```

## 10. GPU 兼容性

### cuDNN

某些 GPU 架构可能与特定 cuDNN 版本不兼容，导致 `CUDNN_STATUS_NOT_INITIALIZED`。建议在 `load()` 中检测并按需禁用：

```python
try:
    x = torch.randn(1, 3, 8, 8, device="cuda")
    torch.nn.functional.conv2d(x, torch.randn(3, 3, 3, 3, device="cuda"), padding=1)
except RuntimeError:
    torch.backends.cudnn.enabled = False
```

### torch.compile

部分模型的 `torch.compile` 在特定环境可能失败，建议提供 fallback：

```python
try:
    model = torch.compile(model)
except Exception:
    pass  # 回退到 eager 模式
```

## 11. Processor 架构清单

新 avatar handler 的 processor 应包含：

- [ ] **audio sliding-window buffer**：deque 维持固定窗口（如 8 秒）
- [ ] **pending audio 双缓冲**：推理用（低采样率）+ 回放用（原始采样率）
- [ ] **output queue**：`Queue[FrameQueueItem]` 配对音视频
- [ ] **frame collector thread**：恒定 FPS 节拍器
- [ ] **idle inference thread**：空音频驱动动态帧
- [ ] **inference lock**：串行化 speech vs idle 推理
- [ ] **interrupt 支持**：清空队列 + 标志位
- [ ] **RGB→BGR 转换**：在入队前完成
- [ ] **per-session state 隔离**：每 session 独立的 latent/buffer

## 12. 配置与注册

### YAML 配置

```yaml
default:
  chat_engine:
    handler_configs:
      NewAvatar:
        module: avatar/<name>/avatar_handler_<name>
        # handler 特有配置 ...
```

双工模式额外添加：SmartTurnEOU、SemanticTurnDetector、DuplexVad。

### 模型下载注册

在 `scripts/download_models.py` 的 `HANDLER_MODEL_REGISTRY` 和 `MODULE_TO_HANDLER` 中添加条目并实现下载函数。

### 模型存放

统一放在 `models/` 下，配置中使用相对路径。多 handler 共享的模型（如 wav2vec2）只下载一份。

## 13. 参考实现

| Handler | 参考价值 |
|---------|---------|
| `avatar/musetalk/` | 最完整：CLIENT_PLAYBACK 管理、打断、帧收集器、音频重采样 |
| `avatar/liteavatar/` | 轻量：idle 信号生成、打断逻辑清晰 |
| `avatar/flashhead/` | 流式扩散：滑动窗口缓冲、idle 推理线程、RGB→BGR |
| `avatar/lam/` | 端侧渲染：子模块引入模式、AVATAR_MOTION_DATA 输出 |

## 14. 最终检查清单

- [ ] 目录结构完整（__init__.py、handler、config、processor、pyproject.toml）
- [ ] git submodule 正确添加（如有第三方代码）
- [ ] Handler 方法全部实现
- [ ] 视频帧输出为 BGR 格式
- [ ] 音视频通过 FrameQueueItem 配对同步输出
- [ ] 空闲时通过空音频生成动态帧（非静态图）
- [ ] 打断正确响应 STREAM_CANCEL 并清空队列
- [ ] CLIENT_PLAYBACK 流正确管理（开始/结束）
- [ ] 采样率转换正确
- [ ] pyproject.toml 不含 torch 系列、不锁死耦合包版本
- [ ] `uv run install.py --all` 无冲突且 torch 未降级
- [ ] download_models.py 注册模型下载
- [ ] YAML 配置文件可正常启动
- [ ] README.md / readme_en.md 同步更新
