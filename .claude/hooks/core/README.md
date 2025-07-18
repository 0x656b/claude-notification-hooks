# Core Notification System

The central notification dispatcher that manages all plugins and handles events.

## Features

- 🔌 Plugin-based architecture
- 📝 Activity logging
- 🔇 Quiet hours support
- 🎛️ Per-tool control
- 🌐 Multi-language support
- 📊 Debug mode

## Configuration

Edit `config.yaml`:

```yaml
# Plugin configuration
plugins:
  sound:
    enabled: true
    script: "../plugins/sound/smart-notification.py"
    events:
      Stop: true
      PreToolUse: true
    tools:
      enabled: true
      custom:
        Bash: {PreToolUse: true}
        Edit: {PreToolUse: true}

# Quiet hours
quiet_hours:
  enabled: true
  start: "23:00"
  end: "07:00"
  mute: ["sound"]

# Activity logging
logging:
  enabled: false
  max_size_mb: 10
  rotate: true

# Language setting
culture:
  language: "en"  # 'en' or 'tr'
```

## Events

- `PreToolUse` - Before Claude uses a tool
- `PostToolUse` - After Claude uses a tool
- `Stop` - When Claude finishes a task
- `Notification` - General notifications
- `SubagentStop` - When subtasks complete

## Debug Mode

Enable debug output:
```bash
export CLAUDE_DEBUG=true
```

## Plugin Development

Add new plugins by:
1. Creating a new directory in `plugins/`
2. Adding `config.yaml` and `README.md`
3. Creating the notification script
4. Adding to core `config.yaml`