#!/usr/bin/env python3
"""
HookMonitor Plugin v3.0
Claude Code hook event'lerini izler ve log dosyasına yazar.
Encoding ayarları config.yaml'dan okunur.
"""
import sys
import json
import datetime
import os
import yaml

def load_plugin_config():
    """Plugin config'ini yükle"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(script_dir, "config.yaml")
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        # Fallback default config
        return {
            "enabled": True,
            "log_file": "hook-monitor.log",
            "encoding": {
                "primary": "cp1254",
                "fallback": "utf-8", 
                "final_fallback": "latin1",
                "errors": "replace"
            },
            "output": {
                "emoji_headers": True,
                "timestamps": True,
                "json_indent": 2,
                "truncate_prompt": 100,
                "show_full_json": True
            },
            "events": {
                "UserPromptSubmit": True,
                "PreToolUse": True,
                "PostToolUse": True,
                "Stop": True,
                "SessionStart": True,
                "Notification": True,
                "SubagentStop": True,
                "PreCompact": True
            }
        }

def load_hook_data(config):
    """Hook'tan gelen JSON data'yı config'e göre parse et"""
    try:
        # stdin'den raw bytes oku
        raw_bytes = sys.stdin.buffer.read()
        
        # Config'ten encoding ayarlarını al
        encoding_config = config.get("encoding", {})
        primary_enc = encoding_config.get("primary", "cp1254")
        fallback_enc = encoding_config.get("fallback", "utf-8") 
        final_enc = encoding_config.get("final_fallback", "latin1")
        error_mode = encoding_config.get("errors", "replace")
        
        # Encoding denemeleri
        try:
            stdin_data = raw_bytes.decode(primary_enc, errors=error_mode).strip()
        except:
            try:
                stdin_data = raw_bytes.decode(fallback_enc, errors=error_mode).strip()
            except:
                stdin_data = raw_bytes.decode(final_enc, errors=error_mode).strip()
        
        # JSON parse et - Ultra robust!
        if stdin_data:
            try:
                hook_data = json.loads(stdin_data)
                return hook_data
            except json.JSONDecodeError:
                # JSON parse failed, try cleaning the string
                try:
                    # Remove or replace problematic characters
                    clean_data = ''.join(c for c in stdin_data if ord(c) < 65536)
                    hook_data = json.loads(clean_data)
                    return hook_data
                except:
                    # Last resort: return partial data
                    return {
                        "error": "JSON parse failed",
                        "raw_length": len(stdin_data),
                        "hook_event_name": "ParseError",
                        "raw_preview": stdin_data[:200]
                    }
        else:
            return {"error": "No stdin data"}
            
    except Exception as e:
        return {
            "error": f"Hook data load failed: {e}",
            "hook_event_name": "LoadError"
        }

def should_monitor_event(hook_data, config):
    """Bu event'i monitor etmeli miyiz?"""
    event_type = hook_data.get("hook_event_name", "")
    events_config = config.get("events", {})
    return events_config.get(event_type, False)

def format_log_entry(hook_data, config):
    """Log entry'sini formatla"""
    output_config = config.get("output", {})
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    event_type = hook_data.get("hook_event_name", "Unknown")
    
    # Emoji headers
    if output_config.get("emoji_headers", True):
        header = "🚀" * 40
        entry = f"{header}\n"
    else:
        header = "=" * 40
        entry = f"{header}\n"
    
    # Timestamp
    if output_config.get("timestamps", True):
        entry += f"⏰ {timestamp} | 📋 EVENT: {event_type}\n"
    else:
        entry += f"EVENT: {event_type}\n"
    
    if output_config.get("emoji_headers", True):
        entry += f"{header}\n"
        entry += f"🎯 EVENT TYPE: {event_type}\n"
        entry += f"📝 CMD ARGS: {sys.argv[1:]}\n"
    else:
        entry += f"{header}\n"
        entry += f"EVENT TYPE: {event_type}\n"
        entry += f"CMD ARGS: {sys.argv[1:]}\n"
    
    # Session info
    if hook_data.get("session_id"):
        session_short = hook_data["session_id"][:8] + "..."
        entry += f"🔑 SESSION: {session_short}\n" if output_config.get("emoji_headers", True) else f"SESSION: {session_short}\n"
    
    if hook_data.get("transcript_path"):
        transcript_name = os.path.basename(hook_data["transcript_path"])
        entry += f"📁 TRANSCRIPT: {transcript_name}\n" if output_config.get("emoji_headers", True) else f"TRANSCRIPT: {transcript_name}\n"
    
    # Prompt preview
    if hook_data.get("prompt"):
        truncate_len = output_config.get("truncate_prompt", 100)
        prompt = hook_data["prompt"]
        if len(prompt) > truncate_len:
            prompt_preview = prompt[:truncate_len] + "..."
        else:
            prompt_preview = prompt
        entry += f"💬 PROMPT: {prompt_preview}\n" if output_config.get("emoji_headers", True) else f"PROMPT: {prompt_preview}\n"
    
    # CWD
    if hook_data.get("cwd"):
        entry += f"📂 CWD: {hook_data['cwd']}\n" if output_config.get("emoji_headers", True) else f"CWD: {hook_data['cwd']}\n"
    
    # Full JSON
    if output_config.get("show_full_json", True):
        json_indent = output_config.get("json_indent", 2)
        entry += f"📊 FULL JSON:\n" if output_config.get("emoji_headers", True) else f"FULL JSON:\n"
        entry += json.dumps(hook_data, indent=json_indent, ensure_ascii=False)
        entry += "\n\n"
    
    return entry

def write_log(log_entry, config):
    """Log entry'sini dosyaya yaz"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = config.get("log_file", "hook-monitor.log")
    log_path = os.path.join(script_dir, log_file)
    
    try:
        with open(log_path, 'a', encoding='utf-8', errors='replace') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"HookMonitor log error: {e}", file=sys.stderr)

def main():
    """Ana fonksiyon"""
    # İlk olarak debug dosyasına "alive" yazalım
    try:
        debug_file = os.path.join(os.path.dirname(__file__), "hook-monitor.log")
        with open(debug_file, 'a', encoding='utf-8', errors='replace') as f:
            f.write(f"ALIVE {datetime.datetime.now()} ARGS: {sys.argv}\n")
    except:
        pass
        
    config = load_plugin_config()
    
    # Plugin enabled mi?
    if not config.get("enabled", True):
        return
    
    # Hook data'yı al
    hook_data = load_hook_data(config)
    
    if "error" in hook_data:
        error_log = f"HookMonitor Error [{datetime.datetime.now()}]: {hook_data['error']}\n"
        write_log(error_log, config)
        return
    
    # Bu event'i monitor et mi?
    if not should_monitor_event(hook_data, config):
        return
    
    # Log entry'sini formatla ve yaz
    log_entry = format_log_entry(hook_data, config)
    write_log(log_entry, config)

if __name__ == "__main__":
    main()