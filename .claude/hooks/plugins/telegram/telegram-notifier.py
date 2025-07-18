#!/usr/bin/env python3
"""
Claude Code Telegram Notification System
Telegram'a bildirim gönderir
"""
import os
import sys
import datetime
import asyncio
import json
from telegram import Bot
from telegram.error import TelegramError

# Telegram ayarları - önce environment'tan kontrol et
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Eğer environment'ta yoksa, TELEGRAM_CREDENTIALS ortam değişkeninden JSON olarak al
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    telegram_creds = os.environ.get("TELEGRAM_CREDENTIALS", "")
    if telegram_creds:
        try:
            creds = json.loads(telegram_creds)
            TELEGRAM_BOT_TOKEN = creds.get("bot_token", "")
            TELEGRAM_CHAT_ID = creds.get("chat_id", "")
        except json.JSONDecodeError:
            pass  # Silently ignore JSON errors

# Environment'ta yoksa, config dosyasından oku
if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try YAML first
    yaml_config_path = os.path.join(script_dir, "config.yaml")
    try:
        import yaml
        with open(yaml_config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            TELEGRAM_BOT_TOKEN = config.get("bot_token", "")
            TELEGRAM_CHAT_ID = config.get("chat_id", "")
    except ImportError:
        pass  # PyYAML not installed
    except (FileNotFoundError, Exception):
        pass  # YAML config not found
    
    # Fallback to JSON
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        config_path = os.path.join(script_dir, "telegram-config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    TELEGRAM_BOT_TOKEN = config.get("bot_token", "")
                    TELEGRAM_CHAT_ID = config.get("chat_id", "")
            except (FileNotFoundError, json.JSONDecodeError, IOError):
                pass  # Config file not found or invalid

# Hala yoksa placeholder kullan
if not TELEGRAM_BOT_TOKEN:
    TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
if not TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

# Emoji mapping - Tool'lar için
EMOJI_MAP = {
    "Bash": "🖥️",
    "Edit": "✏️",
    "Read": "📖",
    "Write": "📝",
    "MultiEdit": "📝",
    "Grep": "🔍",
    "LS": "📁",
    "Glob": "🔍",
    "Task": "📋",
    "TodoWrite": "✅",
    "WebSearch": "🌐",
    "WebFetch": "🌐",
    "NotebookRead": "📓",
    "NotebookEdit": "📓",
    "Stop": "✅",
    "Notification": "🔔",
    "SubagentStop": "🏁",
    "default": "🤖"
}

# Çok dilli mesajlar
MESSAGES = {
    "tr": {
        "work_completed": "İş tamamlandı!",
        "attention_needed": "Dikkat gerekiyor!",
        "subtask_completed": "Alt görev tamamlandı!",
        "claude_finished": "Claude işini bitirdi, PC başına dönebilirsin!",
        "claude_asking": "Claude soru soruyor veya onay bekliyor!",
        "task_finished": "görevi bitti!",
        "running": "çalıştırılıyor...",
        "completed": "tamamlandı",
        "tool_running": "Araç çalıştırılıyor",
        "tool_completed": "Araç tamamlandı"
    },
    "en": {
        "work_completed": "Work completed!",
        "attention_needed": "Attention required!",
        "subtask_completed": "Subtask completed!",
        "claude_finished": "Claude finished, you can return to your PC!",
        "claude_asking": "Claude is asking a question or waiting for confirmation!",
        "task_finished": "task completed!",
        "running": "running...",
        "completed": "completed",
        "tool_running": "Tool running",
        "tool_completed": "Tool completed"
    }
}

async def send_telegram_message(message):
    """Telegram'a mesaj gönder"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='HTML'
        )
        return True
    except Exception as e:
        print(f"Telegram hatası: {e}")
        return False

def load_config():
    """Config dosyasını yükle"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.normpath(os.path.join(script_dir, "..", "config-manager", "notification-config.json"))
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"culture": {"language": "en"}}

def create_message(tool_name="default", event_type="PreToolUse"):
    """Tool'a göre mesaj oluştur"""
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Event'e göre emoji seç (SubagentStop gibi durumlar için)
    if event_type in EMOJI_MAP:
        emoji = EMOJI_MAP[event_type]
    else:
        emoji = EMOJI_MAP.get(tool_name, EMOJI_MAP["default"])
    
    # Config'den dili al
    config = load_config()
    lang = config.get("culture", {}).get("language", "en")
    
    # Geçerli dil değilse default'a dön
    if lang not in MESSAGES:
        lang = "en"
    
    msgs = MESSAGES[lang]
    
    # Proje klasörünü al
    project_folder = os.path.basename(os.getcwd())
    project_path = os.getcwd()
    
    if event_type == "Stop":
        message = f"{emoji} <b>{msgs['work_completed']}</b>\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"📍 <code>{project_path}</code>\n"
        message += f"🕐 {timestamp}\n"
        message += f"💬 {msgs['claude_finished']}"
    elif event_type == "Notification":
        message = f"{emoji} <b>{msgs['attention_needed']}</b>\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"🕐 {timestamp}\n"
        message += f"❓ {msgs['claude_asking']}"
    elif event_type == "SubagentStop":
        message = f"{emoji} <b>{msgs['subtask_completed']}</b>\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"📍 <code>{project_path}</code>\n"
        message += f"🕐 {timestamp}\n"
        message += f"✅ {tool_name} {msgs['task_finished']}"
    elif event_type == "PreToolUse":
        message = f"{emoji} <code>{tool_name}</code> {msgs['running']}\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"🕐 {timestamp}"
    elif event_type == "PostToolUse":
        message = f"{emoji} <code>{tool_name}</code> {msgs['completed']}\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"🕐 {timestamp}"
    else:
        # Bilinmeyen event'ler için de standart format
        message = f"{emoji} <b>{event_type}</b>\n"
        message += f"📁 <code>{project_folder}</code>\n"
        message += f"🔧 <code>{tool_name}</code>\n"
        message += f"🕐 {timestamp}"
    
    return message

async def main():
    # Komut satırı parametreleri
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    event_type = sys.argv[2] if len(sys.argv) > 2 else "PreToolUse"
    
    # Token kontrolü
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ Telegram bot token'ı ayarlanmamış!")
        return
    
    # Mesajı oluştur ve gönder
    message = create_message(tool_name, event_type)
    
    # Sadece önemli event'lerde bildirim gönder (opsiyonel)
    important_events = ["Stop", "Notification", "SubagentStop"]
    if event_type in important_events:
        success = await send_telegram_message(message)
        if success:
            print(f"Telegram bildirimi gönderildi: {event_type}")
        else:
            print(f"Telegram bildirimi gönderilemedi: {event_type}")

if __name__ == "__main__":
    asyncio.run(main())