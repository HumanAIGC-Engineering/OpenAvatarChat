# Manager 监控台

Manager 是一个被动式的监控 Handler，它监听对话引擎中所有数据流和信号事件，并通过 WebSocket 将结构化的信息推送到浏览器端的监控台页面。

启动服务后，访问 `https://<host>:8282/ui/manager.html` 即可打开监控台。

## 功能概览

| 功能 | 说明 |
|------|------|
| 会话管理 | 按 Session 分标签页展示，活跃会话带绿色指示灯 |
| 对话记录 | 以聊天气泡形式展示人类/数字人的文本和音频，支持在线播放和下载 |
| 信号流图 | 基于 Vue Flow 的可视化流程图，展示各 Handler 之间的信号传递和耗时 |
| 配置查看 | 展示当前引擎配置（Handler 列表、并发数、模型路径等） |
| 远程打断 | 在监控台中直接发送打断信号到指定会话 |

## 配置参数

在 YAML 配置文件的 `handler_configs` 中添加 Manager 配置：

```yaml
handler_configs:
  # ... 其他 Handler 配置 ...
  Manager:
    module: manager/handler_data_tool
    buffer_limit: 200          # 可选，每个会话保留的最大记录数
    preview_bytes: 4096        # 可选，二进制数据预览大小
    preview_chars: 512         # 可选，文本数据预览大小
    include_binary_preview: false  # 可选，是否包含 ndarray 的 base64 预览
```

| 参数 | 默认值 | 说明 |
|------|--------|------|
| module | manager/handler_data_tool | Handler 模块路径（必填） |
| buffer_limit | 200 | 每个会话保留的最大事件记录数 |
| preview_bytes | 4096 | 二进制数据（如音频帧）的预览大小（字节） |
| preview_chars | 512 | 文本载荷的预览字符数 |
| include_binary_preview | false | 是否在事件中包含 ndarray 数据的 base64 预览 |

> [!TIP]
> Manager 是完全可选的。如果你不需要监控功能，可以直接从配置中移除 `Manager` 部分。移除后不会影响对话流程。

## 接口说明

Manager 注册了以下接口：

| 接口 | 类型 | 说明 |
|------|------|------|
| `/ws/manager/data_tool` | WebSocket | 实时事件推送、配置快照、远程打断 |
| `/download/manager/data_tool/file` | GET | 下载音频/图片等临时文件（仅限 `temp/data_tool/` 目录） |

### WebSocket 协议

连接建立后，服务端会自动发送：

1. **`snapshot`** — 当前所有会话的历史事件快照
2. **`current_config`** — 当前引擎配置

后续服务端会实时推送每个会话中的数据事件和信号事件。

客户端可发送的消息：

```json
{
  "event": "interrupt",
  "session_id": "<目标会话ID>"
}
```

### 认证

监控台支持可选的 Token 认证。在页面右上角的"认证设置"中输入 Token 后，WebSocket 连接和文件下载请求会自动附带该 Token。

## 监控台界面

### 会话列表

页面顶部以标签页形式展示所有会话。60 秒内有活动的会话会显示绿色指示灯，超过 60 秒无活动则显示灰色。

### 对话记录

左侧面板展示选中会话的对话记录：

- **Human** 消息：用户的语音识别文本和原始音频
- **Avatar** 消息：数字人的回复文本和合成语音

音频消息支持在线播放和下载（WAV 格式）。

### 信号流图

右侧面板展示 Handler 之间的信号流动图：

- 每个节点代表一个 Handler
- 边表示信号传递方向
- 活跃的信号流显示为动画边
- 节点上方显示处理耗时（毫秒）
- 处理超过 10 秒的节点会显示超时样式

### 配置查看

右下角展示当前引擎的完整配置，包括各 Handler 的配置参数、并发限制等。
