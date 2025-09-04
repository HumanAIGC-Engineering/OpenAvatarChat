# Docker 构建指南

本文档介绍如何构建和部署 OpenAvatarChat 的 Docker 镜像。

## 🏗️ 构建方式

### 1. GitHub Actions 自动构建（推荐）

#### 手动触发构建
1. 进入 GitHub 仓库页面
2. 点击 `Actions` 标签
3. 选择 `Build Docker Images` workflow
4. 点击 `Run workflow` 按钮
5. 配置构建参数：
   - **Image Type**: 选择要构建的镜像类型
     - `avatar`: 仅构建 Avatar (Dify) 镜像
     - `lam`: 仅构建 LAM (Dify) 镜像  
     - `both`: 构建两个镜像（默认）
   - **Tag Suffix**: 镜像标签后缀（如 `v1.0.0`, `latest`）
   - **Push to Registry**: 是否推送到 GitHub Container Registry

#### 构建产物
构建成功后，镜像将推送到 GitHub Container Registry：
- `ghcr.io/your-username/your-repo-avatar:tag`
- `ghcr.io/your-username/your-repo-lam:tag`

### 2. 本地构建

#### 使用构建脚本（推荐）
```bash
# 给脚本执行权限
chmod +x scripts/build-docker.sh

# 构建两个镜像
./scripts/build-docker.sh

# 仅构建 Avatar 镜像
./scripts/build-docker.sh avatar

# 仅构建 LAM 镜像  
./scripts/build-docker.sh lam

# 构建并指定标签
./scripts/build-docker.sh both v1.0.0

# 使用自定义 registry
REGISTRY=docker.io ./scripts/build-docker.sh
```

#### 使用 Docker Compose
```bash
# 构建并启动 Avatar 服务
docker-compose --profile avatar up -d

# 构建并启动 LAM 服务
docker-compose --profile lam up -d

# 构建并启动所有服务
docker-compose --profile all up -d

# 仅构建镜像（不启动）
docker-compose build avatar-dify
docker-compose build lam-dify
```

#### 手动 Docker 构建
```bash
# 构建 Avatar 镜像
docker build \
  --build-arg CONFIG_FILE=config/chat_with_dify.yaml \
  -t open-avatar-chat-avatar:latest \
  .

# 构建 LAM 镜像
docker build \
  --build-arg CONFIG_FILE=config/chat_with_lam_dify.yaml \
  -t open-avatar-chat-lam:latest \
  .
```

## 🚀 运行镜像

### 使用 Docker Compose（推荐）
```bash
# 启动 Avatar 服务（端口 8282）
docker-compose --profile avatar up -d

# 启动 LAM 服务（端口 8283）
docker-compose --profile lam up -d

# 查看日志
docker-compose logs -f avatar-dify
docker-compose logs -f lam-dify

# 停止服务
docker-compose --profile avatar down
docker-compose --profile lam down
```

### 使用 Docker 命令
```bash
# 运行 Avatar 镜像
docker run --rm --gpus all -it \
  --name avatar-dify \
  --network=host \
  -v $(pwd)/build:/root/open-avatar-chat/build \
  -v $(pwd)/models:/root/open-avatar-chat/models \
  -v $(pwd)/ssl_certs:/root/open-avatar-chat/ssl_certs \
  -v $(pwd)/config:/root/open-avatar-chat/config \
  -p 8282:8282 \
  open-avatar-chat-avatar:latest \
  --config config/chat_with_dify.yaml

# 运行 LAM 镜像
docker run --rm --gpus all -it \
  --name lam-dify \
  --network=host \
  -v $(pwd)/build:/root/open-avatar-chat/build \
  -v $(pwd)/models:/root/open-avatar-chat/models \
  -v $(pwd)/ssl_certs:/root/open-avatar-chat/ssl_certs \
  -v $(pwd)/config:/root/open-avatar-chat/config \
  -p 8283:8282 \
  open-avatar-chat-lam:latest \
  --config config/chat_with_lam_dify.yaml
```

## 📋 镜像说明

### Avatar (Dify) 镜像
- **配置文件**: `config/chat_with_dify.yaml`
- **数字人类型**: LiteAvatar (2D)
- **LLM**: Dify Chatflow
- **TTS**: Edge TTS
- **并发支持**: 1路
- **适用场景**: 轻量级部署，快速体验

### LAM (Dify) 镜像  
- **配置文件**: `config/chat_with_lam_dify.yaml`
- **数字人类型**: LAM (3D)
- **LLM**: Dify Chatflow
- **TTS**: Edge TTS
- **并发支持**: 5路
- **适用场景**: 高质量 3D 数字人，支持多用户

## 🔧 环境要求

### 系统要求
- Docker 20.10+
- Docker Compose 2.0+
- NVIDIA Docker Runtime（GPU 支持）
- CUDA 12.2+ 兼容的 GPU

### 资源要求
- **Avatar 镜像**: 
  - GPU 内存: 4GB+
  - 系统内存: 8GB+
- **LAM 镜像**:
  - GPU 内存: 8GB+
  - 系统内存: 16GB+

## 🐛 故障排除

### 常见问题

1. **GPU 不可用**
   ```bash
   # 检查 NVIDIA Docker 支持
   docker run --rm --gpus all nvidia/cuda:12.2-base-ubuntu22.04 nvidia-smi
   ```

2. **端口冲突**
   - Avatar 服务默认端口: 8282
   - LAM 服务默认端口: 8283
   - 可通过修改 docker-compose.yml 调整端口映射

3. **模型下载失败**
   - 确保网络连接正常
   - 检查 models 目录挂载是否正确
   - 查看容器日志获取详细错误信息

4. **SSL 证书问题**
   - 确保 ssl_certs 目录存在
   - 运行 `scripts/create_ssl_certs.sh` 生成自签名证书

### 查看日志
```bash
# Docker Compose 日志
docker-compose logs -f [service-name]

# Docker 容器日志
docker logs -f [container-name]
```

## 📚 相关文档

- [项目主 README](../README.md)
- [配置说明](../README.md#配置说明)
- [常见问题](../docs/FAQ.md)
- [部署需求](../README.md#相关部署需求)
