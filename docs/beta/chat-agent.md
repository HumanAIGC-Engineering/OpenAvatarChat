# Chat Agent 模式（OpenClaw 集成）

> [!WARNING]
> 此功能目前处于 **Beta** 阶段，API 和配置格式可能随时变化。

## 功能与定位

Chat Agent 模式使用一个 **多轮工具调用 Agent** 替代传统的单轮 LLM Handler，为数字人提供：

- **工具调用**：Agent 可以多轮调用工具（获取时间、系统信息等），而不仅仅是单次问答
- **人格与长期记忆**：通过 OpenClaw 的 Agent Profile（IDENTITY.md / SOUL.md）赋予数字人持久人格
- **对话上下文压缩**：对话过长时自动压缩历史，保留关键上下文
- **后台任务协作**：通过 OpenClaw 的 oac-bridge 通道，数字人可以在后台执行复杂任务（如代码执行），并将结果以自然口语反馈给用户
- **视觉感知**：结合 PerceptionAgent 处理摄像头输入，让数字人具备环境感知和主动交互能力
- **双工打断**：支持用户随时打断数字人的回答

**架构关系**：Chat Agent 替代了配置中原有的 `LLMOpenAICompatible` Handler。它在内部使用 OpenAI 兼容 API 进行 LLM 推理，同时增加了工具调用循环、记忆管理和 OpenClaw 桥接能力。

## 前置条件

