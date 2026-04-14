# Configuration

Config is loaded from the file specified by the `--config` parameter.

```bash
uv run src/demo.py --config <path-to-config>.yaml
```

## Global Parameters

| Parameter | Default | Description |
|---|---|---|
| log.log_level | INFO | Log level |
| service.host | 0.0.0.0 | Service listen address |
| service.port | 8282 | Service listen port |
| service.cert_file | ssl_certs/localhost.crt | SSL certificate file path |
| service.cert_key | ssl_certs/localhost.key | SSL key file path |
| chat_engine.model_root | models | Model root directory |
| chat_engine.handler_configs | N/A | Handler-specific configs |

> [!IMPORTANT]
> All path parameters can use absolute paths or paths relative to the project root.

## Handler Configuration

See [Handler Reference](/en/reference/handlers/) for per-handler configuration details.
