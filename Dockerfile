FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04

# Re-declare ARGs after FROM to make them available in subsequent layers
ARG WORK_DIR=/root/open-avatar-chat

# Image metadata with dynamic version
LABEL authors="HumanAIGC-Engineering"


# Environment variables for optimized build and runtime
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    UV_COMPILE_BYTECODE=0 \
    WORK_DIR=$WORK_DIR


# =============================================================================
# System Dependencies Installation
# =============================================================================
# Use Tsinghua University mirrors for faster package downloads in China
# Install latest Python 3.11.x and essential system libraries for the application
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        # Python 3.11 and development tools (latest available 3.11.x version)
        python3.11 \
        python3.11-dev \
        python3.11-venv \
        python3.11-distutils \
        python3-pip \
        # Version control and build tools
        git \
        git-lfs \
        build-essential \
        # Graphics and image libraries (required for OpenCV/PIL)
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libgomp1 \
        # Audio processing libraries (required for librosa, soundfile, torchaudio)
        libsndfile1 \
        ffmpeg \
        sox \
        libsox-dev \
        # Multimedia codec libraries (required for video processing)
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        # Additional utilities
        curl \
        ca-certificates && \
    # Configure git lfs
    git lfs install && \
    # Clean up package manager cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Set Python 3.11 as default python3 with higher priority
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 && \
    update-alternatives --set python3 /usr/bin/python3.11 && \
    # Upgrade pip to latest version with optimizations
    python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install --no-cache-dir --upgrade pip setuptools wheel

# Set working directory for the application
WORKDIR $WORK_DIR

# =============================================================================
# Python Dependencies and Virtual Environment Setup
# =============================================================================
# Copy dependency metadata files first for Docker layer caching.
# Only pyproject.toml files are copied here (not full source) so that
# code-only changes do not invalidate the expensive dependency layer.
COPY ./install.py $WORK_DIR/install.py
COPY ./pyproject.toml $WORK_DIR/pyproject.toml
COPY ./src/__init__.py $WORK_DIR/src/__init__.py
COPY ./src/engine_utils $WORK_DIR/src/engine_utils
COPY ./src/handlers/tts/edgetts/pyproject.toml $WORK_DIR/src/handlers/tts/edgetts/pyproject.toml
COPY ./src/handlers/tts/cosyvoice/pyproject.toml $WORK_DIR/src/handlers/tts/cosyvoice/pyproject.toml
COPY ./src/handlers/tts/bailian_tts/pyproject.toml $WORK_DIR/src/handlers/tts/bailian_tts/pyproject.toml
COPY ./src/handlers/avatar/liteavatar/pyproject.toml $WORK_DIR/src/handlers/avatar/liteavatar/pyproject.toml
COPY ./src/handlers/avatar/lam/pyproject.toml $WORK_DIR/src/handlers/avatar/lam/pyproject.toml
COPY ./src/handlers/avatar/musetalk/pyproject.toml $WORK_DIR/src/handlers/avatar/musetalk/pyproject.toml
COPY ./src/handlers/avatar/flashhead/pyproject.toml $WORK_DIR/src/handlers/avatar/flashhead/pyproject.toml
COPY ./src/handlers/vad/silerovad/pyproject.toml $WORK_DIR/src/handlers/vad/silerovad/pyproject.toml
COPY ./src/handlers/vad/smart_turn_eou/pyproject.toml $WORK_DIR/src/handlers/vad/smart_turn_eou/pyproject.toml
COPY ./src/handlers/asr/sensevoice/pyproject.toml $WORK_DIR/src/handlers/asr/sensevoice/pyproject.toml
COPY ./src/handlers/asr/bailian_asr/pyproject.toml $WORK_DIR/src/handlers/asr/bailian_asr/pyproject.toml
COPY ./src/third_party $WORK_DIR/src/third_party

# Install uv and create virtual environment
RUN pip install --no-cache-dir uv && \
    uv venv --python /usr/bin/python3.11 --seed

# Install all dependencies via install.py (handles version conflict
# resolution, flash-attn compilation, etc. automatically)
RUN uv run install.py --all

# Replace onnxruntime with GPU variant (Docker-specific, needs CUDA runtime)
RUN uv pip uninstall onnxruntime onnxruntime-gpu; \
    uv pip install --no-cache-dir onnxruntime-gpu==1.20.2

# =============================================================================
# Application Source Code and Configuration
# =============================================================================
COPY ./scripts $WORK_DIR/scripts
COPY ./src $WORK_DIR/src

# =============================================================================
# Runtime Assets
# =============================================================================
COPY ./resource $WORK_DIR/resource
# =============================================================================
# Final Cleanup and Optimization
# =============================================================================
# Clean up build artifacts and temporary files to reduce image size
RUN rm -rf /root/.cache/uv/* /tmp/* /var/tmp/*

ARG BUILD_VERSION=dev
ARG BUILD_DATE=""
ENV APP_VERSION=${BUILD_VERSION} \
    BUILD_DATE=${BUILD_DATE} \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility,video

# =============================================================================
# Container Entry Point
# =============================================================================
# Use uv to run the application with proper virtual environment
ENTRYPOINT ["uv", "run", "--no-sync", "src/demo.py"]
