# Smart Turn VAD Handler (Duplex Mode)

Duplex configs use the Smart Turn model for end-of-utterance detection.

## Model Dependencies

```bash
uv run scripts/download_models.py --handler smart_turn_eou
```

## Configuration

```yaml
SmartTurnEOU:
  module: vad/smart_turn_eou/eou_handler_smart_turn
  threshold: 0.8
  model_path: "models/smart_turn/smart-turn-v3.1-cpu.onnx"
```
