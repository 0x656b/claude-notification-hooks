# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Code Hook Notification System - A comprehensive cross-platform notification system using Claude Code's hook functionality to provide audio, desktop toast, and Telegram notifications with multi-language support (English/Turkish).

## Architecture

```
.claude/
├── hooks/
│   ├── config-manager/      # Central configuration and control
│   │   ├── notify-all.py    # Main notification dispatcher (plugin-based)
│   │   ├── notification-config.json  # User settings
│   │   └── activity-logger.py        # Activity logging
│   ├── voice-notifier/      # Audio notification system
│   │   ├── smart-notification.py     # Cross-platform audio
│   │   ├── sound-mapping.json        # Tool-to-sound mappings
│   │   └── voice/          # MP3 sound files (not included)
│   ├── telegram-bot/       # Telegram integration
│   │   ├── telegram-notifier.py
│   │   └── telegram-config.json.template
│   └── toast-notifier/     # Desktop notifications
│       └── cross-platform-notifier.py
└── settings.json           # Hook definitions
```

## Key Features

1. **Plugin-based Architecture**: Each notification type is a plugin
2. **Multi-language Support**: English and Turkish (configurable via `culture.language`)
3. **Tool-level Control**: Fine-grained control over which tools trigger notifications
4. **Cross-platform**: Windows, macOS, and Linux support
5. **Quiet Hours**: Configurable silent periods with per-plugin control

## Important Commands

### Quick Configuration (New!)
Configure notifications without editing JSON:
```bash
# Windows
configure-notifications.bat sound:0 telegram:1 lang:tr

# Linux/Mac
./configure-notifications.sh toast:0 quiet:23:00-07:00

# Show current configuration
configure-notifications.bat status
```

### Test Installation
```bash
python3 .claude/hooks/test-notifications.py
```

### Manual Notification Test
```bash
# Test all notifications
python3 .claude/hooks/config-manager/notify-all.py "Test" "Stop"

# Test specific notifier
python3 .claude/hooks/telegram-bot/telegram-notifier.py "Test" "Stop"
```

### Reset to Template
When user wants clean credentials:
```bash
cp .claude/hooks/telegram-bot/telegram-config.json.template .claude/hooks/telegram-bot/telegram-config.json
```

## Configuration Guide

### Language Settings
In `notification-config.json`:
```json
"culture": {
  "language": "en"  // or "tr" for Turkish
}
```

### Tool-level Control
```json
"sound": {
  "tools": {
    "enabled": true,
    "custom": {
      "Bash": {"PreToolUse": true, "PostToolUse": false},
      "Grep": {"PreToolUse": false, "PostToolUse": false}
    }
  }
}
```

### Quiet Hours
```json
"quiet_hours": {
  "enabled": true,
  "start": "23:00",
  "end": "07:00",
  "mute": ["sound"],         // Plugins to mute
  "allow": ["telegram"]       // Plugins always allowed
}
```

## Common Issues & Solutions

1. **Hooks not updating (Windows)**
   - Use `/hooks` command
   - Add and remove a dummy hook to refresh cache

2. **No MP3 sounds**
   - Normal - system falls back to beep sounds
   - Users can add their own MP3s to `.claude/hooks/voice-notifier/voice/`

3. **Desktop notifications show "Python 3.13"**
   - Windows limitation with Python-based notifications
   - Consider using compiled notifier in future versions

4. **Telegram not working**
   - Check credentials in telegram-config.json
   - Ensure bot has received `/start` command

## Security Notes

- Never commit real credentials
- Use environment variables or config files
- telegram-config.json is gitignored by default
- Path traversal protection is implemented

## For Plugin Developers

Create a Python script that accepts two arguments:
```python
tool_name = sys.argv[1]   # e.g., "Bash"
event_type = sys.argv[2]  # e.g., "Stop"
```

Add to notification-config.json:
```json
"my_plugin": {
  "enabled": true,
  "script": "my-plugin/notifier.py",
  "events": {"Stop": true}
}
```

Remember: This is a notification system, not a monitoring system. Keep it lightweight and focused on user awareness.