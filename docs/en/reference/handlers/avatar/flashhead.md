# FlashHead Avatar Handler

Integrates [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead) Lite mode. Achieves 96 FPS on RTX 4090 or 3 concurrent sessions at 25+ FPS.

## Model Dependencies

```bash
uv run scripts/download_models.py --handler flashhead
```

## Configuration

```yaml
FlashHead:
  module: avatar/flashhead/avatar_handler_flashhead
  ckpt_dir: "models/SoulX-FlashHead-1_3B"
  wav2vec_dir: "models/wav2vec2-base-960h"
  model_type: "lite"
  cond_image_path: "resource/avatar/flashhead/default.png"
  fps: 25
  base_seed: 42
  use_face_crop: false
```

> [!Note]
> FlashHead depends on `flash-attn`. `install.py` compiles it automatically.
