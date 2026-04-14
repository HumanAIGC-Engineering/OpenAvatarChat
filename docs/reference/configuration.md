# 配置说明

程序启动时需要通过 `--config` 参数指定配置文件。

```bash
uv run src/demo.py --config <配置文件路径>.yaml
```

## 全局参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| log.log_level | INFO | 程序的日志级别 |
| service.host | 0.0.0.0 | 服务的监听地址 |
| service.port | 8282 | 服务的监听端口 |
| service.cert_file | ssl_certs/localhost.crt | SSL 证书文件路径 |
| service.cert_key | ssl_certs/localhost.key | SSL 密钥文件路径 |
| chat_engine.model_root | models | 模型的根目录 |
| chat_engine.handler_configs | N/A | 由各 Handler 提供的可配置项 |

> [!IMPORTANT]
> 所有配置中的路径参数都可以使用绝对路径，或者相对于项目根目录的相对路径。

## Handler 配置参考

各 Handler 的详细配置参数请参见 [Handler 参考](/reference/handlers/)。
