# MuseTalk 数字人 Handler

集成 MuseTalk 1.5，支持自定义形象。

## 依赖模型

```bash
uv run scripts/download_models.py --handler musetalk
```

> [!WARNING]
> MuseTalk 使用相对路径加载模型，**不要修改模型的下载位置**。

## 配置参数

```yaml
Avatar_MuseTalk:
  module: avatar/musetalk/avatar_handler_musetalk
  fps: 20
  batch_size: 2
  avatar_video_path: "src/handlers/avatar/musetalk/MuseTalk/data/video/sun.mp4"
  avatar_model_dir: "models/musetalk/avatar_model"
  force_create_avatar: false
  debug: false
```

* **形象选择**：通过 `avatar_video_path` 参数修改
* **帧率**：建议 `fps: 20`
* **batch_size**：最小为 2

## 数字人模型下载工具

```bash
# 下载指定模型
uv run scripts/download_avatar_model.py -m "20250612/P1rcvIW8H6kvcYWNkEnBWPfg"
# 查看已下载列表
uv run scripts/download_avatar_model.py -d
```

## 运行

```bash
uv run install.py --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
uv run scripts/download_models.py --handler musetalk
uv run src/demo.py --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml
```
