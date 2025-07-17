# Using Claude Code Hooks in GitHub Actions

[🇹🇷 Türkçe](GITHUB_ACTIONS_TR.md)

This guide shows how to integrate the Claude Code Hook Notification System into your GitHub Actions workflows.

## 🚀 Quick Start

### Minimal Setup (Just Notifications)

If you only want notifications in your CI/CD pipeline:

1. **Copy only what you need** to your repo:
   ```
   .claude/hooks/telegram-bot/telegram-notifier.py
   .claude/hooks/config-manager/notify-all.py
   .claude/hooks/config-manager/notification-config.json
   ```

2. **Add secrets** to your GitHub repository:
   - Go to Settings → Secrets → Actions
   - Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

3. **Use in your workflow**:
   ```yaml
   - name: Notify build start
     run: |
       python3 .claude/hooks/telegram-bot/telegram-notifier.py "Build" "Start"
   ```

## 📋 Complete Integration Examples

### Example 1: Simple Build Notifications

See [`.github/workflows/simple-example.yml`](../.github/workflows/simple-example.yml) for a basic integration that sends Telegram notifications during build steps.

### Example 2: Full Claude Code Integration

See [`.github/workflows/claude-code-example.yml`](../.github/workflows/claude-code-example.yml) for a complete example that:
- Responds to PR comments with `/claude` commands
- Runs Claude Code with specific tasks
- Posts results back to GitHub comments
- Sends Telegram/Discord notifications
- Uploads logs as artifacts

## 🔧 Configuration Options

### Environment Variables

The notification system reads these environment variables in CI:

```yaml
env:
  # For Telegram
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  
  # For GitHub comment notifications
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  GITHUB_REPOSITORY: ${{ github.repository }}
  ISSUE_NUMBER: ${{ github.event.issue.number }}
```

### CI-Specific Configuration

Create a CI-specific config to disable sound and enable only relevant notifications:

```python
config = {
    'notifications': {
        'sound': {
            'enabled': False,  # No sound in CI
        },
        'telegram': {
            'enabled': True,
            'events': {
                'Stop': True,
                'Notification': True
            }
        },
        'github_comment': {
            'enabled': True,
            'script': 'github-actions/comment-notifier.py',
            'events': {
                'Stop': True
            }
        }
    },
    'quiet_hours': {'enabled': False},
    'logging': {'enabled': True},
    'culture': {'language': 'en'}  # or 'tr' for Turkish
}
```

## 🎯 Use Cases

### 1. Long-Running Tasks
Notify when time-consuming operations complete:

```yaml
- name: Run integration tests
  run: |
    python3 notify.py "IntegrationTests" "Start"
    npm run test:integration  # This takes 20 minutes
    python3 notify.py "IntegrationTests" "Stop"
```

### 2. Deployment Notifications
Alert team when deployments happen:

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main'
  run: |
    python3 notify.py "Deploy" "Notification"
    ./deploy.sh
    python3 notify.py "Deploy" "Stop"
```

### 3. Error Notifications
Send alerts on failures:

```yaml
- name: Build
  id: build
  run: npm run build
  
- name: Notify failure
  if: failure()
  run: |
    python3 notify.py "Build" "Error"
```

### 4. Claude Code Automation
Trigger Claude Code from PR comments:

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  claude-task:
    if: contains(github.event.comment.body, '/claude')
    runs-on: ubuntu-latest
    steps:
      # ... setup ...
      - name: Run Claude
        run: |
          TASK="${{ github.event.comment.body }}"
          TASK=${TASK#/claude }  # Remove prefix
          claude-code --task "$TASK" --hooks-enabled
```

## 🛠️ Custom GitHub Actions Notifier

Create a custom notifier that posts to PR comments:

```python
# .claude/hooks/github-actions/comment-notifier.py
import os
import json
import urllib.request

def post_comment(message):
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    pr_number = os.environ.get('PR_NUMBER')
    
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
    data = json.dumps({'body': message}).encode()
    req = urllib.request.Request(url, data=data, headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    })
    
    urllib.request.urlopen(req)
```

## 🔒 Security Best Practices

1. **Never commit credentials** - Always use GitHub Secrets
2. **Limit token permissions** - Use minimal scopes
3. **Validate inputs** - Sanitize PR comments before processing
4. **Use environment restrictions** - Limit secrets to specific environments

## 📊 Status Badges

Add status badges to your README:

```markdown
![Claude Code Notifications](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/claude-code-example.yml/badge.svg)
```

## 🤖 Bot Commands

If implementing PR comment commands:

- `/claude review` - Code review
- `/claude test` - Add missing tests  
- `/claude docs` - Update documentation
- `/claude fix-lint` - Fix linting issues

## 💡 Tips

1. **Parallel notifications**: Use `&` to send notifications without blocking:
   ```bash
   python3 notify.py "Build" "Start" &
   ```

2. **Conditional notifications**: Only notify on main branch:
   ```yaml
   if: github.ref == 'refs/heads/main'
   ```

3. **Matrix notifications**: Different notifications per OS:
   ```yaml
   strategy:
     matrix:
       os: [ubuntu-latest, windows-latest]
   ```

4. **Scheduled notifications**: For regular tasks:
   ```yaml
   on:
     schedule:
       - cron: '0 9 * * 1'  # Weekly on Monday
   ```

## 🔍 Debugging

Enable debug logging:

```yaml
- name: Run with debug
  env:
    ACTIONS_STEP_DEBUG: true
  run: |
    python3 -u notify.py "Debug" "Test"
```

Check webhook deliveries:
- GitHub: Settings → Webhooks → Recent Deliveries
- Telegram: Use `/getUpdates` API endpoint
- Discord: Check webhook logs in server settings

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Discord Webhooks](https://discord.com/developers/docs/resources/webhook)