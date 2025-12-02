#!/usr/bin/env bash

# Initialize variables
CONFIG_FILE=""

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
    echo "AvatarMusetalk configuration detected, starting dependency installation..."
    
    # Install dependencies
    echo "Installing setuptools and pip..."
    uv pip install setuptools pip
    
    echo "Installing chumpy==0.70..."
    uv pip install chumpy==0.70 --no-build-isolation
    
    echo "AvatarMusetalk dependencies installation completed."
else
    echo "No AvatarMusetalk configuration found in config file, skipping dependency installation."
fi 
