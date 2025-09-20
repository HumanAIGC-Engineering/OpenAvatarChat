#!/usr/bin/env bash
CONFIG_PATH=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -config | --config )
            CONFIG_PATH="$2"
            shift 2
            ;;
    esac
done

echo "${CONFIG_PATH}"

#docker build \
#    --build-arg CONFIG_FILE=${CONFIG_PATH}  \
#    -t open-avatar-chat:0.0.1 . 
docker run -d --restart=unless-stopped --name open-avatar-chat \
    --network=host \
    -e PIP_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/" \
    -e UV_INDEX_URL="https://mirrors.aliyun.com/pypi/simple/" \
    -v `pwd`/build:/root/open-avatar-chat/build \
    -v `pwd`/models:/root/open-avatar-chat/models \
    -v `pwd`/ssl_certs:/root/open-avatar-chat/ssl_certs \
    -v `pwd`/config:/root/open-avatar-chat/config \
    -v `pwd`/src:/root/open-avatar-chat/src \
    -p 8282:8282 \
    open-avatar-chat:0.0.1 \
    --config ${CONFIG_PATH}
