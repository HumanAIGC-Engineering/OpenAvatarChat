#!/bin/bash
set -e

# Set model directory
MODEL_DIR="models/smart_turn"

# Create directory
mkdir -p "$MODEL_DIR"

# Install required packages (prefer uv if available)
if command -v uv &> /dev/null && [ -d ".venv" ]; then
    uv pip install -U "huggingface_hub[cli]"
else
    pip install -U "huggingface_hub[cli]"
fi

# Set HuggingFace mirror (for use in mainland China)
export HF_ENDPOINT=https://hf-mirror.com

# Download Smart Turn v3 model
echo "Downloading Smart Turn v3 model to $MODEL_DIR..."
if ! hf download pipecat-ai/smart-turn-v3 --local-dir "$MODEL_DIR"; then
    echo "✗ Download failed. Please check your network or HF endpoint, then retry." >&2
    exit 1
fi

echo ""
echo "Verifying downloaded contents in $MODEL_DIR:"

# List ONNX files (cpu/gpu variants may differ)
shopt -s nullglob
onnx_files=("$MODEL_DIR"/*.onnx)
if [ "${#onnx_files[@]}" -eq 0 ]; then
    echo "✗ No ONNX files found. Please retry download or check network." >&2
    exit 1
else
    echo "✓ Found ONNX files:"
    for f in "${onnx_files[@]}"; do
        echo "  - $f"
    done
fi

# Optional configs (best-effort)
for f in "$MODEL_DIR/config.json" "$MODEL_DIR/preprocessor_config.json"; do
    if [ -f "$f" ]; then
        echo "✓ Found: $f"
    else
        echo "• Optional: $f (not found)"
    fi
done

echo ""
echo "Done. If models are incomplete, re-run the script or check connectivity."

