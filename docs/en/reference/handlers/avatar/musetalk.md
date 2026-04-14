# MuseTalk Avatar Handler

Integrates MuseTalk 1.5 with custom avatar support.

## Model Dependencies

```bash
uv run scripts/download_models.py --handler musetalk
```

> [!WARNING]
> MuseTalk uses relative paths for models. Do not change the download location.

## Configuration

```yaml
Avatar_MuseTalk:
  module: avatar/musetalk/avatar_handler_musetalk
  fps: 20
  batch_size: 2
  avatar_video_path: "src/handlers/avatar/musetalk/MuseTalk/data/video/sun.mp4"
  avatar_model_dir: "models/musetalk/avatar_model"
  force_create_avatar: false
```

## Run

```bash
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
uv run scripts/download_models.py --handler musetalk
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```
