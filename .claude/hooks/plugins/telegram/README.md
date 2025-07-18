# Telegram Notification Plugin

Sends notifications to Telegram via bot API.

## Features

- 📱 Send notifications to Telegram chat
- 🤖 Custom bot token and chat ID
- 📝 Markdown message formatting
- 🔄 Automatic retry on network errors
- 🎯 Multi-language support

## Quick Setup

1. **Create a Telegram bot:**
   - Message @BotFather on Telegram
   - Use `/newbot` command
   - Get your bot token

2. **Get your chat ID:**
   - Start conversation with your bot
   - Send a message
   - Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Find your chat ID in the response

3. **Configure credentials:**
   Edit `config.yaml`:
   ```yaml
   bot_token: "YOUR_BOT_TOKEN_HERE"
   chat_id: "YOUR_CHAT_ID_HERE"
   ```

4. **Install dependencies:**
   ```bash
   pip install python-telegram-bot PyYAML
   ```

## Configuration

Edit `config.yaml`:

```yaml
# Telegram bot settings
bot_token: "1234567890:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
chat_id: "987654321"

# Message settings
message_format: "🤖 Claude Code: {message}"
use_markdown: true

# Error handling
retry_attempts: 3
timeout_seconds: 10
```

## Alternative Configuration Methods

### Environment Variables
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### JSON Credentials (legacy)
```bash
export TELEGRAM_CREDENTIALS='{"bot_token":"your_token","chat_id":"your_chat_id"}'
```

## Troubleshooting

- **No messages:** Check bot token and chat ID
- **403 Forbidden:** Send `/start` to your bot first
- **Network errors:** Messages will retry automatically
- **Wrong format:** Verify credentials are strings, not numbers