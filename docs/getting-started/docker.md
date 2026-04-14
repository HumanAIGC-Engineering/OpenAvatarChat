# Docker 部署

容器化运行：容器依赖 NVIDIA 容器环境，在准备好支持 GPU 的 Docker 环境后即可构建和启动。

> [!Note]
> Docker 镜像内部使用与本地相同的 `install.py` 进行依赖安装，无需额外脚本。
> `Dockerfile` 基于 CUDA 12.8，使用 `install.py --all` 将所有 handler 依赖统一打包到镜像中。

## 前置条件

- NVIDIA GPU 及驱动（支持 CUDA 12.8）
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- Docker 20.10+ 且 Docker Compose V2

## 构建镜像

```bash
# 克隆项目并进入目录
git clone https://github.com/HumanAIGC-Engineering/OpenAvatarChat.git && cd OpenAvatarChat

# 下载所有子模块
git submodule update --init --recursive --depth 1

# 下载所有 handler 所需的模型
uv run scripts/download_models.py --all

# 构建镜像
bash build_cuda128.sh
```

## 配置环境变量

如需使用百炼 API（用于 LLM 和 CosyVoice TTS），在项目根目录创建 `.env` 文件：

```bash
echo "DASHSCOPE_API_KEY=sk-xxxxx" > .env
```

## 运行容器

使用 `run_docker_cuda128.sh` 脚本启动，通过 `--config` 指定不同的数字人配置：

```bash
# LiteAvatar（轻量数字人，默认配置）
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml

# LAM（3D 数字人）
bash run_docker_cuda128.sh --config config/chat_with_lam.yaml

# MuseTalk（视频驱动数字人）
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml

# FlashHead（高质量数字人，GPU 资源消耗较大）
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml
```

启动成功后访问 `https://localhost:8282` 进入对话界面。

> [!Note]
> - 使用 MuseTalk 配置时，脚本会自动添加 `PYTORCH_JIT=0` 环境变量。
> - FlashHead 和 MuseTalk 的 `concurrent_limit` 为 1，GPU 占用较高。
> - 配置文件通过 volume 挂载到容器内，可在 `config/` 目录下自行修改。

## Docker Compose

支持使用 Docker Compose 一次性拉起 Open Avatar Chat 服务和 coturn 服务。

> [!Note]
> 在构建完成 `open-avatar-chat:latest` 之后，可以修改项目根目录下 `docker-compose.yml` 中的 `command` 字段来切换配置文件，默认为 `chat_with_openai_compatible_bailian_cosyvoice.yaml`。

```bash
# 拉起服务
docker compose up

# 关闭服务
docker compose down
```

## 支持的数字人配置

| 配置文件 | 数字人类型 | 说明 |
|---------|-----------|------|
| `chat_with_openai_compatible_bailian_cosyvoice.yaml` | LiteAvatar | 轻量级，资源占用低 |
| `chat_with_lam.yaml` | LAM | 3D 数字人，使用 WebSocket 客户端 |
| `chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml` | MuseTalk | 视频驱动，需要 `PYTORCH_JIT=0` |
| `chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml` | FlashHead | 高质量生成，GPU 占用较高 |

各配置文件还有对应的全双工（duplex）版本，可在 `config/` 目录下查看。
