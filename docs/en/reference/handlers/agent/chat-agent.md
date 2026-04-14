# Chat Agent Handler

Chat Agent is a Handler type parallel to LLM Handler. It uses a multi-turn tool-calling Agent to replace the traditional single-turn LLM Handler, providing tool calling, memory management, and external system integration.

> [!NOTE]
> This Handler is currently in Beta. See [Beta: Chat Agent](/en/beta/chat-agent) for the full guide.

## Configuration

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

| Parameter | Default | Description |
|---|---|---|
| oc_bridge.enabled | false | Enable OpenClaw Bridge |
| oc_bridge.plugin_tools_cmd | - | Plugin Tools MCP startup command |
| oc_bridge.gateway_http_url | http://localhost:18789 | OpenClaw Gateway HTTP address |
| oc_bridge.webhook_path | /webhook/oac-bridge | Webhook path on OC Gateway |
| oc_bridge.callback_port | 8011 | OAC callback HTTP service port |
| oc_bridge.token | "" | Shared auth token |
