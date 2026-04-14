#!/usr/bin/env bash
# MuseTalk offline synthesis smoke test. Run from repository root (Inner-OpenAvatarChat).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"

CONFIG="${CONFIG:-config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml}"
AUDIO="${AUDIO:-tests/inttest/musetalk/assets/audio/test-audio-1.wav}"
OUTDIR="${OUTDIR:-tests/inttest/musetalk/outputs/offline}"
BATCH="${BATCH:-8}"

if [[ ! -f "$AUDIO" ]]; then
  echo "Missing audio: $AUDIO" >&2
  exit 1
fi

# Prefer project venv via uv so torch and deps resolve (see pyproject.toml)
if command -v uv &>/dev/null && [[ -f "$ROOT/pyproject.toml" ]]; then
  PYTHON=(uv run python)
else
  PYTHON=(python)
fi

exec "${PYTHON[@]}" src/handlers/avatar/musetalk/musetalk_algo.py \
  --config "$CONFIG" \
  --audio_path "$AUDIO" \
  --output_dir "$OUTDIR" \
  --batch_size "$BATCH" \
  "$@"
