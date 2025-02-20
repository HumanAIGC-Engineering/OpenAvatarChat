#!/usr/bin/env bash

docker build -t open-avatar-chat:0.0.1 .
docker run --rm --gpus all -it --name open-avatar-chat \
    -v `pwd`/models:/root/open-avatar-chat/models \
    -v `pwd`/ssl_certs:/root/open-avatar-chat/ssl_certs \
    -v `pwd`/config:/root/open-avatar-chat/config \
    -p 8282:8282 \
    open-avatar-chat:0.0.1
