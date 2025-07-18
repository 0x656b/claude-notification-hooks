# Sound Notification Plugin

Plays audio notifications for Claude Code events using MP3 files or system beeps.

## Features

- 🎵 MP3 sound files for different tools and events
- 🔊 System beep fallback when MP3 files are missing
- 🎚️ Volume control
- 🔇 Silent mode for undefined tools
- 🏷️ Tool categorization for easier management

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install pygame PyYAML
   ```

2. **Add MP3 files (optional):**
   - Place your MP3 files in the audio directory (default: `voice/`)
   - Files should match the names in `config.yaml`
   - System beeps will be used if MP3 files are missing

3. **Configure sounds:**
   - Edit `config.yaml` to customize tool-to-sound mappings
   - Change `audio_directory` to switch voice sets
   - Adjust volume and beep settings

## Configuration

Edit `config.yaml`:

```yaml
# Sound settings
volume: 100
audio_directory: "voice"  # Change to: female_tr, male_en, custom, etc.

tool_sounds:
  Bash: "bash.mp3"
  Edit: "editing.mp3"
  # Add more tools...

# Beep fallback
beep_fallback:
  enabled: true
  settings:
    Edit: {frequency: 900, duration: 250}
```

## Audio Directory Options

- `voice/` - Default directory (system beeps if no MP3s)
- `female_tr/` - Turkish female voice
- `male_tr/` - Turkish male voice  
- `female_en/` - English female voice
- `male_en/` - English male voice
- `custom/` - Your custom sound files

## Included MP3 Files

- `bash.mp3` - Command execution
- `editing.mp3` - File editing
- `listing.mp3` - File reading/listing
- `commit.mp3` - Git operations
- `stop.mp3` - Task completion
- `ready.mp3` - System ready
- `error.mp3` - Error notifications

## Troubleshooting

- **No sound:** Check if pygame is installed and volume is up
- **Wrong sound:** Verify tool names match exactly in config.yaml
- **Beep instead of MP3:** Add MP3 files to the voice/ directory