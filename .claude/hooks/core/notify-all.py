#!/usr/bin/env python3
"""
Dinamik plugin tabanlı bildirim sistemi
Config'e göre tüm notification plugin'lerini çalıştırır
"""
import sys
import subprocess
import os
import datetime

def load_config():
    """Core config'ini yükle (YAML format)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.yaml")
    
    try:
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Backward compatibility: convert new structure to old format
        if 'plugins' in config:
            # Convert new plugin structure to old notification structure
            notifications = {}
            for plugin_name, plugin_config in config['plugins'].items():
                notifications[plugin_name] = plugin_config
            
            # Merge with other config sections
            return {
                "notifications": notifications,
                "quiet_hours": config.get("quiet_hours", {"enabled": False}),
                "logging": config.get("logging", {"enabled": False}),
                "culture": config.get("culture", {"language": "en"})
            }
        else:
            return config
            
    except ImportError:
        print("PyYAML not installed, falling back to JSON config")
        return load_json_config()
    except (FileNotFoundError, Exception):
        print("YAML config not found, falling back to JSON config")
        return load_json_config()

def load_json_config():
    """Fallback: Load old JSON config for backward compatibility"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "notification-config.json")
    
    try:
        import json
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Varsayılan config - güncel yapıya uygun
        return {
            "notifications": {
                "sound": {
                    "enabled": True, 
                    "script": "../plugins/sound/smart-notification.py",
                    "events": {"Stop": True, "Notification": True, "PreToolUse": True}
                },
                "telegram": {
                    "enabled": False,  # Varsayılan olarak kapalı (credentials gerekiyor)
                    "script": "../plugins/telegram/telegram-notifier.py",
                    "events": {"Stop": True, "Notification": True}
                },
                "desktop_toast": {
                    "enabled": True,
                    "script": "../plugins/desktop/cross-platform-notifier.py",
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
    
    # Quiet hours aktif - mute listesindeki plugin'leri kapat
    muted_plugins = quiet_config.get("mute", [])
    return plugin_name not in muted_plugins


def log_activity(tool_name, event_type, config):
    """Activity logging functionality - merged from activity-logger.py"""
    logging_enabled = config.get("logging", {}).get("enabled", True)
    
    if logging_enabled:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_file = os.path.join(script_dir, "..", "activity.log")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Boyut kontrolü
        max_size = config.get("logging", {}).get("max_size_mb", 10)
        if config.get("logging", {}).get("rotate", True):
            check_log_size(log_file, max_size)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {event_type}: {tool_name}\n")

def check_log_size(log_file, max_size_mb):
    """Log dosyası boyutunu kontrol et ve gerekirse rotasyon yap"""
    if os.path.exists(log_file):
        size_mb = os.path.getsize(log_file) / (1024 * 1024)
        if size_mb > max_size_mb:
            # Eski logu yedekle
            import time
            backup_name = log_file + f".{int(time.time())}"
            os.rename(log_file, backup_name)
            # Çok eski yedekleri sil
            import glob
            backups = sorted(glob.glob(log_file + ".*"))
            if len(backups) > 3:  # En fazla 3 yedek tut
                for old_backup in backups[:-3]:
                    os.remove(old_backup)

def main():
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    event_type = sys.argv[2] if len(sys.argv) > 2 else "PreToolUse"
    
    # Debug log
    debug_mode = os.environ.get('CLAUDE_DEBUG', '').lower() == 'true'
    if debug_mode:
        print(f"[DEBUG] Tool: {tool_name}, Event: {event_type}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config = load_config()
    
    # Activity logging for all events
    log_activity(tool_name, event_type, config)
    
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
        # AND logic: events flag && (tools disabled OR tool specific flag)
        
        # 1. Global event flag kontrolü
        global_event_enabled = plugin_config.get("events", {}).get(event_type, False)
        
        # 2. Tool-specific kontrol
        tools_config = plugin_config.get("tools", {})
        tool_specific_enabled = True  # Varsayılan: tool kontrolü yoksa izin ver
        
        if tools_config.get("enabled", False):
            # Tool-level kontrol aktif
            
            # Whitelist kontrolü
            whitelist = tools_config.get("whitelist", [])
            if whitelist and tool_name not in whitelist:
                tool_specific_enabled = False
                
            # Blacklist kontrolü
            blacklist = tools_config.get("blacklist", [])
            if blacklist and tool_name in blacklist:
                tool_specific_enabled = False
                
            # Custom tool settings kontrolü
            custom_tools = tools_config.get("custom", {})
            if tool_name in custom_tools:
                # Bu tool için özel ayar var - AND logic uygula
                tool_event_flag = custom_tools[tool_name].get(event_type, True)
                tool_specific_enabled = tool_event_flag
                if debug_mode:
                    print(f"[DEBUG] {plugin_name}: {tool_name}.{event_type} custom={tool_event_flag}")
        
        # AND logic: Her iki flag da true olmalı
        should_notify = global_event_enabled and tool_specific_enabled
        
        if debug_mode:
            print(f"[DEBUG] {plugin_name}: {tool_name}/{event_type} - global={global_event_enabled}, tool={tool_specific_enabled}, result={should_notify}")
        
        if not should_notify:
            continue
            
        # Quiet hours kontrolü
        if not should_run_plugin(plugin_name, quiet_mode, quiet_config):
            if debug_mode:
                print(f"[DEBUG] {plugin_name} muted during quiet hours")
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
            # Güvenlik: Path traversal kontrolü - aber relative paths within plugins are OK
            if script_path.startswith('/') or script_path.startswith('\\') or script_path.startswith('..'):
                # Allow relative paths within plugins directory
                if script_path.startswith('../plugins/'):
                    # This is a valid plugin path
                    pass
                else:
                    print(f"Güvenlik: Geçersiz script yolu: {script_path}")
                    continue
            # Relative path - .claude/hooks/ dizinine göre
            # Path separator'ı normalize et (Windows/Unix uyumluluğu)
            script_path = script_path.replace('/', os.sep).replace('\\', os.sep)
            final_script_path = os.path.normpath(os.path.join(script_dir, script_path))
        
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