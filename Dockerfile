FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04
LABEL authors="HumanAIGC-Engineering"

ARG CONFIG_FILE=config/chat_with_minicpm.yaml

ENV DEBIAN_FRONTEND=noninteractive

# Use Tsinghua University APT mirrors
# RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
#     sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# Update package list and install required dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.11 python3.11-dev python3.11-venv python3.11-distutils python3-pip git libgl1 libglib2.0-0

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 && \
    python3.11 -m ensurepip --upgrade && \
    python3.11 -m pip install --upgrade pip

ARG WORK_DIR=/root/open-avatar-chat
WORKDIR $WORK_DIR

# Set UV cache and temp directories to avoid disk space issues
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV TMPDIR=/tmp
ENV TEMP=/tmp
ENV TMP=/tmp
ENV PIP_CACHE_DIR=/tmp/pip-cache
ENV PYTHONPYCACHEPREFIX=/tmp/pycache

# Create temp directory with proper permissions
RUN mkdir -p /tmp/uv-cache /tmp/pip-cache /tmp/pycache && \
    chmod 1777 /tmp

# Install core dependencies (with space optimization)
COPY ./install.py $WORK_DIR/install.py
COPY ./pyproject.toml $WORK_DIR/pyproject.toml
COPY ./src/third_party $WORK_DIR/src/third_party
RUN echo "=== Installing UV and setting up environment ===" && \
    pip install uv && \
    uv venv --python 3.11.11 && \
    echo "=== Pre-core-install cleanup ===" && \
    rm -rf /tmp/* /var/tmp/* && \
    mkdir -p /tmp /var/tmp && \
    chmod 1777 /tmp /var/tmp && \
    echo "=== Installing core dependencies ===" && \
    UV_NO_CACHE=1 uv sync --no-install-workspace && \
    echo "=== Post-core-install cleanup ===" && \
    # Clean up after core installation
    uv cache clean && \
    rm -rf /root/.cache/pip/* /tmp/* /var/tmp/* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./src $WORK_DIR/src

# Copy script files (must be copied before installing config dependencies)
ADD ./scripts $WORK_DIR/scripts

# Execute pre-config installation script
RUN echo "Using config file: ${CONFIG_FILE}"
COPY $CONFIG_FILE /tmp/build_config.yaml
RUN chmod +x $WORK_DIR/scripts/pre_config_install.sh && \
    $WORK_DIR/scripts/pre_config_install.sh --config /tmp/build_config.yaml

# Install config dependencies (with space optimization)
RUN echo "=== Pre-installation cleanup ===" && \
    # Aggressive cleanup before installation
    rm -rf /tmp/* /var/tmp/* /var/cache/* && \
    mkdir -p /tmp /var/tmp && \
    chmod 1777 /tmp /var/tmp && \
    df -h && \
    echo "=== Starting dependency installation ===" && \
    UV_NO_CACHE=1 uv run install.py \
    --config /tmp/build_config.yaml \
    --uv \
    --skip-core && \
    echo "=== Post-installation cleanup ===" && \
    # Clean up uv cache to free space
    uv cache clean && \
    rm -rf /root/.cache/pip/* /tmp/* /var/tmp/* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    df -h

# Execute post-config installation script
RUN chmod +x $WORK_DIR/scripts/post_config_install.sh && \
    $WORK_DIR/scripts/post_config_install.sh --config /tmp/build_config.yaml && \
    rm /tmp/build_config.yaml && \
    # Final cleanup
    uv cache clean && \
    rm -rf /root/.cache/pip/* /tmp/* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD ./resource $WORK_DIR/resource
ADD ./.env* $WORK_DIR/

WORKDIR $WORK_DIR
ENTRYPOINT ["uv", "run", "src/demo.py"]
