# OpenAI 兼容 LLM Handler

使用 OpenAI 兼容 API 进行语言模型推理。如果你已有一个可调用的 LLM API Key，可以用这种方式启动来体验对话数字人。

## 配置参数

```yaml
LLMOpenAICompatible: 
  model_name: "qwen-plus"
  system_prompt: "你是个AI对话数字人，你要用简短的对话来回答我的问题，并在合理的地方插入标点符号"
  api_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
  api_key: 'yourapikey' # default=os.getenv("DASHSCOPE_API_KEY")
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| LLMOpenAICompatible.model_name | qwen-plus | 模型名称 |
| LLMOpenAICompatible.system_prompt | | 默认系统 prompt |
| LLMOpenAICompatible.api_url | | 模型 API URL |
| LLMOpenAICompatible.api_key | | 模型 API Key |

> [!TIP]
> 系统默认会获取项目当前目录下的 `.env` 文件用来获取环境变量。