1. **OpenClaw**：需要安装并运行 [OpenClaw](https://github.com/openclaw/openclaw) Gateway
2. **百炼 API Key**：Agent 和 TTS 均使用百炼 API，需设置 `DASHSCOPE_API_KEY` 环境变量
3. **oac-bridge 插件**：需要将本仓库中的 oac-bridge 插件部署到 OpenClaw 中

## 部署 oac-bridge 插件到 OpenClaw

oac-bridge 是一个 OpenClaw 频道插件，负责 OAC 与 OpenClaw 之间的双向消息传递和工具调用。插件源码位于本仓库的 `extensions/openclaw/oac-bridge/` 目录。

### 步骤 1：将插件复制到 OpenClaw 的 extensions 目录

```bash
# 假设 OpenClaw 仓库克隆在 ~/Code/openclaw
# 将 oac-bridge 插件复制到 OpenClaw 的 extensions 目录
cp -r extensions/openclaw/oac-bridge ~/Code/openclaw/extensions/oac-bridge
```

### 步骤 2：在 OpenClaw 中注册工作区包

编辑 OpenClaw 根目录的 `package.json`，在 `workspaces` 数组中添加 oac-bridge：

```json
{
  "workspaces": [
    "extensions/oac-bridge"
  ]
}
```

> [!NOTE]
> 如果 OpenClaw 的 `package.json` 已经有 `workspaces` 字段，只需在数组中追加 `"extensions/oac-bridge"` 即可。

### 步骤 3：安装依赖并编译

```bash
cd ~/Code/openclaw

# 安装依赖（会自动链接 oac-bridge 工作区包）
pnpm install

# 编译 OpenClaw（oac-bridge 依赖编译产物）
pnpm build
```

> [!IMPORTANT]
> `pnpm build` 必须成功完成，因为 OAC 侧的 `plugin_tools_cmd` 需要指向编译后的 `dist/mcp/plugin-tools-serve.js`。

### 步骤 4：配置 OpenClaw

OpenClaw 的配置默认写在 **`~/.openclaw/openclaw.json`**（若设置了环境变量 `OPENCLAW_CONFIG_PATH`，则以该路径为准）。oac-bridge 读取的是其中的 **`channels["oac-bridge"]`** 段。

**方式 A：CLI（推荐）**

OpenClaw 自带子命令 `openclaw config set <点号路径> <值>`，会合并写入上述配置文件。路径里的 `oac-bridge` 是**一个**键名（含连字符），点号只分隔层级，因此应写成：

```bash
# 设置 OAC 回调地址（端口需与 OAC 的 oc_bridge.callback_port 一致，默认 8011）
openclaw config set channels.oac-bridge.callbackUrl "http://localhost:8011/oc-reply"

# （可选）共享认证 token，需与 OAC 侧 oc_bridge.token 一致
openclaw config set channels.oac-bridge.token "your-shared-token"
```

**方式 B：直接编辑配置文件**

与上面 CLI 等价，可在 `~/.openclaw/openclaw.json` 中手动加入或修改（JSON / JSON5 中键名需加引号）：

```json
{
  "channels": {
    "oac-bridge": {
      "callbackUrl": "http://localhost:8011/oc-reply",
      "token": "your-shared-token"
    }
  }
}
```

**方式 C：环境变量（覆盖缺省）**

插件在解析配置时，若配置文件里未设置对应项，会回退到环境变量（与 `extensions/oac-bridge/src/accounts.ts` 一致）：

| 环境变量 | 对应配置项 |
|---|---|
| `OAC_CALLBACK_URL` | `channels.oac-bridge.callbackUrl` |
| `OAC_BRIDGE_TOKEN` | `channels.oac-bridge.token` |

修改配置或环境变量后，需要**重启** OpenClaw Gateway 才会生效。

### 步骤 5：启动 OpenClaw Gateway

```bash
openclaw gateway run
```

启动成功后，在 OpenClaw 日志中应能看到：
```
Registered HTTP route: /webhook/oac-bridge for OAC Bridge
```

### 插件配置参数说明

以下参数写在 OpenClaw 的 `~/.openclaw/openclaw.json`（或 `OPENCLAW_CONFIG_PATH`）里，也可用 `openclaw config set` 或环境变量（见上文）设置：

| 参数 | 默认值 | 说明 |
|---|---|---|
| `channels.oac-bridge.callbackUrl` | - | OC Agent 回复消息时回调的 OAC HTTP 地址，**必填** |
| `channels.oac-bridge.token` | `""` | 共享认证 token，用于双向 HTTP 请求的 Bearer 认证 |
| `channels.oac-bridge.webhookPath` | `/webhook/oac-bridge` | OAC 发送消息到 OC 时使用的 webhook 路径 |
| `channels.oac-bridge.enabled` | `true` | 是否启用此通道 |

### 插件提供的工具

oac-bridge 插件还注册了两个 Agent 工具，OAC 通过 Plugin Tools MCP 调用：

| 工具 | 说明 |
|---|---|
| `get_agent_profile` | 读取 OpenClaw workspace 中的 `IDENTITY.md`、`SOUL.md`、`USER.md`，用于获取 Agent 的人格和用户偏好 |
| `list_scheduled_tasks` | 列出 OpenClaw 中已配置的定时任务/提醒 |

## OAC 侧配置

Agent 示例配置文件为 `config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml`，其中关键的 `oc_bridge` 部分：

```yaml
ChatAgent:
  module: agent/chat_agent_handler
  llm_model: "qwen3.6-plus"
  api_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  # ...其他配置...
  oc_bridge:
    enabled: true
    # Plugin Tools MCP 启动命令 — 需指向 OpenClaw 编译产物的绝对路径
    plugin_tools_cmd: "node /home/you/Code/openclaw/dist/mcp/plugin-tools-serve.js"
    # OpenClaw Gateway 的 HTTP 地址（本地连接使用 localhost）
    gateway_http_url: "http://localhost:18789"
    # OAC 回调 HTTP 服务端口（OpenClaw 的 callbackUrl 中的端口需与此一致）
    callback_port: 8011
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `oc_bridge.enabled` | `false` | 是否启用 OpenClaw Bridge |
| `oc_bridge.plugin_tools_cmd` | - | Plugin Tools MCP 启动命令，需修改为你本地 OpenClaw 编译产物的**绝对路径** |
| `oc_bridge.gateway_http_url` | `http://localhost:18789` | OpenClaw Gateway 的 HTTP 地址 |
| `oc_bridge.webhook_path` | `/webhook/oac-bridge` | OC Gateway 上的 webhook 路径 |
| `oc_bridge.callback_port` | `8011` | OAC 回调 HTTP 服务端口 |
| `oc_bridge.token` | `""` | 共享认证 token（留空表示不认证） |

> [!IMPORTANT]
> `plugin_tools_cmd` 中的路径必须是**绝对路径**，因为 OAC 进程可能在不同的工作目录下启动。例如：
> ```yaml
> plugin_tools_cmd: "node /home/luyi/Code/openclaw/dist/mcp/plugin-tools-serve.js"
> ```

## 数据流

```
OAC (port 8283)                          OpenClaw Gateway (port 18789)
     │                                        │
     ├──POST /webhook/oac-bridge──────────▶   │  用户消息 → OC Agent
     │                                        │
     │   ◀──POST localhost:8011/oc-reply───   │  OC Agent 回复 → OAC
     │                                        │
     ├──stdio── Plugin Tools MCP ─────────▶   │  工具调用（profile, memory, tasks）
```

**消息流程详解：**

1. **用户说话** → OAC 的 ChatAgent 处理用户输入
2. **OAC → OC**：ChatAgent 通过 HTTP POST 将消息发送到 OpenClaw Gateway 的 `/webhook/oac-bridge` 端点
3. **OC Agent 处理**：OpenClaw Agent 接收消息，可能调用工具、查询记忆等
4. **OC → OAC**：OpenClaw Agent 的回复通过 HTTP POST 发送到 OAC 的回调地址 `http://localhost:8011/oc-reply`
5. **OAC TTS → Avatar**：ChatAgent 将回复文本交给 TTS 和 Avatar 合成语音和动画
6. **Plugin Tools MCP**：OAC 的 ChatAgent 通过 stdio 管道直接调用 OpenClaw 的 MCP 工具（get_agent_profile、list_scheduled_tasks 等）

## 启动与验证

> [!IMPORTANT]
> 请确保 OAC 和 OpenClaw 运行在**同一台机器**上（本地连接），目前暂未测试跨机器部署。

```bash
# 1. 启动 OpenClaw Gateway（在终端 A）
cd ~/Code/openclaw
openclaw gateway run

# 2. 安装 OAC 依赖（在终端 B）
cd ~/Code/OpenAvatarChat
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml

# 3. 下载模型
uv run scripts/download_models.py --handler flashhead

# 4. 启动 OAC Agent 模式
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml
```

### 验证连接

启动后在日志中确认以下关键信息：

**OAC 侧日志：**
- `[ChatAgent] OC Channel Client started` — OAC ↔ OC HTTP 通道已建立
- `[ChatAgent] OC MCP Client connected` — Plugin Tools MCP 已连接

**OpenClaw 侧日志：**
- `Registered HTTP route: /webhook/oac-bridge` — webhook 已注册
- `Starting OAC Bridge channel` — oac-bridge 通道已启动

### 常见问题

| 问题 | 可能原因 | 解决方案 |
|---|---|---|
| `OC MCP Client` 连接失败 | `plugin_tools_cmd` 路径错误 | 确认路径指向 OpenClaw 编译后的 `dist/mcp/plugin-tools-serve.js`，需先运行 `pnpm build` |
| `OC Channel Client` 连接失败 | OpenClaw Gateway 未启动或端口不对 | 确认 `openclaw gateway run` 已运行，默认端口 18789 |
| OC Agent 不回复 | `callbackUrl` 未配置 | 运行 `openclaw config set channels.oac-bridge.callbackUrl "http://localhost:8011/oc-reply"` |
| `401 Invalid token` | token 不匹配 | 确保 OAC 的 `oc_bridge.token` 与 OpenClaw 的 `channels.oac-bridge.token` 一致 |

> [!TIP]
> 如果不需要 OpenClaw 集成，可以将 `oc_bridge.enabled` 设为 `false`，Agent 仍然可以独立运行，保留工具调用、上下文压缩等本地能力。
