CONFIG_PATH=""

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -config | --config )
            CONFIG_PATH="$2"
            shift 2
            ;;
    esac
done

# Determine config file path
CONFIG_FILE="${CONFIG_PATH:-config/chat_with_openai_compatible_bailian_cosyvoice.yaml}"

# Check for AvatarMusetalk module and set environment variables（if Musetalk is used, set PYTORCH_JIT=0）
if grep -q "AvatarMusetalk:" "$CONFIG_FILE" 2>/dev/null && grep -q "module: avatar/musetalk/avatar_handler_musetalk" "$CONFIG_FILE" 2>/dev/null; then
    echo "Detected AvatarMusetalk module, adding PYTORCH_JIT=0 environment variable"
    ENV_VARS="-e PYTORCH_JIT=0"
else
    echo "No AvatarMusetalk module detected in config, skipping PYTORCH_JIT environment variable"
fi

docker run --rm --gpus all -it --name open-avatar-chat \
    --network=host \
    $ENV_VARS \
    -v `pwd`/build:/root/open-avatar-chat/build \
    -v `pwd`/models:/root/open-avatar-chat/models \
    -v `pwd`/ssl_certs:/root/open-avatar-chat/ssl_certs \
    -v `pwd`/config:/root/open-avatar-chat/config \
    -v `pwd`/.env:/root/open-avatar-chat/.env \
    -v `pwd`/models/musetalk/s3fd-619a316812/:/root/.cache/torch/hub/checkpoints/ \
    -v `pwd`/exp:/root/open-avatar-chat/exp \
    -v `pwd`/resource:/root/open-avatar-chat/resource \
    -p 8282:8282 \
    open-avatar-chat:latest \
    --config ${CONFIG_PATH:-config/chat_with_openai_compatible_bailian_cosyvoice.yaml}