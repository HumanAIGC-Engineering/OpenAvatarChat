FROM ubuntu:22.04
LABEL authors="HumanAIGC-Engineering"

ENV DEBIAN_FRONTEND=noninteractive

# 替换为清华大学的APT源
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 更新包列表并安装必要的依赖
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get install -y python3.10 python3.10-dev python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# 安装PyTorch GPU版本
RUN pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124

ARG WORK_DIR=/root/open-avatar-chat
WORKDIR $WORK_DIR
ADD ./requirements.txt $WORK_DIR/requirements.txt
ADD ./src $WORK_DIR/src
ADD ./resource $WORK_DIR/resource

RUN pip install -r $WORK_DIR/requirements.txt

ENTRYPOINT ["python3", "src/demo.py"]
