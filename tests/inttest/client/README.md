# WebSocket Client Handler 集成测试

## 概述

本测试套件用于验证 WebSocket Client Handler 的完整功能。测试通过模拟客户端和渲染器的行为，使用真实的 ASR、LLM、TTS、Avatar 处理器来验证整个系统的集成。

## 前置条件

### 1. 配置 API 密钥

如果使用在线服务（如阿里云 DashScope），需要配置 API 密钥：

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

### 2. 确保模型已下载

确保下载LAM相关的算法模型

## 运行测试

**终端 1 - 启动测试服务器（需要是https模式启动）：**

```bash
uv run install.py --uv --config config/test_ws_client.yaml
uv run src/demo.py --config config/test_ws_client.yaml
```

**终端 2 - 运行测试：**

```bash
# 运行所有测试
uv run pytest tests/inttest/client/test_ws_client.py -v

# 运行特定测试
uv run pytest tests/inttest/client/test_ws_client.py::TestWSClientIntegration::test_01_session_initialization -v

# 显示详细日志
uv run pytest tests/inttest/client/test_ws_client.py -v -s

# 运行单个测试并显示输出
uv run pytest tests/inttest/client/test_ws_client.py::TestWSClientIntegration::test_05_text_input_and_echo -v -s
```

## 测试覆盖

本测试套件包含以下测试用例：

### ✅ test_01_session_initialization
- 测试会话初始化流程
- 验证 InitializeAvatarSession 消息
- 验证 AvatarSessionInitialized 响应

### ✅ test_02_render_port_connection
- 测试渲染端口连接
- 验证双端口设计
- 验证 Welcome Message 的接收和解析

### ✅ test_03_audio_streaming
- 测试音频流上传（纯二进制格式）
- 验证 JBIN 头部格式
- 验证连续音频包发送

### ✅ test_04_video_upload
- 测试视频帧上传（JSON + 二进制）
- 验证 SendHumanVideo 消息
- 验证 JPEG 图像数据传输

### ✅ test_05_text_input_and_echo
- 测试文本输入
- 验证 SendHumanText 消息
- 验证 EchoAvatarText 响应（LLM 回复）

### ✅ test_06_motion_data_output
- 测试 Motion Data 输出
- 验证 MotionData JSON 消息
- 验证 JBIN 二进制数据
- 验证 ARKit blendshapes 和音频数据

### ✅ test_07_end_speech_handling
- 测试 EndSpeech 消息处理
- 验证 speech_id 提取
- 验证 VAD 重新启用机制

### ✅ test_08_heartbeat_mechanism
- 测试心跳机制
- 验证 TriggerHeartbeat 消息
- 验证 AvatarHeartbeat 响应

### ✅ test_09_interrupt_signal
- 测试打断信号
- 验证 Interrupt 消息
- 验证 InterruptAccepted 响应

## 测试数据

测试使用以下模拟数据：

- **音频**：440Hz 正弦波，16kHz 采样率，int16 格式
- **视频**：640x480 渐变图像，JPEG 编码
- **文本**：简短的中文测试文本

## 注意事项

### 性能考虑

- 某些测试可能需要较长时间（5-30秒），因为需要等待真实的模型处理
- LLM 和 TTS 调用可能需要网络请求
- 首次运行可能需要下载模型

### 端口占用

- 测试服务器使用端口 8283
- 确保该端口未被其他程序占用
- 如需更改端口，修改 `config/test_ws_client.yaml` 和 `test_ws_client.py` 中的端口

### 超时设置

- 大部分测试使用 5 秒超时
- Motion Data 相关测试使用 30 秒超时（等待模型处理）
- 如果测试超时，可能是：
  - 模型加载时间过长
  - 网络请求延迟
  - API 配额限制

### 调试技巧

1. **查看服务器日志**：在服务器终端查看详细日志
2. **使用 -s 参数**：`pytest -v -s` 显示 print 输出
3. **单独运行测试**：先运行简单测试（如 test_01），再运行复杂测试
4. **检查连接**：确保 WebSocket 连接成功建立

## 文件结构

```
tests/inttest/client/
├── __init__.py              # 模块初始化
├── ws_test_utils.py         # 测试工具函数
├── test_ws_client.py        # 主测试文件
└── README.md                # 本文档
```

## 相关文档

- [WebSocket 协议文档](../../../docs/交互数字人WebSocket协议接口.md)
- [测试配置](../../../config/test_ws_client.yaml)



