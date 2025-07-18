# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Code Hook Notification System - A comprehensive cross-platform notification system using Claude Code's hook functionality to provide audio, desktop toast, and Telegram notifications with multi-language support (English/Turkish).

## Architecture (v2.0 - Restructured)

```
.claude/
├── hooks/
│   ├── core/                # Main notification system
│   │   ├── notify-all.py    # Unified notification dispatcher
│   │   ├── config.yaml      # Core system configuration
│   │   └── README.md        # Core system documentation
│   ├── plugins/             # Self-contained notification plugins
│   │   ├── sound/           # Audio notification system
│   │   │   ├── smart-notification.py     # Cross-platform audio
│   │   │   ├── config.yaml              # Sound plugin configuration
│   │   │   ├── README.md                # Sound plugin documentation
│   │   │   ├── voice/                   # Default MP3 files
│   │   │   ├── female_tr/               # Turkish female voice
│   │   │   ├── male_tr/                 # Turkish male voice
│   │   │   ├── female_en/               # English female voice
│   │   │   ├── male_en/                 # English male voice
│   │   │   └── custom/                  # User custom sounds
│   │   ├── telegram/        # Telegram integration
│   │   │   ├── telegram-notifier.py
│   │   │   ├── config.yaml              # Telegram plugin configuration
│   │   │   └── README.md                # Telegram setup guide
│   │   └── desktop/         # Desktop notifications
│   │       ├── cross-platform-notifier.py
│   │       ├── config.yaml              # Desktop plugin configuration
│   │       └── README.md                # Desktop plugin documentation
│   └── tools/               # Installation and configuration tools
│       ├── install/         # Installation scripts
│       │   ├── install-windows.bat
│       │   ├── install-mac-linux.sh
│       │   └── requirements.txt
│       ├── configure/       # Configuration utilities
│       │   ├── configure-notifications.bat
│       │   ├── configure-notifications.sh
│       │   └── configure.py
│       └── test/            # Test utilities
│           └── test-notifications.py
└── settings.json           # Hook definitions
```

## Key Features (v2.0)

1. **Unified Architecture**: Single notify-all.py handles all events and activity logging
2. **Modular Plugins**: Each notification type is self-contained with its own config and docs
3. **YAML Configuration**: User-friendly YAML configs with JSON fallback
4. **Voice Set Switching**: Change entire voice set with one config line (`audio_directory`)
5. **Multi-language Support**: English and Turkish (configurable via `culture.language`)
6. **Tool-level Control**: Fine-grained control over which tools trigger notifications
7. **Cross-platform**: Windows, macOS, and Linux support (enhanced Mac beep)
8. **Quiet Hours**: Configurable silent periods with per-plugin control
9. **Smart Sound System**: 
   - Tools defined in config.yaml play their specific sounds
   - Undefined tools are silent during PreToolUse/PostToolUse
   - Stop events always play their designated sound regardless of tool
10. **Ultra-Simple Setup**: True 30-second installation experience

## Important Commands

### Quick Configuration (v2.0)
Configure notifications without editing YAML:
```bash
# Windows
.claude/hooks/tools/configure/configure-notifications.bat sound:0 telegram:1 lang:tr

# Linux/Mac
./.claude/hooks/tools/configure/configure-notifications.sh toast:0 quiet:23:00-07:00

# Show current configuration
.claude/hooks/tools/configure/configure-notifications.bat status
```

### Test Installation
```bash
python3 .claude/hooks/tools/test/test-notifications.py
```

### Manual Notification Test
```bash
# Test all notifications
python3 .claude/hooks/core/notify-all.py "Test" "Stop"

# Test specific notifier
python3 .claude/hooks/plugins/telegram/telegram-notifier.py "Test" "Stop"
```

### Reset to Template
When user wants clean credentials:
```bash
# Reset Telegram config (now YAML)
cp .claude/hooks/plugins/telegram/config.yaml.template .claude/hooks/plugins/telegram/config.yaml
```

## Configuration Guide (v2.0)

### Core Configuration
In `.claude/hooks/core/config.yaml`:
```yaml
# Language settings
culture:
  language: "en"  # or "tr" for Turkish

# Quiet hours
quiet_hours:
  enabled: true
  start: "23:00"
  end: "07:00"
  mute: ["sound"]  # Plugins to mute during quiet hours

# Activity logging
logging:
  enabled: false
  max_size_mb: 10
  rotate: true
```

### Plugin Configuration
Each plugin has its own config.yaml:

#### Sound Plugin (`.claude/hooks/plugins/sound/config.yaml`)
```yaml
# Voice set switching
audio_directory: "voice"  # Change to: female_tr, male_tr, female_en, male_en, custom

# Tool-level control
volume: 100
tool_sounds:
  Bash: "bash.mp3"
  Edit: "editing.mp3"
  # ... more tools
```

#### Telegram Plugin (`.claude/hooks/plugins/telegram/config.yaml`)
```yaml
# Telegram bot settings
bot_token: "YOUR_BOT_TOKEN_HERE"
chat_id: "YOUR_CHAT_ID_HERE"
message_format: "🤖 Claude Code: {message}"
```

#### Desktop Plugin (`.claude/hooks/plugins/desktop/config.yaml`)
```yaml
# Desktop notification settings
title: "Claude Code"
duration: 5
icon: ""  # Optional icon path
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

5. **Windows variable substitution**
   - Windows has issues with `${TOOL_NAME}` variables in hooks
   - This project uses individual hook definitions for each tool as a workaround
   - See `.claude/settings.json` for the implementation

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