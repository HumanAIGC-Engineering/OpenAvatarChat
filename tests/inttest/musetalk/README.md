# MuseTalk 离线合成集成测试

本目录用于存放 **离线合成** 的测试输入与输出，与线上实时推理共用同一份 YAML 配置（见下文）。

## 目录结构

```
tests/inttest/musetalk/
├── README.md                 # 本说明
├── assets/
│   └── audio/                # 测试用音频（可提交小样本）
│       └── test-audio-1.wav
├── outputs/
│   └── offline/              # 离线合成 MP4 输出（默认不提交，见 .gitignore）
└── run_offline_smoke.sh      # 一键冒烟脚本（需在项目根目录执行）
```

说明：

- **输入**：仅测试素材放在 `assets/audio/`，避免与 `models/musetalk/avatar_model/` 下的 **数字人缓存数据**（latent、mask 等）混在一起。
- **输出**：统一写到 `outputs/offline/`，便于清理与自动化忽略大文件。

## 运行方式

在项目根目录 `Inner-OpenAvatarChat/` 下执行：

```bash
./tests/inttest/musetalk/run_offline_smoke.sh
```

或手动：

```bash
cd /path/to/Inner-OpenAvatarChat
python src/handlers/avatar/musetalk/musetalk_algo.py \
  --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \
  --audio_path tests/inttest/musetalk/assets/audio/test-audio-1.wav \
  --output_dir tests/inttest/musetalk/outputs/offline \
  --batch_size 8
```

依赖：

- 项目 Python 环境（推荐在项目根目录使用 `uv run`，脚本已优先调用 `uv run python`）
- GPU（CUDA）、已下载的 `models/musetalk/`、系统已安装 `ffmpeg`

成功后在 `outputs/offline/` 下生成 `test-audio-1_offline.mp4`（该目录下生成物默认被 git 忽略，见 `outputs/offline/.gitignore`）。

## 与配置的关系

`avatar_model_dir` 等仍由 YAML 中的 `AvatarMusetalk` 段指定（默认 `models/musetalk/avatar_model`），仅 **测试音频路径** 与 **本次 MP4 输出路径** 使用本目录下的 `assets` / `outputs`。
