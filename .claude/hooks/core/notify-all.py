#!/usr/bin/env python3
"""
Universal Hook Handler v3.0
Claude Code hook'larından gelen JSON stdin'i parse ederek tüm notification plugin'lerini çalıştırır.
"""
import sys
import subprocess
import os
import datetime
import json

def load_hook_data():
    """Hook'tan gelen JSON data'yı parse et"""
    try:
        # stdin'den raw bytes oku (encoding fix için)
        raw_bytes = sys.stdin.buffer.read()
        
        # CP1254 (Windows Turkish) encoding fix
        try:
            stdin_data = raw_bytes.decode('cp1254', errors='replace').strip()
        except:
            # Fallback: UTF-8 with surrogate cleanup
            try:
                stdin_data = raw_bytes.decode('utf-8', errors='replace').strip()
            except:
                stdin_data = raw_bytes.decode('latin1', errors='replace').strip()
        
        # JSON parse et
        if stdin_data:
            hook_data = json.loads(stdin_data)
            return hook_data
        else:
            return {"error": "No stdin data"}
            
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse failed: {e}"}
    except Exception as e:
        return {"error": f"Hook data load failed: {e}"}

def load_config():
    """Core config'ini yükle (YAML format)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.yaml")
    
    try:
        import yaml
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # v3.0 format: plugin structure
        if 'plugins' in config:
            return config
        else:
            # Backward compatibility
            return {
                "plugins": config.get("notifications", {}),
                "quiet_hours": config.get("quiet_hours", {"enabled": False}),
                "logging": config.get("logging", {"enabled": False}),
                "culture": config.get("culture", {"language": "en"})
            }
            
    except ImportError:
        return load_json_fallback()
    except (FileNotFoundError, Exception):
        return load_json_fallback()

def load_json_fallback():
    """JSON fallback for backward compatibility"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "notification-config.json")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            old_config = json.load(f)
        
        return {
            "plugins": old_config.get("notifications", {}),
            "quiet_hours": old_config.get("quiet_hours", {"enabled": False}),
            "logging": old_config.get("logging", {"enabled": False}),
            "culture": old_config.get("culture", {"language": "en"})
        }
    except:
        # Default config if nothing found
        return {
            "plugins": {},
            "quiet_hours": {"enabled": False},
            "logging": {"enabled": False},
            "culture": {"language": "en"}
        }

def should_notify(plugin_config, hook_data, config):
    """Plugin'in notification göndermesi gerekip gerekmediğini kontrol et"""
    
    # Plugin enabled mi?
    if not plugin_config.get("enabled", True):
        return False
        
    # Event type kontrolü
    event_type = hook_data.get("hook_event_name", "")
    events = plugin_config.get("events", {})
    
    if event_type not in events or not events[event_type]:
        return False
    
    # Tool-level kontrolü (varsa)
    tool_name = hook_data.get("tool_name", "")
    if tool_name and "tools" in plugin_config:
        tool_config = plugin_config["tools"]
        if "blacklist" in tool_config and tool_name in tool_config["blacklist"]:
            return False
        if "whitelist" in tool_config and tool_config["whitelist"] and tool_name not in tool_config["whitelist"]:
            return False
        if "custom" in tool_config and tool_name in tool_config["custom"]:
            custom_events = tool_config["custom"][tool_name]
            if event_type in custom_events and not custom_events[event_type]:
                return False
    
    # Quiet hours kontrolü
    if is_quiet_hours(config):
        quiet_config = config.get("quiet_hours", {})
        muted_plugins = quiet_config.get("mute", [])
        plugin_key = next((key for key, val in config["plugins"].items() if val == plugin_config), "")
        if plugin_key in muted_plugins:
            return False
    
    return True

def is_quiet_hours(config):
    """Quiet hours aktif mi?"""
    quiet_config = config.get("quiet_hours", {})
    if not quiet_config.get("enabled", False):
        return False
    
    try:
        now = datetime.datetime.now().time()
        start_time = datetime.datetime.strptime(quiet_config.get("start", "23:00"), "%H:%M").time()
        end_time = datetime.datetime.strptime(quiet_config.get("end", "07:00"), "%H:%M").time()
        
        if start_time <= end_time:
            return start_time <= now <= end_time
        else:
            return now >= start_time or now <= end_time
    except:
        return False

def run_plugin(plugin_config, hook_data, config):
    """Plugin script'ini çalıştır"""
    script_path = plugin_config.get("script", "")
    if not script_path:
        return
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_script_path = os.path.join(script_dir, script_path)
    
    if not os.path.exists(full_script_path):
        return
        
    try:
        # Hook data'yı JSON olarak plugin'e gönder
        json_input = json.dumps(hook_data, ensure_ascii=False)
        
        # Event type ve tool name'i argument olarak ver (backward compatibility)
        event_type = hook_data.get("hook_event_name", "Unknown")
        tool_name = hook_data.get("tool_name", event_type)
        
        # Plugin'i çalıştır
        process = subprocess.run(
            ["python3", full_script_path, tool_name, event_type],
            input=json_input,
            text=True,
            capture_output=True,
            timeout=10,
            cwd=script_dir
        )
        
        # Debug plugin için özel durum: console output'u gösterme
        if "debug" not in script_path.lower():
            if process.stderr:
                print(f"Plugin error ({script_path}): {process.stderr}", file=sys.stderr)
                
    except subprocess.TimeoutExpired:
        print(f"Plugin timeout: {script_path}", file=sys.stderr)
    except Exception as e:
        print(f"Plugin failed ({script_path}): {e}", file=sys.stderr)

def main():
    """Ana fonksiyon"""
    # Hook data'yı al
    hook_data = load_hook_data()
    
    if "error" in hook_data:
        print(f"Hook error: {hook_data['error']}", file=sys.stderr)
        return
    
    # Config'i yükle
    config = load_config()
    
    # Her plugin için kontrol et ve çalıştır
    plugins = config.get("plugins", {})
    for plugin_name, plugin_config in plugins.items():
        if should_notify(plugin_config, hook_data, config):
            run_plugin(plugin_config, hook_data, config)

if __name__ == "__main__":
    main()