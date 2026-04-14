# LAM 端侧渲染 Client Handler

端侧渲染基于 [RTC Client Handler](/reference/handlers/client/rtc-client) 扩展，支持多路连接，可以通过配置文件选择形象。

## 形象选择

形象可以通过 [LAM](https://github.com/aigc3d/LAM) 项目进行训练。本项目中预置了 4 个范例形象，位于 `src/handlers/client/ws_lam_client/lam_samples` 下。

```yaml
LamClient:
  module: client/ws_lam_client/ws_lam_client_handler
  asset_path: "lam_samples/barbara.zip"
  concurrent_limit: 5
```
