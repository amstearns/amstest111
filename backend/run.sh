#!/bin/bash
# Start the Renewable Energy Executive Dashboard API
# Serves on port 8000

export PATH="$HOME/.local/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$WORKSPACE_ROOT"

echo "Starting Renewable Energy Dashboard API on port 8000..."
python3 -m uvicorn backend.app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --log-level info
