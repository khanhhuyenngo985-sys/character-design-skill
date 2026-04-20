#!/bin/bash
# MemPalace Auto-Save Hook
# Saves session state to MemPalace palace

PALACE_PATH="$HOME/.mempalace"
PYTHON_BIN="/opt/homebrew/bin/python3.11"

# Only run if mempalace is installed
if ! command -v "$PYTHON_BIN" &> /dev/null; then
    exit 0
fi

# Run mempalace status check (optional mining of context)
"$PYTHON_BIN" -m mempalace status --palace "$PALACE_PATH" > /dev/null 2>&1

exit 0
