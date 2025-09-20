FROM crpi-d7893jmckneooooz.cn-beijing.personal.cr.aliyuncs.com/cxzy/nvidia_cuda:12.2.2-cudnn8-devel-ubuntu22.04
LABEL authors="HumanAIGC-Engineering"

ARG CONFIG_FILE=config/chat_with_minicpm.yaml
ARG PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/

ENV DEBIAN_FRONTEND=noninteractive

# Use Tsinghua University APT mirrors
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

RUN rm -f /etc/apt/sources.list.d/cuda*.list /etc/apt/sources.list.d/nvidia*.list || true

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

# Install core dependencies
COPY ./pyproject.toml $WORK_DIR/pyproject.toml

COPY ./src/third_party $WORK_DIR/src/third_party
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/root/.cache/pip \
    pip install -i ${PIP_INDEX_URL} uv && \
    uv venv && \
    uv sync --index-url ${PIP_INDEX_URL} --no-install-workspace

ENV VIRTUAL_ENV=$WORK_DIR/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./install.py $WORK_DIR/install.py
ADD ./src $WORK_DIR/src

# Copy script files (must be copied before installing config dependencies)
ADD ./scripts $WORK_DIR/scripts

# Execute pre-config installation script
RUN echo "Using config file: ${CONFIG_FILE}"
COPY $CONFIG_FILE /tmp/build_config.yaml

# Install config dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/root/.cache/pip \
    chmod +x $WORK_DIR/scripts/pre_config_install.sh && \
    $WORK_DIR/scripts/pre_config_install.sh --config /tmp/build_config.yaml && \
    export UV_INDEX_URL=${PIP_INDEX_URL} && \
    export PIP_INDEX_URL=${PIP_INDEX_URL} && \
    uv run install.py \
       --config /tmp/build_config.yaml \
       --uv \
       --skip-core

# Execute post-config installation script
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=cache,target=/root/.cache/pip \
    chmod +x $WORK_DIR/scripts/post_config_install.sh && \
    $WORK_DIR/scripts/post_config_install.sh --config /tmp/build_config.yaml && \
    rm /tmp/build_config.yaml

ADD ./resource $WORK_DIR/resource
ADD ./.env* $WORK_DIR/

WORKDIR $WORK_DIR
ENTRYPOINT ["uv", "run", "src/demo.py"]
