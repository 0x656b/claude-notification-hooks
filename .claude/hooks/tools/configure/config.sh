#!/bin/bash
# Claude Code Hook Notification Configurator
# Works from any location - finds the correct paths automatically

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.7 or later"
    exit 1
fi

# Set the config file path as environment variable (v2.0 structure)
export CLAUDE_NOTIFICATION_CONFIG="$SCRIPT_DIR/../../core/config.yaml"

# Run the configuration tool with relative path
$PYTHON "$SCRIPT_DIR/configure.py" "$@"