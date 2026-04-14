# Chat Agent Handler

Chat Agent 是与 LLM Handler 平级的 Handler 类型。它使用一个多轮工具调用 Agent 替代传统的单轮 LLM Handler，为数字人提供工具调用、记忆管理和外部系统集成能力。

> [!NOTE]
> 此 Handler 目前处于 Beta 阶段。完整的使用指南请参见 [Beta: Chat Agent](/beta/chat-agent)。

## 配置参数

```yaml
ChatAgent:
  module: agent/chat_agent_handler
  llm_model: "qwen3.6-plus"
  api_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  oc_bridge:
    enabled: true
    plugin_tools_cmd: "node /path/to/openclaw/dist/mcp/plugin-tools-serve.js"
    gateway_http_url: "http://localhost:18789"
    callback_port: 8011
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| oc_bridge.enabled | false | 是否启用 OpenClaw Bridge |
| oc_bridge.plugin_tools_cmd | - | Plugin Tools MCP 启动命令 |
| oc_bridge.gateway_http_url | http://localhost:18789 | OpenClaw Gateway HTTP 地址 |
| oc_bridge.webhook_path | /webhook/oac-bridge | OC Gateway 上的 webhook 路径 |
| oc_bridge.callback_port | 8011 | OAC 回调 HTTP 服务端口 |
| oc_bridge.token | "" | 共享认证 token |
