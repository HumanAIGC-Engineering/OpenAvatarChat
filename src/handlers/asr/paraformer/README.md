# 阿里云Paraformer ASR处理器

这个处理器集成了阿里云的Paraformer实时语音识别API，支持多种语言和实时识别功能。

## 功能特性

- 支持多种Paraformer模型（paraformer-realtime-v2, paraformer-realtime-8k-v2等）
- 实时语音识别，支持中间结果输出
- 支持中文、英文、日语、韩语等多种语言
- 自动标点符号预测和逆文本正则化
- 支持情感识别（仅限paraformer-realtime-8k-v2模型）
- 支持语义断句检测

## 配置参数

```yaml
Paraformer:
  enabled: True
  module: asr/paraformer/asr_handler_paraformer
  model_name: "paraformer-realtime-v2"  # 模型名称
  api_key: "your_api_key_here"          # 阿里云API密钥
  sample_rate: 16000                    # 采样率
  format: "pcm"                         # 音频格式
  enable_intermediate_result: True      # 启用中间结果
  enable_punctuation_prediction: True   # 启用标点符号预测
  enable_inverse_text_normalization: True  # 启用逆文本正则化
  language_hints: ["zh", "en"]          # 语言提示
  max_sentence_silence: 800             # 最大句子静默时间(ms)
  enable_emotion_recognition: False     # 启用情感识别
  enable_semantic_sentence_detection: False  # 启用语义断句检测
```

## 支持的模型

| 模型名称 | 适用场景 | 采样率 | 支持语言 |
|---------|---------|--------|---------|
| paraformer-realtime-v2 | 直播、会议等场景 | 任意 | 中文、英文、日语、韩语、德语、法语、俄语 |
| paraformer-realtime-8k-v2 | 电话客服、语音信箱等 | 8kHz | 中文 |
| paraformer-realtime-v1 | 直播、会议等场景 | 16kHz | 中文 |
| paraformer-realtime-8k-v1 | 电话客服、语音信箱等 | 8kHz | 中文 |

## 环境要求

1. 安装依赖：
```bash
pip install dashscope>=1.14.0
```

2. 设置API密钥：
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

## 使用方法

1. 在配置文件中启用Paraformer处理器
2. 设置正确的API密钥
3. 根据需要调整其他参数
4. 重启服务

## 注意事项

- 确保API密钥有效且有足够的配额
- 音频数据会自动转换为16位PCM格式
- 支持实时流式识别，会输出中间结果
- 情感识别功能仅限paraformer-realtime-8k-v2模型
- 语义断句检测默认为关闭状态

## 故障排查

1. **无法识别语音**：
   - 检查API密钥是否正确
   - 确认音频格式和采样率设置
   - 检查网络连接

2. **识别结果为空**：
   - 确认音频质量
   - 检查语言设置是否匹配
   - 尝试调整max_sentence_silence参数

3. **连接错误**：
   - 检查网络连接
   - 确认API服务状态
   - 检查防火墙设置