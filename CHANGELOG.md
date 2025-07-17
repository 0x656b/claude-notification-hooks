# Changelog

All notable changes to Claude Code Hook Notification System will be documented in this file.

## [1.0.1] - 2025-01-17

### Added
- **Enhanced sound mapping** - More comprehensive tool-to-sound mappings
  - Added all Claude Code tools (WebSearch, WebFetch, TodoWrite, NotebookEdit, etc.)
  - Category-based organization for easier management
  - Extended event sounds (Start, Success, Error events)
  - Improved beep fallback with tool-specific frequencies
- **Debug mode improvements** - Better debug output for notification flow
- **English comments** - All configuration comments now in English for wider accessibility

### Changed
- **AND logic for notifications** - Notifications now require BOTH global event flag AND tool-specific flag
  - Example: `events.PreToolUse: true` AND `custom.Bash.PreToolUse: true` = notification triggers
  - Provides more precise control over when notifications fire
- **Simplified quiet hours** - Removed redundant `allow` list, only `mute` list needed
  - Plugins not in `mute` list automatically continue working during quiet hours
  - Cleaner, more intuitive configuration
- **Smart sound system** - Undefined tools are now silent during PreToolUse/PostToolUse
  - Only tools explicitly defined in sound-mapping.json will play sounds
  - Stop events always play their designated sound regardless of tool

### Fixed
- Quiet hours logic now correctly mutes specified plugins
- Tool-level notification inheritance issues resolved
- Debug mode now properly shows muted plugins during quiet hours

## [1.0.0] - 2024-01-16

### Added
- **Command-line configuration tool** - Change settings without editing JSON files
  - `configure-notifications.bat` (Windows) and `configure-notifications.sh` (Linux/Mac)
  - Options: `sound:0/1`, `telegram:0/1`, `toast:0/1`, `lang:en/tr`, `quiet:HH:MM-HH:MM`
  - `status` command to show current configuration
- **Debug mode** - Set `CLAUDE_DEBUG=true` to see detailed notification flow
- **debug-hooks.bat** - Tool for troubleshooting notification issues
- **settings-manager** folder - Dedicated folder for configuration tools
- **telegram-config.json.template** - Template file for safe credential management

### Changed
- **Improved security** - Added path traversal protection in notify-all.py
- **Better subprocess handling** - Replaced os.system() with subprocess.run()
- **Unified PreToolUse hooks** - Single hook definition using `%TOOL_NAME%` parameter
- **Enhanced error messages** - More descriptive errors when configuration files are missing

### Fixed
- Hook caching issues on Windows
- Tool-specific notification control now works correctly
- Configuration file path handling for different environments

## [1.0.0] - 2024-01-16

### Initial Release
- Multi-platform notification system (Windows, macOS, Linux)
- Plugin-based architecture
- Audio notifications with MP3/beep fallback
- Telegram bot integration
- Desktop toast notifications
- Multi-language support (English/Turkish)
- Tool-level notification control
- Quiet hours feature
- Comprehensive documentation in English and Turkish
- GitHub Actions integration examples