#!/usr/bin/env bash

# ============================================================
# Knowledge Screen - Linux/Ubuntu Startup Launcher
# ============================================================

# Wait 60 seconds for desktop environment and monitors
# to finish initializing.
sleep 60

# Get the directory containing THIS script.
# Similar idea to %~dp0 in the Windows BAT file.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the Knowledge Screen project directory.
cd "$SCRIPT_DIR" || exit 1

# Launch using the project's virtual environment directly.
# No need to: source .venv/bin/activate
./.venv/bin/python knowledge_screen.py