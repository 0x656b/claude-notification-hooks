#!/bin/bash

echo "======================================================"
echo " Claude Code Hook Notification System - Setup"
echo "======================================================"
echo ""

# OS detection
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    echo "[ERROR] Unsupported OS: $OSTYPE"
    exit 1
fi

echo "[OK] Detected OS: $OS"

# Python check
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org"
    exit 1
fi

echo "[OK] Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "Installing Python packages..."
python3 -m pip install --upgrade pip

# Get script directory and install from there
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Some packages failed to install!"
    exit 1
fi

# Platform-specific recommendations
echo ""
echo "======================================================"
echo " Platform-specific recommendations"
echo "======================================================"

if [[ "$OS" == "Linux" ]]; then
    echo ""
    echo "For Linux users:"
    echo "- Audio: Install sox for better sound support"
    echo "  sudo apt-get install sox"
    echo "- Notifications: notify-send should be pre-installed"
    echo "  If not: sudo apt-get install libnotify-bin"
elif [[ "$OS" == "macOS" ]]; then
    echo ""
    echo "For macOS users:"
    echo "- Audio: Uses built-in afplay (no action needed)"
    echo "- Notifications: Uses osascript (no action needed)"
fi

echo ""
echo "======================================================"
echo " Installation complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Copy .claude folder to your project root"
echo "2. Run /hooks command in Claude Code"
echo "3. Test: python3 .claude/hooks/test-notifications.py"
echo ""
echo "For Telegram notifications:"
echo "- Create .claude/hooks/telegram-bot/telegram-config.json"
echo "- Follow Telegram setup in README"
echo ""

# Make scripts executable
chmod +x .claude/hooks/*.py 2>/dev/null
chmod +x .claude/hooks/*/*.py 2>/dev/null

echo "Press any key to continue..."
read -n 1