# Claude Code Notification System

Get instant notifications when Claude Code completes tasks - sounds, Telegram, desktop toasts!

[🇹🇷 Türkçe README](README-TR.md) | [📖 Full Documentation](docs/FULL-GUIDE.md)

## ⚡ 30-Second Setup

1. **Install:**
   ```bash
   # Windows
   .claude/hooks/tools/install/install-windows.bat
   
   # Linux/Mac
   ./.claude/hooks/tools/install/install-mac-linux.sh
   ```

2. **Configure:**
   ```bash
   # Quick config
   .claude/hooks/tools/configure/configure-notifications.bat sound:1 telegram:0
   
   # Or detailed setup
   .claude/hooks/tools/configure/configure-notifications.bat
   ```

3. **Done!** Claude Code will now notify you when tasks complete.

## 🔊 Notification Types

- **🎵 Sound** - Audio notifications (MP3 + beep fallback)
- **📱 Telegram** - Bot messages to your phone
- **🖥️ Desktop** - System toast notifications

## 🎛️ Quick Configuration

```bash
# Enable sound, disable telegram
.claude/hooks/tools/configure/configure-notifications.bat sound:1 telegram:0

# Set quiet hours (mute 11pm-7am)
.claude/hooks/tools/configure/configure-notifications.bat quiet:23:00-07:00

# Change language to Turkish
.claude/hooks/tools/configure/configure-notifications.bat lang:tr

# Show current settings
.claude/hooks/tools/configure/configure-notifications.bat status
```

## 📁 File Structure

```
.claude/hooks/
├── core/           # Main notification system
├── plugins/        # Sound, Telegram, Desktop
└── tools/          # Setup and configuration
```

## 🎯 What You Get

- **Instant feedback** when Claude completes tasks
- **Multi-language** support (English/Turkish)
- **Cross-platform** (Windows/Mac/Linux)
- **Plugin-based** architecture
- **YAML configuration** (user-friendly)

## 📚 Learn More

- [📖 Full Documentation](docs/FULL-GUIDE.md)
- [🔧 Plugin Development](docs/PLUGIN-DEVELOPMENT.md)
- [❓ Troubleshooting](docs/TROUBLESHOOTING.md)

## 🚀 Advanced Features

- Per-tool notification control
- Quiet hours with plugin-specific muting
- Activity logging and rotation
- Sound categories and custom mappings
- Debug mode for development

---

**Ready in 30 seconds!** Run the installer and start getting notifications from Claude Code.