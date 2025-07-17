# Claude Code Hook Notification System

A comprehensive notification system using Claude Code's hook functionality to provide audio, Telegram, and desktop notifications during development work.

[🇹🇷 Türkçe README](README-TR.md)

## 📋 Table of Contents

- [What is Claude Code and Hooks?](#-what-is-claude-code-and-hooks)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Testing Your Installation](#-testing-your-installation)
- [Installation](#-installation)
- [Notification Types](#-notification-types)
- [Configuration](#️-configuration)
- [Platform Support](#-platform-support)
- [Telegram Setup](#-telegram-setup)
- [Troubleshooting](#-troubleshooting)
- [Advanced Topics](#-advanced-topics)

## 🤖 What is Claude Code and Hooks?

### Claude Code
Claude Code is Anthropic's official CLI tool that brings Claude AI's capabilities directly to your terminal. It helps with:
- Writing and editing code
- Running commands
- Reading and analyzing files
- Answering programming questions
- And much more!

### What are Hooks?
Hooks are commands that Claude Code executes at specific events during its operation. Think of them as "triggers" that fire when Claude does something.

**Example Events:**
- `PreToolUse` - Before Claude uses a tool (like running a command)
- `PostToolUse` - After Claude uses a tool
- `Stop` - When Claude finishes a task
- `Notification` - When Claude needs your attention
- `SubagentStop` - When a subtask is completed

**Example Hook:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/notify.py"
        }
      ]
    }
  ]
}
```

This hook runs `notify.py` whenever Claude stops, playing a "work complete" sound!

## 📁 Project Structure

```
claude-notification-hooks/
├── .claude/                    # Claude Code configuration folder
│   ├── settings.json          # Hook definitions
│   └── hooks/                 # Hook scripts and configs
│       ├── config-manager/    # Central configuration
│       │   ├── notify-all.py  # Main notification dispatcher
│       │   ├── notification-config.json  # User settings
│       │   └── activity-logger.py
│       ├── voice-notifier/    # Audio notification system
│       │   ├── smart-notification.py
│       │   ├── sound-mapping.json
│       │   └── voice/        # MP3 sound files
│       │       ├── bash.mp3
│       │       ├── editing.mp3
│       │       ├── ready.mp3
│       │       └── ...
│       ├── telegram-bot/      # Telegram integration
│       │   ├── telegram-notifier.py
│       │   └── telegram-config.json  # Bot credentials
│       ├── toast-notifier/    # Cross-platform desktop notifications
│       │   └── cross-platform-notifier.py
│       └── utils/             # Utility functions
│           └── platform_utils.py
├── README.md                  # This file
├── README-TR.md              # Turkish documentation
├── CLAUDE.md                 # Instructions for Claude
└── .gitignore               # Git ignore file
```

## 🚀 Quick Start

1. **Copy the `.claude` folder** to your project root
2. **Install Python dependencies:**
   ```bash
   pip install pygame plyer windows-toasts python-telegram-bot
   ```
3. **Activate hooks in Claude Code:**
   ```bash
   /hooks
   ```
4. **Test it:** Let Claude do something and hear the notification!

## 🧪 Testing Your Installation

After installation, test all notification types:

```bash
python3 .claude/hooks/test-notifications.py
```

This will:
- Test each notification type (sound, desktop, Telegram)
- Show which dependencies are installed
- Display configuration status
- Help diagnose any issues

## 📦 Installation

### Prerequisites
- Python 3.7+
- Claude Code CLI installed
- pip (Python package manager)

### Platform Compatibility
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu/Debian Linux
- ✅ Most Linux distributions with Python 3.7+

### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/claude-notification-hooks
# OR just copy the .claude folder to your project
```

### Step 2: Install Dependencies

We provide convenient installation scripts for automatic setup:

**Windows (run as Administrator):**
```bash
install-windows.bat
```

**macOS/Linux:**
```bash
chmod +x install-mac-linux.sh
./install-mac-linux.sh
```

**Or install manually:**

**Windows:**
```bash
pip install -r requirements.txt
# Or manually:
pip install pygame plyer windows-toasts python-telegram-bot
```

**macOS:**
```bash
pip install -r requirements.txt
# Audio uses built-in afplay, notifications use osascript
```

**Linux:**
```bash
pip install -r requirements.txt
# Optional: sudo apt-get install sox mpg123
```

The installation scripts will:
- Check for Python installation
- Update pip to the latest version
- Install all required dependencies from requirements.txt
- Provide platform-specific recommendations
- Make Python scripts executable (Linux/macOS)

### Step 3: Configure (Optional)
Edit `.claude/hooks/config-manager/notification-config.json`:
```json
{
  "notifications": {
    "sound": {
      "enabled": true,
      "events": {
        "Stop": true,
        "Notification": true,
        "PreToolUse": true
      }
    },
    "telegram": {
      "enabled": false,  # Enable after setup
      "events": {
        "Stop": true,
        "Notification": true
      }
    }
  }
}
```

### Step 4: Activate Hooks
In Claude Code:
```bash
/hooks
```
This opens the hooks interface. The hooks are already defined in `settings.json`.

**Important for Windows:** If hooks don't work immediately:
1. Add a dummy hook (e.g., `echo test`)
2. Remove it immediately
3. This refreshes the cache and activates all hooks

## 🔔 Notification Types

### 1. 🔊 Audio Notifications
- Custom MP3 sounds for different tools
- Fallback beep sounds if MP3s are missing
- Volume control in config

**Sounds:**
- `bash.mp3` - Shell commands
- `editing.mp3` - File edits
- `ready.mp3` - Task complete
- `commit.mp3` - Git operations
- And more!

### 2. 📱 Telegram Notifications
- Get notified on your phone
- Perfect for long-running tasks
- Rich formatted messages with emojis

### 3. 💻 Desktop Toast Notifications
- Native OS notifications
- Windows/macOS/Linux support
- Non-intrusive pop-ups

### 4. 🔌 Custom Plugin Notifications
- Fully extensible plugin architecture
- Add any notification method (Discord, Slack, Email, etc.)
- Simple JSON configuration
- See [Plugin System](#plugin-system) for details

## ⚙️ Configuration

### Main Configuration File
`.claude/hooks/config-manager/notification-config.json`

```json
{
  "notifications": {
    "sound": {
      "enabled": true,
      "script": "voice-notifier/smart-notification.py",
      "volume": 100,
      "events": {
        "Stop": true,
        "Notification": true,
        "PreToolUse": true,
        "PostToolUse": false
      }
    },
    "telegram": {
      "enabled": true,
      "script": "telegram-bot/telegram-notifier.py",
      "events": {
        "Stop": true,
        "Notification": true,
        "SubagentStop": true
      }
    },
    "desktop_toast": {
      "enabled": true,
      "script": "toast-notifier/cross-platform-notifier.py",
      "events": {
        "Stop": true,
        "Notification": true,
        "SubagentStop": true
      }
    }
  },
  "quiet_hours": {
    "enabled": false,
    "start": "23:00",
    "end": "07:00",
    "mute": ["sound"],
    "allow": ["telegram", "desktop_toast"]
  },
  "logging": {
    "enabled": false,
    "max_size_mb": 10
  }
}
```

**Key Features:**
- **Plugin-based**: Each notification type is a plugin with its own script
- **Flexible events**: Control which events trigger each plugin
- **Tool-level control**: Fine-tune which tools trigger notifications
- **Multi-language support**: English and Turkish notifications (configurable)
- **Quiet hours**: Fine-grained control over which plugins run at night
- **Extensible**: Add any custom notification plugin easily

### Tool-Level Control

Fine-tune which tools trigger notifications for any plugin. This feature is available for all plugins, not just sound:

```json
"sound": {
  "enabled": true,
  "events": {
    "PreToolUse": true  // Global setting
  },
  "tools": {
    "enabled": true,    // Enable tool-specific control
    "custom": {
      "Bash": {"PreToolUse": true, "PostToolUse": false},
      "Edit": {"PreToolUse": true, "PostToolUse": false},
      "Read": {"PreToolUse": true, "PostToolUse": false},
      "Grep": {"PreToolUse": false, "PostToolUse": false},  // Silent
      "LS": {"PreToolUse": false, "PostToolUse": false},     // Silent
      "Glob": {"PreToolUse": false, "PostToolUse": false}    // Silent
    }
  }
}
```

**Options:**
- `whitelist`: Only these tools will make sounds
- `blacklist`: These tools will never make sounds
- `custom`: Per-tool event settings (overrides global events)

### Language Settings

Set your preferred language for Telegram and desktop notifications:

```json
"culture": {
  "language": "en"  // Options: "en" (English) or "tr" (Türkçe)
}
```

### Sound Mapping
`.claude/hooks/voice-notifier/sound-mapping.json`

**Note about MP3 files**: The project uses MP3 sound files which are not included in the repository due to licensing. You can:
1. Use the fallback beep sounds (automatic)
2. Add your own MP3 files to `.claude/hooks/voice-notifier/voice/`
3. Use royalty-free notification sounds from sites like freesound.org

Customize which tool triggers which sound:
```json
{
  "tool_sounds": {
    "Bash": "bash.mp3",
    "Edit": "editing.mp3",
    "Read": "listing.mp3"
  },
  "event_sounds": {
    "Stop": "ready.mp3",
    "Notification": "ready.mp3"
  }
}
```

## 🌍 Platform Support

This project automatically detects your OS and adapts accordingly!

### Windows
- **Audio**: pygame for MP3, winsound for beeps
- **Toast**: Windows 10/11 notifications via plyer
- **Path format**: Both `C:\path` and `/c/path` work

### macOS
- **Audio**: afplay (built-in)
- **Toast**: osascript notifications
- **No additional setup needed!**

### Linux
- **Audio**: paplay/aplay/mpg123 (auto-detected)
- **Toast**: notify-send
- **Optional**: `sudo apt-get install sox mpg123`

## 📱 Telegram Setup

### Step 1: Create a Bot

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Choose a name (e.g., "My Claude Notifier")
4. Choose a username (e.g., `my_claude_bot`)
5. Copy the token you receive

### Step 2: Get Your Chat ID

1. Send any message to your bot
2. Open this URL in your browser:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
3. Find your chat ID in the response:
   ```json
   "chat": {"id": 123456789}
   ```

### Step 3: Configure

**IMPORTANT**: Never commit your real credentials to version control!

Copy the template and add your credentials:
```bash
cp .claude/hooks/telegram-bot/telegram-config.json.template .claude/hooks/telegram-bot/telegram-config.json
```

Then edit `.claude/hooks/telegram-bot/telegram-config.json`:
```json
{
  "bot_token": "YOUR_BOT_TOKEN_HERE",
  "chat_id": "YOUR_CHAT_ID_HERE"
}
```

Or use environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

### Step 4: Enable in Config
Set `telegram.enabled` to `true` in `notification-config.json`

## 🔧 Troubleshooting

### Quick Diagnosis
Run the test script to check your setup:
```bash
python3 .claude/hooks/test-notifications.py
```

### Common Issues

#### 1. Hooks Not Working At All
**Symptoms:** No notifications when Claude runs commands

**Solutions:**
- Run `/hooks` in Claude Code
- **Windows Cache Issue:** Add a dummy hook (e.g., `echo test`), then remove it
- Verify Python 3 is in PATH: `python3 --version`
- Check hook definitions in `.claude/settings.json`
- Try absolute paths in hook commands

#### 2. Missing Dependencies
**Error:** `ModuleNotFoundError: No module named 'plyer'`

**Solutions:**
```bash
# Windows
pip install -r requirements.txt
# Or use installation scripts (see Installation section)

# Mac/Linux
pip install -r requirements.txt
# Or use installation scripts (see Installation section)
```

#### 3. No Sound (Platform-Specific)

**Windows:**
- Install pygame: `pip install pygame`
- Check volume in `notification-config.json`
- Verify MP3 files exist in `.claude/hooks/voice-notifier/voice/`
- Try beep fallback by removing MP3 files

**Linux:**
- Install audio player: `sudo apt-get install sox mpg123`
- Check audio permissions
- Test with: `play /usr/share/sounds/ubuntu/stereo/bell.ogg`

**macOS:**
- Should work out of the box with afplay
- Check system sound settings

#### 4. Telegram Issues

**Bot not responding:**
- Verify `telegram-config.json` exists and has correct values
- Test bot token: `https://api.telegram.org/bot<TOKEN>/getMe`
- Ensure you've sent `/start` to your bot
- Check firewall/proxy settings

**Wrong chat ID:**
- Get updates: `https://api.telegram.org/bot<TOKEN>/getUpdates`
- Look for `"chat":{"id":YOUR_ID}`

#### 5. Desktop Toast Issues

**Windows "Python 3.13" in title:**
- This is normal for Python-based notifications
- For cleaner look, consider using PowerShell-based solution

**Linux notifications not showing:**
- Install: `sudo apt-get install libnotify-bin`
- Test: `notify-send "Test" "Message"`
- Check if notifications are enabled in system settings

**macOS notifications blocked:**
- Check System Preferences > Notifications
- Allow Terminal/Python notifications

#### 6. Quiet Hours Not Working
- Verify time format is 24-hour: "23:00" not "11:00 PM"
- Check timezone settings
- Ensure plugin names in `mute`/`allow` match exactly

#### 7. Custom Plugin Not Loading
- Check script path is correct (relative to `.claude/hooks/`)
- Verify script has execute permissions on Unix
- Add debug print at start of script
- Check for Python syntax errors

#### 8. Performance Issues
- Disable logging: `"logging": {"enabled": false}`
- Reduce active notifications
- Use quiet hours to limit notifications

### Debug Mode
Add this to your plugin scripts for debugging:
```python
import sys
print(f"Debug: Called with args: {sys.argv}", file=sys.stderr)
```

### Still Having Issues?
1. Check the logs (if enabled) in `.claude/hooks/`
2. Run test script: `python3 .claude/hooks/test-notifications.py`
3. Create an issue on GitHub with:
   - Your OS and Python version
   - Error messages
   - Your `notification-config.json` (remove sensitive data)

## 🎓 Advanced Topics

### GitHub Actions Integration

You can use this notification system in your CI/CD pipelines! See our GitHub Actions Guide ([English](docs/GITHUB_ACTIONS.md) | [Türkçe](docs/GITHUB_ACTIONS_TR.md)) for:

- 🚀 Quick setup for build notifications
- 🤖 Full Claude Code automation examples  
- 💬 PR comment commands (`/claude review`)
- 📊 Status reporting back to GitHub
- 🔔 Multi-platform notification strategies

Example workflows are in `.github/workflows/`:
- [`simple-example.yml`](.github/workflows/simple-example.yml) - Basic build notifications
- [`claude-code-example.yml`](.github/workflows/claude-code-example.yml) - Full Claude Code integration

### Claude Code Sandbox Environment

Claude Code runs in a sandboxed environment with some quirks:

1. **Path Formats:**
   - Hook definitions use Unix paths: `/d/project/script.py`
   - Python scripts can use Windows paths: `D:\project\script.py`
   - Both formats work in most cases

2. **Environment Variables:**
   - Sandbox may not access system environment variables
   - Use config files instead of relying on env vars

3. **Python Execution:**
   - Uses `python3` command even on Windows
   - Runs the system's Python installation

### Custom Hooks

Add your own hooks to `settings.json`:
```json
{
  "MyCustomEvent": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/my-script.py"
        }
      ]
    }
  ]
}
```

### Hook Parameters

Hooks receive parameters about the event:
- `%TOOL_NAME%` - Name of the tool used
- `%EVENT_TYPE%` - Type of event triggered

Example:
```bash
python3 notify.py %TOOL_NAME% %EVENT_TYPE%
```

### Plugin System

The notification system is fully plugin-based! Each notification type is a plugin defined in `notification-config.json`.

#### Built-in Plugins

```json
{
  "sound": {
    "enabled": true,
    "script": "voice-notifier/smart-notification.py",
    "events": {
      "Stop": true,
      "Notification": true,
      "PreToolUse": true
    }
  }
}
```

#### Creating Custom Plugins

1. **Write your notification script** that accepts two parameters:
   ```python
   # my-notifier.py
   import sys
   tool_name = sys.argv[1]  # e.g., "Bash"
   event_type = sys.argv[2]  # e.g., "Stop"
   # Your notification logic here
   ```

2. **Add to notification-config.json**:
   ```json
   "my_custom_notifier": {
     "enabled": true,
     "script": "custom/my-notifier.py",
     "events": {
       "Stop": true,
       "Notification": true
     },
     "tools": {
       "enabled": true,
       "blacklist": ["LS", "Grep"]  // Optional tool-level control
     },
     "params": ["--extra", "parameters"]
   }
   ```

3. **That's it!** The plugin will automatically be loaded and run.

#### Plugin Examples

**Discord Webhook:**
```json
"discord": {
  "enabled": true,
  "script": "discord-bot/discord-notifier.py",
  "events": {
    "Stop": true,
    "Notification": true
  },
  "params": ["--webhook-url", "YOUR_WEBHOOK_URL"]
}
```

**Slack (Absolute Path):**
```json
"slack": {
  "enabled": true,
  "script": "/home/user/scripts/slack-notifier.py",
  "events": {
    "Stop": true
  }
}
```

**Email Notifications:**
```json
"email": {
  "enabled": true,
  "script": "email-plugin/send-email.py",
  "events": {
    "Stop": true,
    "Notification": true
  },
  "params": ["--to", "your@email.com", "--smtp", "smtp.gmail.com"]
}
```

#### Quiet Hours for Plugins

Control which plugins work during quiet hours:

```json
"quiet_hours": {
  "enabled": true,
  "start": "23:00",
  "end": "07:00",
  "mute": ["sound", "discord"],  // These plugins won't run
  "allow": ["telegram", "email"]  // These will always run
}
```

## 🔒 Security Best Practices

- **Never commit credentials**: Always use `.gitignore` for config files with tokens
- **Use environment variables**: For CI/CD, use secrets instead of hardcoded values
- **Rotate tokens regularly**: If a token is exposed, regenerate it immediately
- **Minimal permissions**: Give bots only the permissions they need

## 🤝 Contributing

Feel free to submit issues and pull requests!

## 📝 License

This project is open source and available under the MIT License.

---

**Note**: This is a notification system, not a monitoring system. It's designed to help you stay aware of Claude's activities, not to track or log them extensively.

**Important**: Before sharing this project, ensure you've removed any personal credentials from `telegram-config.json`!