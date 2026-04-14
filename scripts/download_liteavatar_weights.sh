#!/bin/bash
set -e

LITE_AVATAR_DIR="src/handlers/avatar/liteavatar/algo/liteavatar"

# Ensure modelscope is available (needed by download_model.sh)
if ! command -v modelscope &> /dev/null; then
    echo "modelscope CLI not found, installing..."
    if command -v uv &> /dev/null && [ -d ".venv" ]; then
        uv pip install modelscope
    else
        pip install modelscope
    fi
fi

pushd "$LITE_AVATAR_DIR"

bash download_model.sh

popd
