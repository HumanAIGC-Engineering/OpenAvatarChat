# LiteAvatar Avatar Handler

2D avatar using LiteAvatar. 100 avatar assets available on [LiteAvatarGallery](https://modelscope.cn/models/HumanAIGC-Engineering/LiteAvatarGallery).

## Model Dependencies

```bash
uv run scripts/download_models.py --handler liteavatar
```

## Configuration

```yaml
LiteAvatar:
  module: avatar/liteavatar/avatar_handler_liteavatar
  avatar_name: 20250408/sample_data
  fps: 25
  use_gpu: true
```

| Parameter | Default | Description |
|---|---|---|
| LiteAvatar.avatar_name | 20250408/sample_data | Avatar data name |
| LiteAvatar.fps | 25 | Frame rate |
| LiteAvatar.enable_fast_mode | False | Low-latency mode |
| LiteAvatar.use_gpu | True | Use GPU |

## Multi-Session

Set `default.chan_engine.concurrent_limit` to enable. Each session uses ~3GB VRAM.
