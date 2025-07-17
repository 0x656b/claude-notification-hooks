#!/usr/bin/env python3
"""
Config'e göre activity log tutar
"""
import sys
import os
import json
import datetime

def load_config():
    """Config dosyasını yükle"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "notification-config.json")
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"logging": {"enabled": True}}

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
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    
    config = load_config()
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
            f.write(f"[{timestamp}] Tool completed: {tool_name}\n")

if __name__ == "__main__":
    main()