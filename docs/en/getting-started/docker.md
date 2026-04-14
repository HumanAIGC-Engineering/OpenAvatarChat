# Docker Deployment

The container requires the NVIDIA container runtime. After preparing a GPU-capable Docker environment, you can build and start.

> [!Note]
> The Docker image uses the same `install.py` internally for dependency installation.
> The `Dockerfile` is based on CUDA 12.8 and uses `install.py --all` to bundle all handler dependencies into the image.

## Prerequisites

- NVIDIA GPU with driver supporting CUDA 12.8
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- Docker 20.10+ with Docker Compose V2

## Build the Image

```bash
# Clone the project
git clone https://github.com/HumanAIGC-Engineering/OpenAvatarChat.git && cd OpenAvatarChat

# Download all submodules
git submodule update --init --recursive --depth 1

# Download all handler models
uv run scripts/download_models.py --all

# Build the image
bash build_cuda128.sh
```

## Configure Environment Variables

If using the Bailian API (for LLM and CosyVoice TTS), create a `.env` file in the project root:

```bash
echo "DASHSCOPE_API_KEY=sk-xxxxx" > .env
```

## Run the Container

Use `run_docker_cuda128.sh` to start the container with different avatar configurations via `--config`:

```bash
# LiteAvatar (lightweight avatar, default)
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice.yaml

# LAM (3D avatar)
bash run_docker_cuda128.sh --config config/chat_with_lam.yaml

# MuseTalk (video-driven avatar)
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml

# FlashHead (high-quality avatar, GPU-intensive)
bash run_docker_cuda128.sh --config config/chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml
```

Once started, visit `https://localhost:8282` to access the chat interface.

> [!Note]
> - When using the MuseTalk config, the run script automatically sets `PYTORCH_JIT=0`.
> - FlashHead and MuseTalk have `concurrent_limit` set to 1 due to high GPU usage.
> - Config files are mounted into the container via volumes and can be modified in the `config/` directory.

## Docker Compose

Docker Compose can be used to start both the Open Avatar Chat service and the coturn service together.

> [!Note]
> After building the `open-avatar-chat:latest` image, you can modify the `command` field in `docker-compose.yml` to switch the config file. The default is `chat_with_openai_compatible_bailian_cosyvoice.yaml`.

```bash
# Start services
docker compose up

# Stop services
docker compose down
```

## Supported Avatar Configurations

| Config File | Avatar Type | Notes |
|------------|-------------|-------|
| `chat_with_openai_compatible_bailian_cosyvoice.yaml` | LiteAvatar | Lightweight, low resource usage |
| `chat_with_lam.yaml` | LAM | 3D avatar, uses WebSocket client |
| `chat_with_openai_compatible_bailian_cosyvoice_musetalk.yaml` | MuseTalk | Video-driven, requires `PYTORCH_JIT=0` |
| `chat_with_openai_compatible_bailian_cosyvoice_flashhead.yaml` | FlashHead | High-quality generation, GPU-intensive |

Each config also has a corresponding duplex version available in the `config/` directory.
