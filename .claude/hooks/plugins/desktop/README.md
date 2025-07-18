# Desktop Notification Plugin

Shows desktop toast notifications across Windows, macOS, and Linux.

## Features

- 🪟 Windows toast notifications
- 🍎 macOS notification center
- 🐧 Linux desktop notifications
- ⏰ Configurable duration
- 🎨 Custom titles and icons
- 📱 Cross-platform compatibility

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install plyer PyYAML
   ```

2. **Configure notifications:**
   Edit `config.yaml`:
   ```yaml
   title: "Claude Code"
   duration: 5
   icon: "/path/to/icon.ico"  # Optional
   ```

3. **Test notification:**
   ```bash
   python3 cross-platform-notifier.py Test Stop
   ```

## Configuration

Edit `config.yaml`:

```yaml
# Basic settings
title: "Claude Code"
duration: 5  # seconds
icon: ""     # Path to icon file (optional)

# Platform-specific settings
windows:
  app_id: "Claude.Code.Notifications"
  use_powershell: false

macos:
  sound: "default"
  
linux:
  urgency: "normal"  # low, normal, critical
  category: "dev"
```

## Platform Requirements

### Windows
- Uses `plyer` library for native notifications
- No additional setup required

### macOS
- Uses `osascript` for native notifications
- No additional setup required

### Linux
- Requires `libnotify` and `notify-send`
- Install with: `sudo apt-get install libnotify-bin` (Ubuntu/Debian)
- Or: `sudo yum install libnotify` (CentOS/RHEL)

## Troubleshooting

- **No notifications:** Check if notification daemon is running
- **Wrong title:** Verify config.yaml syntax
- **Permission denied:** Ensure notification permissions are enabled
- **Linux issues:** Install libnotify-bin package