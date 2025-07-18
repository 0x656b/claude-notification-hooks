#!/usr/bin/env python3
"""
Cross-platform Toast Notification System
Windows, Mac, Linux destekler
"""
import os
import sys
import datetime
import subprocess
import json

def load_config():
    """Load plugin config (YAML first, then JSON fallback)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try YAML first
    yaml_config = os.path.join(script_dir, "config.yaml")
    try:
        import yaml
        with open(yaml_config, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        pass  # PyYAML not installed
    except (FileNotFoundError, Exception):
        pass  # YAML config not found
    
    # Fallback to JSON or defaults
    return {
        "title": "Claude Code",
        "duration": 5,
        "icon": ""
    }

# Platform utils'i import et
try:
    from platform_utils import get_platform, get_notification_command
except ImportError:
    # Fallback implementations
    def get_platform():
        import platform
        return platform.system().lower()
    
    def get_notification_command():
        return None

# Emoji mapping
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
        "subtask_completed": "Alt görev tamamlandı",
        "claude_finished": "Claude işini bitirdi",
        "claude_asking": "Claude soru soruyor",
        "task_finished": "görevi bitti",
        "starting": "başlıyor",
        "running": "Araç çalıştırılıyor",
        "completed": "bitti",
        "tool_completed": "Araç tamamlandı"
    },
    "en": {
        "work_completed": "Work completed!",
        "attention_needed": "Attention required!",
        "subtask_completed": "Subtask completed",
        "claude_finished": "Claude finished",
        "claude_asking": "Claude needs attention",
        "task_finished": "task finished",
        "starting": "starting",
        "running": "Tool running",
        "completed": "finished",
        "tool_completed": "Tool completed"
    }
}

def load_config():
    """Config dosyasını yükle"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.normpath(os.path.join(script_dir, "..", "config-manager", "notification-config.json"))
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"culture": {"language": "en"}}

def create_notification(tool_name="default", event_type="PreToolUse"):
    """Tool'a göre bildirim oluştur"""
    
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
    
    if event_type == "Stop":
        title = f"{emoji} {msgs['work_completed']}"
        message = f"📁 {project_folder}\n💬 {msgs['claude_finished']}\n🕐 {timestamp}"
    elif event_type == "Notification":
        title = f"{emoji} {msgs['attention_needed']}"
        message = f"📁 {project_folder}\n❓ {msgs['claude_asking']}\n🕐 {timestamp}"
    elif event_type == "SubagentStop":
        title = f"{emoji} {msgs['subtask_completed']}"
        message = f"📁 {project_folder}\n✅ {tool_name} {msgs['task_finished']}\n🕐 {timestamp}"
    elif event_type == "PreToolUse":
        title = f"{emoji} {tool_name} {msgs['starting']}"
        message = f"📁 {project_folder}\n🔧 {msgs['running']}\n🕐 {timestamp}"
    elif event_type == "PostToolUse":
        title = f"{emoji} {tool_name} {msgs['completed']}"
        message = f"📁 {project_folder}\n✅ {msgs['tool_completed']}\n🕐 {timestamp}"
    else:
        title = f"{emoji} {event_type}"
        message = f"📁 {project_folder}\n🔧 {tool_name}\n🕐 {timestamp}"
    
    return title, message

def show_notification(title, message):
    """Platform'a göre bildirim göster"""
    platform = get_platform()
    
    try:
        if platform == 'windows':
            # Windows - plyer kullan
            try:
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    app_name="Claude Code",
                    timeout=10
                )
            except ImportError:
                # plyer yoksa windows-toasts dene
                try:
                    from windows_toasts import WindowsToaster, Toast, ToastDisplayImage
                    toaster = WindowsToaster('Claude Code')
                    toast = Toast()
                    toast.text_fields = [title, message]
                    toast.on_dismissed = lambda _: print('Toast dismissed')
                    toaster.show_toast(toast)
                except ImportError:
                    print(f"Windows bildirim hatası - plyer veya windows-toasts yüklü değil")
                    
        elif platform == 'macos':
            # macOS - osascript kullan
            # Güvenli subprocess kullanımı
            subprocess.run([
                'osascript', '-e', 
                f'display notification "{message}" with title "{title}"'
            ], capture_output=True)
            
        elif platform == 'linux':
            # Linux - notify-send kullan
            subprocess.run(['notify-send', title, message], capture_output=True)
            
        return True
        
    except Exception as e:
        print(f"Bildirim hatası ({platform}): {e}")
        return False

def main():
    # Komut satırı parametreleri
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    event_type = sys.argv[2] if len(sys.argv) > 2 else "PreToolUse"
    
    # Bildirim oluştur
    title, message = create_notification(tool_name, event_type)
    
    # Sadece önemli event'lerde bildirim göster
    important_events = ["Stop", "Notification", "SubagentStop"]
    if event_type in important_events:
        if show_notification(title, message):
            print(f"{get_platform()} bildirimi gösterildi: {event_type}")
        else:
            print(f"{get_platform()} bildirimi gösterilemedi: {event_type}")

if __name__ == "__main__":
    main()