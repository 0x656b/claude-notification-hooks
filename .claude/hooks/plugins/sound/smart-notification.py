#!/usr/bin/env python3
"""
Claude Code Smart Notification System
Tool'lara göre farklı sesler çalar - Cross-platform
"""
import os
import sys
import datetime
import json

# Platform utils'i import et
try:
    from platform_utils import get_platform, get_sound_player, get_beep_command
except ImportError:
    # Fallback implementations
    def get_platform():
        import platform
        return platform.system().lower()
    
    def get_sound_player():
        return None
    
    def get_beep_command():
        return None

# Platform-specific imports
platform = get_platform()
if platform == 'windows':
    try:
        import pygame
        import winsound
    except ImportError:
        pygame = None
        winsound = None

def get_script_dir():
    """Script'in bulunduğu klasörü al"""
    return os.path.dirname(os.path.abspath(__file__))

def load_sound_mapping():
    """Ses mapping config'ini yükle (YAML format)"""
    script_dir = get_script_dir()
    
    # Try YAML first
    yaml_file = os.path.join(script_dir, "config.yaml")
    try:
        import yaml
        with open(yaml_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except ImportError:
        print("PyYAML not installed, falling back to JSON config")
    except (FileNotFoundError, Exception):
        pass
    
    # Fallback to JSON
    mapping_file = os.path.join(script_dir, "sound-mapping.json")
    try:
        import json
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Varsayılan mapping
        return {
            "tool_sounds": {"Bash": "bash.mp3", "Edit": "editing.mp3"},
            "event_sounds": {"Stop": "ready.mp3", "Notification": "ready.mp3"},
            "default_sound": "ready.mp3",
            "beep_fallback": {"enabled": True, "settings": {"default": {"frequency": 1000, "duration": 300}}}
        }

def load_config():
    """Config dosyasını yükle"""
    script_dir = get_script_dir()
    # Try core config first
    core_config = os.path.join(script_dir, "..", "..", "core", "config.yaml")
    try:
        import yaml
        with open(core_config, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except (ImportError, FileNotFoundError, Exception):
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

def play_sound_for_tool(tool_name="default", event_type="PreToolUse"):
    """Tool'a göre uygun sesi çal"""
    
    script_dir = get_script_dir()
    
    # Load sound config to get audio directory
    sound_config = load_sound_mapping()
    audio_directory = sound_config.get("audio_directory", "voice")
    voice_dir = os.path.join(script_dir, audio_directory)
    
    log_file = os.path.join(script_dir, "..", "notifications.log")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config = load_config()
    logging_enabled = config.get("logging", {}).get("enabled", True)
    
    # Sound mapping'i yükle
    sound_mapping = load_sound_mapping()
    
    try:
        # Ses dosyasını belirle
        sound_file = None
        
        # Önce event_sounds'a bak (Stop, Error gibi özel durumlar için)
        if event_type in sound_mapping.get("event_sounds", {}) and sound_mapping["event_sounds"][event_type] is not None:
            sound_file = sound_mapping["event_sounds"][event_type]
        # Sonra tool_sounds'a bak
        elif tool_name in sound_mapping.get("tool_sounds", {}):
            sound_file = sound_mapping["tool_sounds"][tool_name]
        # Tanımlı değilse sessiz geç (varsayılan sesi kullanma)
        else:
            # Eğer event_type PreToolUse/PostToolUse ise ve tool tanımlı değilse, sessiz geç
            if event_type in ["PreToolUse", "PostToolUse"]:
                message = f"[{timestamp}] {event_type}: {tool_name} → 🔇 Tanımsız tool, sessiz"
                if logging_enabled:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(message + "\n")
                return  # Sessiz çık
            # Diğer durumlarda varsayılan sesi kullan
            else:
                sound_file = sound_mapping.get("default_sound", "ready.mp3")
            
        sound_path = os.path.join(voice_dir, sound_file)
        
        # Log başlat
        message = f"[{timestamp}] {event_type}: {tool_name}"
        
        if os.path.exists(sound_path):
            # MP3 çal - platform'a göre
            if platform == 'windows':
                # Windows - pygame kullan (eğer yüklüyse)
                if pygame:
                    # pygame mixer'ı sadece initialize edilmemişse başlat
                    if not pygame.mixer.get_init():
                        pygame.mixer.init()
                    
                    pygame.mixer.music.load(sound_path)
                    pygame.mixer.music.play()
                    
                    # Ses bitene kadar bekle (max 5 saniye)
                    import time
                    max_wait = 5
                    start_time = time.time()
                    while pygame.mixer.music.get_busy() and (time.time() - start_time) < max_wait:
                        time.sleep(0.1)
                else:
                    # pygame yoksa beep kullan
                    if winsound:
                        winsound.Beep(1000, 300)
            else:
                # Mac/Linux - komut satırı player kullan
                player_cmd = get_sound_player()
                if player_cmd:
                    # Güvenli subprocess kullanımı
                    import subprocess
                    import shlex
                    # Player komutu ve dosya yolunu ayrı ayrı geç
                    if 'afplay' in player_cmd:
                        subprocess.run(['afplay', sound_path], capture_output=True)
                    elif 'paplay' in player_cmd:
                        subprocess.run(['paplay', sound_path], capture_output=True)
                    elif 'aplay' in player_cmd:
                        subprocess.run(['aplay', '-q', sound_path], capture_output=True)
                    elif 'mpg123' in player_cmd:
                        subprocess.run(['mpg123', '-q', sound_path], capture_output=True)
                    else:
                        # Fallback - ama yine de güvenli
                        cmd_parts = shlex.split(player_cmd.format(file=shlex.quote(sound_path)))
                        subprocess.run(cmd_parts, capture_output=True)
            
            message += f" → 🎵 {sound_file}"
        else:
            # MP3 yoksa beep (eğer aktifse)
            beep_config = sound_mapping.get("beep_fallback", {})
            if beep_config.get("enabled", True):
                beep_settings = beep_config.get("settings", {})
                
                # Önce event_type için ayar ara
                if event_type in beep_settings:
                    freq = beep_settings[event_type].get("frequency", 1000)
                    dur = beep_settings[event_type].get("duration", 300)
                # Sonra tool_name için
                elif tool_name in beep_settings:
                    freq = beep_settings[tool_name].get("frequency", 1000)
                    dur = beep_settings[tool_name].get("duration", 300)
                # Varsayılan
                else:
                    default = beep_settings.get("default", {})
                    freq = default.get("frequency", 1000)
                    dur = default.get("duration", 300)
                
                # Platform'a göre beep
                if platform == 'windows' and winsound:
                    winsound.Beep(freq, dur)
                else:
                    beep_cmd = get_beep_command()
                    if beep_cmd:
                        import subprocess
                        # Güvenli subprocess kullanımı
                        subprocess.run(beep_cmd, shell=True, capture_output=True)
                
                message += " → 🔊 Beep"
            else:
                message += " → 🔇 Sessiz"
        
        # Log yaz (eğer aktifse)
        if logging_enabled:
            # Boyut kontrolü
            max_size = config.get("logging", {}).get("max_size_mb", 10)
            if config.get("logging", {}).get("rotate", True):
                check_log_size(log_file, max_size)
            
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(message + "\n")
            
    except Exception as e:
        if logging_enabled:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] ❌ Hata: {str(e)}\n")

if __name__ == "__main__":
    # Komut satırı parametreleri
    tool_name = sys.argv[1] if len(sys.argv) > 1 else "default"
    event_type = sys.argv[2] if len(sys.argv) > 2 else "PreToolUse"
    
    play_sound_for_tool(tool_name, event_type)