FROM nvidia/cuda:12.2.2-cudnn8-devel-ubuntu22.04
LABEL authors="HumanAIGC-Engineering"

ARG CONFIG_FILE=config/chat_with_minicpm.yaml

ENV DEBIAN_FRONTEND=noninteractive

# 替换为清华大学的APT源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 更新包列表并安装必要的依赖
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

#安装核心依赖
COPY ./install.py $WORK_DIR/install.py
COPY ./pyproject.toml $WORK_DIR/pyproject.toml
COPY ./src/third_party $WORK_DIR/src/third_party
RUN pip install uv && \
    uv venv --python 3.11.11 && \
    uv sync --no-install-workspace

ADD ./src $WORK_DIR/src

# 复制脚本文件（需要在安装config依赖前就复制，以便使用）
ADD ./scripts $WORK_DIR/scripts

#安装config依赖前的脚本执行
RUN echo "Using config file: ${CONFIG_FILE}"
COPY $CONFIG_FILE /tmp/build_config.yaml
RUN chmod +x $WORK_DIR/scripts/pre_config_install.sh && \
    $WORK_DIR/scripts/pre_config_install.sh --config /tmp/build_config.yaml

#安装config依赖
RUN uv run install.py \
    --config /tmp/build_config.yaml \
    --uv \
    --skip-core

#安装config依赖后的脚本执行
RUN chmod +x $WORK_DIR/scripts/post_config_install.sh && \
    $WORK_DIR/scripts/post_config_install.sh --config /tmp/build_config.yaml && \
    rm /tmp/build_config.yaml

ADD ./resource $WORK_DIR/resource
ADD ./.env* $WORK_DIR/

WORKDIR $WORK_DIR
ENTRYPOINT ["uv", "run", "src/demo.py"]
