# OpenAI Compatible LLM Handler

Uses OpenAI-compatible APIs for language model inference.

## Configuration

```yaml
LLMOpenAICompatible:
  model_name: "qwen-plus"
  system_prompt: "You are an AI digital human."
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # optional; falls back to api_key_env
  api_key_env: "DASHSCOPE_API_KEY"
```

| Parameter | Default | Description |
|---|---|---|
| LLMOpenAICompatible.model_name | qwen-plus | Model name |
| LLMOpenAICompatible.system_prompt | | System prompt |
| LLMOpenAICompatible.api_url | | API URL |
| LLMOpenAICompatible.api_key | | API Key |
| LLMOpenAICompatible.api_key_env | DASHSCOPE_API_KEY | Environment variable to read when `api_key` is not set |

> [!TIP]
> OpenAvatarChat reads `.env` from the working directory for environment variables.
