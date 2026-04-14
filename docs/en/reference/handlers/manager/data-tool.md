# Manager Console

Manager is a passive monitoring handler that listens to all data streams and signal events in the chat engine, pushing structured information to the browser-based console via WebSocket.

After starting the service, visit `https://<host>:8282/ui/manager.html` to open the console.

## Features

| Feature | Description |
|---------|-------------|
| Session Management | Tab-based per-session view with green activity indicator |
| Chat Records | Displays human/avatar text and audio in chat bubble format, with playback and download |
| Signal Flow Graph | Vue Flow-based visualization showing signal flow between handlers with timing |
| Config Viewer | Displays current engine configuration (handler list, concurrency, model paths, etc.) |
| Remote Interrupt | Send interrupt signals to specific sessions directly from the console |

## Configuration

Add the Manager config under `handler_configs` in your YAML configuration file:

```yaml
handler_configs:
  # ... other handler configs ...
  Manager:
    module: manager/handler_data_tool
    buffer_limit: 200          # optional, max records per session
    preview_bytes: 4096        # optional, binary data preview size
    preview_chars: 512         # optional, text payload preview size
    include_binary_preview: false  # optional, include base64 preview for ndarray data
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| module | manager/handler_data_tool | Handler module path (required) |
| buffer_limit | 200 | Maximum event records kept per session |
| preview_bytes | 4096 | Preview size for binary data such as audio frames (bytes) |
| preview_chars | 512 | Preview character count for text payloads |
| include_binary_preview | false | Whether to include base64 preview for ndarray data in events |

> [!TIP]
> Manager is entirely optional. If you don't need monitoring, simply remove the `Manager` section from your config. Removing it has no impact on the conversation pipeline.

## API Endpoints

Manager registers the following endpoints:

| Endpoint | Type | Description |
|----------|------|-------------|
| `/ws/manager/data_tool` | WebSocket | Real-time event push, config snapshot, remote interrupt |
| `/download/manager/data_tool/file` | GET | Download audio/image temp files (restricted to `temp/data_tool/` directory) |

### WebSocket Protocol

After connection is established, the server automatically sends:

1. **`snapshot`** — Historical event snapshot for all sessions
2. **`current_config`** — Current engine configuration

The server then pushes data events and signal events in real time for each session.

Client-to-server messages:

```json
{
  "event": "interrupt",
  "session_id": "<target_session_id>"
}
```

### Authentication

The console supports optional token-based authentication. Enter a token in the "Auth Settings" in the top-right corner, and it will be automatically attached to WebSocket connections and file download requests.

## Console Interface

### Session List

The top of the page shows all sessions as tabs. Sessions with activity within the last 60 seconds show a green indicator; inactive sessions show gray.

### Chat Records

The left panel shows the chat records for the selected session:

- **Human** messages: speech recognition text and raw audio
- **Avatar** messages: reply text and synthesized speech

Audio messages support inline playback and download (WAV format).

### Signal Flow Graph

The right panel shows the signal flow between handlers:

- Each node represents a handler
- Edges indicate signal flow direction
- Active signal flows are shown with animated edges
- Processing duration (milliseconds) is displayed above each node
- Nodes exceeding 10 seconds show a timeout style

### Config Viewer

The bottom-right section displays the complete engine configuration, including each handler's parameters, concurrency limits, and more.
