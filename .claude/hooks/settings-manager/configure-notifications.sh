#!/bin/bash
# Claude Code Hook Notification Configurator
# Simple wrapper for the Python configuration tool

# Find Python executable
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.7 or later"
    exit 1
fi

# Get the directory where this script is located
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set the config file path as environment variable
export CLAUDE_NOTIFICATION_CONFIG="$DIR/.claude/hooks/config-manager/notification-config.json"

# Run the configuration tool
$PYTHON "$DIR/.claude/hooks/settings-manager/configure.py" "$@"