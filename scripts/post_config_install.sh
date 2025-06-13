#!/usr/bin/env bash

# Initialize variables
CONFIG_FILE=""

# Detect workspace directory based on script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$WORKSPACE_DIR/.venv"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --config )
            CONFIG_FILE="$2"
            shift 2 # Skip current and next argument
            ;;
        * )
            shift # Skip unknown arguments
            ;;
    esac
done

if [[ -z "$CONFIG_FILE" ]]; then
    echo "Error: No config file specified. Please use --config parameter to specify the config file path."
    exit 1
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Config file $CONFIG_FILE does not exist."
    exit 1
fi

echo "Parsing config file: $CONFIG_FILE"

# Set LD_LIBRARY_PATH environment variable
echo "Setting NVIDIA library paths to LD_LIBRARY_PATH..."

# Find nvidia library paths in .venv
NVIDIA_PATHS=""

# Check common nvidia library paths
NVIDIA_LIBS=(
    "cuda_runtime/lib"
    "cublas/lib" 
    "cudnn/lib"
    "cufft/lib"
    "curand/lib"
    "cusolver/lib"
    "cusparse/lib"
    "nccl/lib"
    "nvjpeg/lib"
    "nvtx/lib"
)

for lib in "${NVIDIA_LIBS[@]}"; do
    LIB_PATH="$VENV_PATH/lib/python3.11/site-packages/nvidia/$lib"
    if [[ -d "$LIB_PATH" ]]; then
        if [[ -z "$NVIDIA_PATHS" ]]; then
            NVIDIA_PATHS="$LIB_PATH"
        else
            NVIDIA_PATHS="$NVIDIA_PATHS:$LIB_PATH"
        fi
        echo "Found NVIDIA library path: $LIB_PATH"
    fi
done

if [[ -n "$NVIDIA_PATHS" ]]; then
    # Export the environment variable directly
    export LD_LIBRARY_PATH="$NVIDIA_PATHS:$LD_LIBRARY_PATH"
    echo "LD_LIBRARY_PATH has been set to: $LD_LIBRARY_PATH"
    
    # Create a script to set the environment variable for future login shells
    echo "#!/bin/bash" > /etc/profile.d/nvidia_libs.sh
    echo "export LD_LIBRARY_PATH=\"$NVIDIA_PATHS:\$LD_LIBRARY_PATH\"" >> /etc/profile.d/nvidia_libs.sh
    chmod +x /etc/profile.d/nvidia_libs.sh

    # Ensure non-login interactive shells also get the variable
    if [[ -f /etc/bash.bashrc ]]; then
        echo "export LD_LIBRARY_PATH=\"$NVIDIA_PATHS:\$LD_LIBRARY_PATH\"" >> /etc/bash.bashrc
    fi
    
    # Register the paths with the dynamic linker so they are picked up without LD_LIBRARY_PATH
    echo "$NVIDIA_PATHS" | tr ':' '\n' > /etc/ld.so.conf.d/nvidia_venv.conf
    ldconfig -v 2>/dev/null || true
    
    echo "NVIDIA library paths have been added to LD_LIBRARY_PATH"
    echo "Note: Please open a new shell or run 'source /etc/profile.d/nvidia_libs.sh' to apply changes in current session"
else
    echo "Warning: No NVIDIA library paths found"
fi

# Check if config file contains AvatarMusetalk configuration
if grep -q "AvatarMusetalk:" "$CONFIG_FILE"; then
    echo "AvatarMusetalk configuration detected, starting additional configuration..."
    
    # 1. Modify mmcv_maximum_version in mmdet's __init__.py file
    MMDET_INIT_FILE="$VENV_PATH/lib/python3.11/site-packages/mmdet/__init__.py"
    
    if [[ -f "$MMDET_INIT_FILE" ]]; then
        echo "Modifying mmcv_maximum_version in mmdet/__init__.py..."
        sed -i "s/mmcv_maximum_version = '[^']*'/mmcv_maximum_version = '2.2.1'/g" "$MMDET_INIT_FILE"
        echo "mmcv_maximum_version has been updated to 2.2.1"
    else
        echo "Warning: $MMDET_INIT_FILE file not found"
    fi
    
    echo "AvatarMusetalk additional configuration completed."
else
    echo "No AvatarMusetalk configuration found in config file, skipping additional configuration."
fi 
