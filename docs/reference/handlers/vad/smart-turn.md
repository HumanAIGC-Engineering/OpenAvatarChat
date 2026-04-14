# Smart Turn VAD Handler（双工模式）

双工配置（`*_duplex.yaml`）使用 Smart Turn 模型进行端点检测（End-of-Utterance）。

## 依赖模型

```bash
uv run scripts/download_models.py --handler smart_turn_eou
```

模型将下载到 `models/smart_turn/` 目录。

## 配置参数

```yaml
SmartTurnEOU:
  module: vad/smart_turn_eou/eou_handler_smart_turn
  threshold: 0.8
  model_path: "models/smart_turn/smart-turn-v3.1-cpu.onnx"
```
