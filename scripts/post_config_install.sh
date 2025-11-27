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

    # 2. Install mmcv==2.2.0
    echo "Installing mmcv==2.2.0..."
    uv pip uninstall mmcv
    uv run mim install mmcv==2.2.0 --force
else
    echo "No AvatarMusetalk configuration found in config file, skipping additional configuration."
fi 
