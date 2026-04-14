# FlashHead 数字人 Handler

集成 [SoulX-FlashHead](https://github.com/Soul-AILab/SoulX-FlashHead) 项目的 Lite 模式，基于扩散模型的实时流式说话头生成。支持单张图像驱动，在单 RTX 4090 上可达 96FPS 或 3 路并发 25+ FPS。

## 依赖模型

```bash
uv run scripts/download_models.py --handler flashhead
```

<details>
<summary>手动下载</summary>

* **Soul-AILab/SoulX-FlashHead-1_3B** [HuggingFace](https://huggingface.co/Soul-AILab/SoulX-FlashHead-1_3B)
```bash
pip install "huggingface_hub[cli]"
huggingface-cli download Soul-AILab/SoulX-FlashHead-1_3B --local-dir ./models/SoulX-FlashHead-1_3B
```

* **facebook/wav2vec2-base-960h**（与 LAM 共享）
```bash
git clone --depth 1 https://huggingface.co/facebook/wav2vec2-base-960h ./models/wav2vec2-base-960h
```

</details>

## 配置参数

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
  debug: false
```

* **条件图像**：通过 `cond_image_path` 指定人脸图像
* **模型类型**：`lite`（推荐）或 `pro`
* **人脸裁剪**：设置 `use_face_crop: true` 可自动检测并裁剪

> [!Note]
> FlashHead 依赖 `flash-attn`，`install.py` 会自动编译安装。
