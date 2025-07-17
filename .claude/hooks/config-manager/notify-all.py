#!/usr/bin/env python3
"""
Dinamik plugin tabanlı bildirim sistemi
Config'e göre tüm notification plugin'lerini çalıştırır
"""
import sys
import subprocess
import os
import json
import datetime

def load_config():
    """Notification config'ini yükle"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "notification-config.json")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Varsayılan config - güncel yapıya uygun
        return {
            "notifications": {
                "sound": {
                    "enabled": True, 
                    "script": "voice-notifier/smart-notification.py",
                    "events": {"Stop": True, "Notification": True, "PreToolUse": True}
                },
                "telegram": {
                    "enabled": False,  # Varsayılan olarak kapalı (credentials gerekiyor)
                    "script": "telegram-bot/telegram-notifier.py",
                    "events": {"Stop": True, "Notification": True}
                },
                "desktop_toast": {
                    "enabled": True,
                    "script": "toast-notifier/cross-platform-notifier.py",
                    "events": {"Stop": True, "Notification": True}
                }
            },
            "quiet_hours": {"enabled": False},
            "culture": {"language": "en"}
        }

def is_quiet_hours(config):
    """Sessiz saat kontrolü"""
    quiet = config.get("quiet_hours", {})
    if not quiet.get("enabled", False):
        return False
    
    now = datetime.datetime.now().time()
    start = datetime.datetime.strptime(quiet["start"], "%H:%M").time()
    end = datetime.datetime.strptime(quiet["end"], "%H:%M").time()
    
    if start <= end:
        return start <= now <= end
    else:  # Gece yarısını geçiyor
        return now >= start or now <= end

def should_run_plugin(plugin_name, quiet_mode, quiet_config):
    """Plugin'in quiet hours'da çalışıp çalışmayacağını kontrol et"""
    if not quiet_mode:
        return True
    
    # Mute listesinde varsa çalıştırma
    if plugin_name in quiet_config.get("mute", []):
        return False
    
    # Allow listesinde varsa çalıştır
    if plugin_name in quiet_config.get("allow", []):
        return True
    
    # Ne mute ne allow'da yoksa, varsayılan davranış: çalıştırma
    return False


def main():
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    event_type = sys.argv[2] if len(sys.argv) > 2 else "PreToolUse"
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config()
    
    # Sessiz saat kontrolü
    quiet_mode = is_quiet_hours(config)
    quiet_config = config.get("quiet_hours", {})
    
    # Tüm notification plugin'lerini işle
    notifications = config.get("notifications", {})
    
    for plugin_name, plugin_config in notifications.items():
        # Örnek plugin'leri atla
        if plugin_name.startswith("_"):
            continue
            
        # Plugin aktif mi?
        if not plugin_config.get("enabled", False):
            continue
            
        # Bu event için bildirim gönderilecek mi?
        # Önce tool-specific kontrol
        tools_config = plugin_config.get("tools", {})
        if tools_config.get("enabled", False):
            # Tool-level kontrol aktif
            # 1. Whitelist kontrolü
            whitelist = tools_config.get("whitelist", [])
            if whitelist and tool_name not in whitelist:
                continue
                
            # 2. Blacklist kontrolü
            blacklist = tools_config.get("blacklist", [])
            if blacklist and tool_name in blacklist:
                continue
                
            # 3. Custom tool settings kontrolü
            custom_tools = tools_config.get("custom", {})
            if tool_name in custom_tools:
                # Bu tool için özel ayar var
                tool_events = custom_tools[tool_name]
                if not tool_events.get(event_type, False):
                    continue
            else:
                # Tool için özel ayar yok, genel event ayarını kullan
                if not plugin_config.get("events", {}).get(event_type, False):
                    continue
        else:
            # Tool-level kontrol kapalı, sadece genel event kontrolü
            if not plugin_config.get("events", {}).get(event_type, False):
                continue
            
        # Quiet hours kontrolü
        if not should_run_plugin(plugin_name, quiet_mode, quiet_config):
            print(f"{plugin_name} sessiz saatlerde kapalı")
            continue
        
        # Script yolu belirtilmemiş mi?
        script_path = plugin_config.get("script")
        if not script_path:
            print(f"{plugin_name} için script yolu belirtilmemiş")
            continue
        
        # Script yolu absolute veya relative olabilir
        if os.path.isabs(script_path):
            # Güvenlik: Absolute path'leri de kontrol et
            if '..' in script_path:
                print(f"Güvenlik: Path traversal tespit edildi: {script_path}")
                continue
            # Absolute path - olduğu gibi kullan
            final_script_path = script_path
        else:
            # Güvenlik: Path traversal kontrolü
            if '..' in script_path or script_path.startswith('/') or script_path.startswith('\\'):
                print(f"Güvenlik: Geçersiz script yolu: {script_path}")
                continue
            # Relative path - .claude/hooks/ dizinine göre
            # Path separator'ı normalize et (Windows/Unix uyumluluğu)
            script_path = script_path.replace('/', os.sep).replace('\\', os.sep)
            final_script_path = os.path.normpath(os.path.join(script_dir, "..", script_path))
        
        # Script'i çalıştır - güvenlik kontrolleri ile
        try:
            # Script'in varlığını ve güvenliğini kontrol et
            if not os.path.exists(final_script_path):
                print(f"Uyarı: Script bulunamadı: {final_script_path}")
                continue
                
            if not final_script_path.endswith('.py'):
                print(f"Güvenlik: Sadece .py dosyaları çalıştırılabilir: {final_script_path}")
                continue
            
            # Ek parametreler varsa onları da geç
            cmd = [sys.executable, final_script_path, tool_name, event_type]
            
            # Plugin'e özel ekstra parametreler
            extra_params = plugin_config.get("params", [])
            if extra_params:
                cmd.extend(extra_params)
            
            subprocess.run(cmd)
            
        except Exception as e:
            print(f"{plugin_name} hatası: {e}")

if __name__ == "__main__":
    main()