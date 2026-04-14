# Chat Agent Mode (OpenClaw Integration)

> [!WARNING]
> This feature is currently in **Beta**. APIs and configuration formats may change at any time.

## Features and Purpose

Chat Agent mode replaces the traditional single-turn LLM Handler with a **multi-turn tool-calling Agent**, providing:

- **Tool Calling**: Invoke tools across multiple turns (get time, system info, etc.)
- **Persona & Long-term Memory**: Persistent persona through OpenClaw's Agent Profile (IDENTITY.md / SOUL.md)
- **Context Compression**: Automatically compresses conversation history when too long
- **Background Task Collaboration**: Execute complex tasks in the background via OpenClaw's oac-bridge channel
- **Visual Perception**: Camera input processing via PerceptionAgent for environment awareness
- **Duplex Interruption**: User can interrupt the digital human at any time

**Architecture**: Chat Agent replaces `LLMOpenAICompatible` Handler. It uses OpenAI-compatible APIs internally while adding tool-calling loops, memory management, and OpenClaw bridging.

## Prerequisites

1. **OpenClaw**: Install and run [OpenClaw](https://github.com/openclaw/openclaw) Gateway
2. **Bailian API Key**: Set the `DASHSCOPE_API_KEY` environment variable
3. **oac-bridge Plugin**: Deploy the oac-bridge plugin from this repository into OpenClaw

## Deploy the oac-bridge Plugin to OpenClaw

oac-bridge is an OpenClaw channel plugin that handles bidirectional message passing and tool calling between OAC and OpenClaw. The plugin source code is located in this repository at `extensions/openclaw/oac-bridge/`.

### Step 1: Copy the Plugin to OpenClaw's Extensions Directory

```bash
# Assuming OpenClaw is cloned at ~/Code/openclaw
cp -r extensions/openclaw/oac-bridge ~/Code/openclaw/extensions/oac-bridge
```

### Step 2: Register the Workspace Package in OpenClaw

Edit the `package.json` in OpenClaw's root directory and add oac-bridge to the `workspaces` array:

```json
{
  "workspaces": [
    "extensions/oac-bridge"
  ]
}
```

> [!NOTE]
> If OpenClaw's `package.json` already has a `workspaces` field, simply append `"extensions/oac-bridge"` to the existing array.

### Step 3: Install Dependencies and Build

```bash
cd ~/Code/openclaw

# Install dependencies (automatically links the oac-bridge workspace package)
pnpm install

# Build OpenClaw (oac-bridge requires the compiled output)
pnpm build
```

> [!IMPORTANT]
> `pnpm build` must complete successfully because the OAC-side `plugin_tools_cmd` points to the compiled `dist/mcp/plugin-tools-serve.js`.

### Step 4: Configure OpenClaw

OpenClaw stores config in **`~/.openclaw/openclaw.json`** by default (or whatever path you set in **`OPENCLAW_CONFIG_PATH`**). The oac-bridge plugin reads the **`channels["oac-bridge"]`** object.

**Option A: CLI (recommended)**

OpenClaw provides `openclaw config set <dot.path> <value>`, which merges into that file. The segment `oac-bridge` is a **single** key (hyphenated); dots only separate levels, so use:

```bash
openclaw config set channels.oac-bridge.callbackUrl "http://localhost:8011/oc-reply"
openclaw config set channels.oac-bridge.token "your-shared-token"
```

**Option B: Edit the config file directly**

Equivalent to the CLI—edit `~/.openclaw/openclaw.json` (JSON / JSON5; quote keys with hyphens):

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

**Option C: Environment variables (fallback)**

If a value is missing from the config file, the plugin falls back to env vars (see `extensions/oac-bridge/src/accounts.ts`):

| Environment variable | Config field |
|---|---|
| `OAC_CALLBACK_URL` | `channels.oac-bridge.callbackUrl` |
| `OAC_BRIDGE_TOKEN` | `channels.oac-bridge.token` |

Restart the OpenClaw Gateway after changing config or env vars.

### Step 5: Start OpenClaw Gateway

```bash
openclaw gateway run
```

On successful startup, you should see in the OpenClaw logs:
```
Registered HTTP route: /webhook/oac-bridge for OAC Bridge
```

### Plugin Configuration Reference

These parameters live in `~/.openclaw/openclaw.json` (or `OPENCLAW_CONFIG_PATH`). Set them with `openclaw config set`, by editing the file, or via env vars (see above):

| Parameter | Default | Description |
|---|---|---|
| `channels.oac-bridge.callbackUrl` | - | HTTP URL where OC Agent posts replies back to OAC. **Required.** |
| `channels.oac-bridge.token` | `""` | Shared auth token for Bearer authentication on both directions |
| `channels.oac-bridge.webhookPath` | `/webhook/oac-bridge` | HTTP path on the gateway where OAC posts inbound messages |
| `channels.oac-bridge.enabled` | `true` | Whether to enable this channel |

### Plugin-Provided Tools

The oac-bridge plugin also registers two Agent tools, called by OAC via Plugin Tools MCP:

| Tool | Description |
|---|---|
| `get_agent_profile` | Reads `IDENTITY.md`, `SOUL.md`, `USER.md` from the OpenClaw workspace for Agent persona and user preferences |
| `list_scheduled_tasks` | Lists configured cron/scheduled tasks and reminders in OpenClaw |

## OAC Configuration

Example config: `config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml`. The key `oc_bridge` section:

```yaml
ChatAgent:
  module: agent/chat_agent_handler
  llm_model: "qwen3.6-plus"
  api_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  # ...other configs...
  oc_bridge:
    enabled: true
    # Plugin Tools MCP command — must point to the absolute path of OpenClaw's compiled output
    plugin_tools_cmd: "node /home/you/Code/openclaw/dist/mcp/plugin-tools-serve.js"
    # OpenClaw Gateway HTTP address (use localhost for local connections)
    gateway_http_url: "http://localhost:18789"
    # OAC callback HTTP service port (must match the port in OpenClaw's callbackUrl)
    callback_port: 8011
```

| Parameter | Default | Description |
|---|---|---|
| `oc_bridge.enabled` | `false` | Enable OpenClaw Bridge |
| `oc_bridge.plugin_tools_cmd` | - | Plugin Tools MCP startup command. Must be the **absolute path** to your local OpenClaw build output |
| `oc_bridge.gateway_http_url` | `http://localhost:18789` | OpenClaw Gateway HTTP address |
| `oc_bridge.webhook_path` | `/webhook/oac-bridge` | Webhook path on OC Gateway |
| `oc_bridge.callback_port` | `8011` | OAC callback HTTP service port |
| `oc_bridge.token` | `""` | Shared auth token (empty = no auth) |

> [!IMPORTANT]
> The path in `plugin_tools_cmd` must be an **absolute path**, since the OAC process may start from a different working directory. For example:
> ```yaml
> plugin_tools_cmd: "node /home/luyi/Code/openclaw/dist/mcp/plugin-tools-serve.js"
> ```

## Data Flow

```
OAC (port 8283)                          OpenClaw Gateway (port 18789)
     |                                        |
     |--POST /webhook/oac-bridge---------->   |  User message -> OC Agent
     |                                        |
     |   <--POST localhost:8011/oc-reply---   |  OC Agent reply -> OAC
     |                                        |
     |--stdio-- Plugin Tools MCP ---------->  |  Tool calls (profile, memory, tasks)
```

**Detailed message flow:**

1. **User speaks** → OAC's ChatAgent processes the input
2. **OAC → OC**: ChatAgent sends the message via HTTP POST to OpenClaw Gateway's `/webhook/oac-bridge` endpoint
3. **OC Agent processes**: OpenClaw Agent receives the message, may call tools, query memory, etc.
4. **OC → OAC**: OpenClaw Agent's reply is sent via HTTP POST to OAC's callback at `http://localhost:8011/oc-reply`
5. **OAC TTS → Avatar**: ChatAgent passes the reply text to TTS and Avatar for speech and animation synthesis
6. **Plugin Tools MCP**: OAC's ChatAgent calls OpenClaw's MCP tools directly via stdio pipe (get_agent_profile, list_scheduled_tasks, etc.)

## Startup and Verification

> [!IMPORTANT]
> OAC and OpenClaw must run on the **same machine** (local connection). Cross-machine deployment has not been tested yet.

```bash
# 1. Start OpenClaw Gateway (in Terminal A)
cd ~/Code/openclaw
openclaw gateway run

# 2. Install OAC dependencies (in Terminal B)
cd ~/Code/OpenAvatarChat
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml

# 3. Download models
uv run scripts/download_models.py --handler flashhead

# 4. Start OAC Agent mode
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead_duplex_agent.yaml
```

### Verify the Connection

After startup, confirm these key messages in the logs:

**OAC logs:**
- `[ChatAgent] OC Channel Client started` — HTTP channel between OAC and OC established
- `[ChatAgent] OC MCP Client connected` — Plugin Tools MCP connected

**OpenClaw logs:**
- `Registered HTTP route: /webhook/oac-bridge` — Webhook registered
- `Starting OAC Bridge channel` — oac-bridge channel started

### Troubleshooting

| Issue | Possible Cause | Solution |
|---|---|---|
| `OC MCP Client` connection fails | Wrong `plugin_tools_cmd` path | Verify the path points to OpenClaw's compiled `dist/mcp/plugin-tools-serve.js`; run `pnpm build` first |
| `OC Channel Client` connection fails | OpenClaw Gateway not running or wrong port | Confirm `openclaw gateway run` is running; default port is 18789 |
| OC Agent doesn't reply | `callbackUrl` not configured | Run `openclaw config set channels.oac-bridge.callbackUrl "http://localhost:8011/oc-reply"` |
| `401 Invalid token` | Token mismatch | Ensure OAC's `oc_bridge.token` matches OpenClaw's `channels.oac-bridge.token` |

> [!TIP]
> Set `oc_bridge.enabled` to `false` to run the Agent independently without OpenClaw, retaining tool calling, context compression, and other local capabilities.
