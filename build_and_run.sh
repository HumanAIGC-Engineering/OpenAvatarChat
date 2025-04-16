#!/usr/bin/env bash
# 初始化变量
CONFIG_PATH=""

# 解析参数的循环
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -config | --config )
            CONFIG_PATH="$2"
            shift 2 # 跳过当前参数及后一个参数
            ;;
    esac
done

echo "${CONFIG_PATH}"

docker build \
    --build-arg CONFIG_FILE=${CONFIG_PATH}  \
    -t open-avatar-chat:0.0.1 . 
docker run --rm --gpus all -it --name open-avatar-chat \
    -v `pwd`/build:/root/open-avatar-chat/build \
    -v `pwd`/models:/root/open-avatar-chat/models \
    -v `pwd`/ssl_certs:/root/open-avatar-chat/ssl_certs \
    -v `pwd`/config:/root/open-avatar-chat/config \
    -p 8282:8282 \
    open-avatar-chat:0.0.1 \
    --config ${CONFIG_PATH}
