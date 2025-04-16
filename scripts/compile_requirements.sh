#!/bin/sh

# Get the directory where the script is located and navigate to the project root directory
SCRIPT_DIR=$(dirname "$0")
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

# Set the upgrade flag
UPGRADE_FLAG=""
if [ "$1" = "--upgrade" ]; then
    UPGRADE_FLAG="--upgrade"
    echo "[INFO] Upgrade mode enabled"
fi

# Process a directory
process_directory() {
    DIR=$1
    if [ -f "$DIR/pyproject.toml" ]; then
        echo "[INFO] Processing directory: ${DIR#$ROOT_DIR/}"
        (cd "$DIR" && uv pip compile pyproject.toml -o requirements.txt $UPGRADE_FLAG)
        echo "[INFO] Done processing directory: ${DIR#$ROOT_DIR/}"
    else
        echo "[WARN] pyproject.toml not found in ${DIR#$ROOT_DIR/}"
    fi
}

# Process the root directory
process_directory "$ROOT_DIR"

# Process secondary subdirectories under src/handlers
find "$ROOT_DIR/src/handlers" -maxdepth 2 -mindepth 2 -type d | while read -r DIR; do
    process_directory "$DIR"
done

echo "[INFO] Dependency compilation completed"
