#!/bin/bash

# Set root directory
MUSETALK_ROOT_DIR="models/musetalk"
MODEL_DIR="models"

# Create all necessary subdirectories
mkdir -p "$MODEL_DIR"
mkdir -p "$MUSETALK_ROOT_DIR"
mkdir -p "$MUSETALK_ROOT_DIR/musetalkV15"
mkdir -p "$MUSETALK_ROOT_DIR/syncnet"
mkdir -p "$MUSETALK_ROOT_DIR/dwpose"
mkdir -p "$MUSETALK_ROOT_DIR/whisper"
mkdir -p "$MODEL_DIR/sd-vae"
mkdir -p "$MODEL_DIR/face-parse-bisent"


# Install required packages
pip install -U "huggingface_hub[cli]"

# Set HuggingFace mirror (for use in mainland China)
export HF_ENDPOINT=https://hf-mirror.com

# Download MuseTalk weights (TMElyralab/MuseTalk) - download to root directory, may contain subdirectories
echo "Downloading MuseTalk main weights to $MUSETALK_ROOT_DIR..."
huggingface-cli download TMElyralab/MuseTalk --local-dir "$MUSETALK_ROOT_DIR" --local-dir-use-symlinks False


echo "Downloading SD VAE weights to $MODEL_DIR/sd-vae..."
huggingface-cli download stabilityai/sd-vae-ft-mse --local-dir "$MODEL_DIR/sd-vae" --local-dir-use-symlinks False


echo "Downloading Whisper weights to $MUSETALK_ROOT_DIR/whisper..."
huggingface-cli download openai/whisper-tiny --local-dir "$MUSETALK_ROOT_DIR/whisper" --local-dir-use-symlinks False --include "config.json" "pytorch_model.bin" "preprocessor_config.json"

echo "Downloading DWPose weights to $MUSETALK_ROOT_DIR/dwpose..."
huggingface-cli download yzd-v/DWPose --local-dir "$MUSETALK_ROOT_DIR/dwpose" --local-dir-use-symlinks False --include "dw-ll_ucoco_384.pth"

# Download SyncNet weights to syncnet subdirectory
echo "Downloading SyncNet weights to $MUSETALK_ROOT_DIR/syncnet..."
huggingface-cli download ByteDance/LatentSync --local-dir "$MUSETALK_ROOT_DIR/syncnet" --local-dir-use-symlinks False --include "latentsync_syncnet.pt"


echo "Downloading Face Parse Bisent weights to $MODEL_DIR/face-parse-bisent..."
huggingface-cli download ManyOtherFunctions/face-parse-bisent --local-dir "$MODEL_DIR/face-parse-bisent" --local-dir-use-symlinks False --include "79999_iter.pth" "resnet18-5c106cde.pth"

echo "Downloading MiniCPM-o-2_6-int4 weights to $MUSETALK_ROOT_DIR/s3fd-619a316812..."
git clone https://www.modelscope.cn/HaveAnApplePie/s3fd-619a316812.git $MUSETALK_ROOT_DIR/s3fd-619a316812

echo "All download commands have been executed, but the model files may not be downloaded. Please check the following directories and files exist:"
echo "\n- models/musetalk/ (MuseTalk main weights)"
echo "- models/musetalk/whisper/config.json"
echo "- models/musetalk/whisper/pytorch_model.bin"
echo "- models/musetalk/whisper/preprocessor_config.json"
echo "- models/musetalk/dwpose/dw-ll_ucoco_384.pth"
echo "- models/musetalk/syncnet/latentsync_syncnet.pt"
echo "- models/sd-vae/ (SD VAE weights)"
echo "- models/face-parse-bisent/79999_iter.pth"
echo "- models/face-parse-bisent/resnet18-5c106cde.pth"
echo "\nIf any file is missing, please check the download logs above."

echo "If files are missing, run the script again."

