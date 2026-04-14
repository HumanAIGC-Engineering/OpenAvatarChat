# Dify Chatflow Handler

集成 Dify 的 Chatflow，用户可以在 Dify 中创建一个 Chatflow，将生成的应用的 API URL 和 API Key 填入配置即可使用。

## 配置参数

```yaml
Dify:
  enabled: True
  module: llm/dify/llm_handler_dify
  enable_video_input: False  # 是否允许摄像头输入
  api_key: ''                # Dify API Key
  api_url: 'http://localhost/v1'  # Dify API URL
```
