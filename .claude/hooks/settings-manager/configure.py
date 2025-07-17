#!/usr/bin/env python3
"""
Claude Code Notification Configuration Tool
Allows easy command-line configuration of notification settings
"""
import json
import sys
import os

# Default config file path (relative to script)
DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "..", 
    "config-manager", 
    "notification-config.json"
)

# Check if config path was passed as environment variable (from batch/shell script)
CONFIG_FILE = os.environ.get('CLAUDE_NOTIFICATION_CONFIG', DEFAULT_CONFIG_FILE)

# Debug: Print which config file is being used (can be removed later)
if '--debug' in sys.argv:
    print(f"Using config file: {CONFIG_FILE}")
    print(f"Environment variable: {os.environ.get('CLAUDE_NOTIFICATION_CONFIG', 'Not set')}")

def load_config():
    """Load the current configuration"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at: {CONFIG_FILE}")
        print(f"Current working directory: {os.getcwd()}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading configuration: {e}")
        print(f"Config file path: {CONFIG_FILE}")
        sys.exit(1)

def save_config(config):
    """Save the configuration"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def show_status(config):
    """Display current configuration status"""
    print("Current Configuration:")
    print("-" * 40)
    
    # Sound status
    sound_enabled = config.get('notifications', {}).get('sound', {}).get('enabled', False)
    print(f"Sound:          {'ENABLED' if sound_enabled else 'DISABLED'}")
    
    # Telegram status
    telegram_enabled = config.get('notifications', {}).get('telegram', {}).get('enabled', False)
    print(f"Telegram:       {'ENABLED' if telegram_enabled else 'DISABLED'}")
    
    # Toast status
    toast_enabled = config.get('notifications', {}).get('desktop_toast', {}).get('enabled', False)
    print(f"Desktop Toast:  {'ENABLED' if toast_enabled else 'DISABLED'}")
    
    # Language
    lang = config.get('culture', {}).get('language', 'en')
    lang_name = 'English' if lang == 'en' else 'Turkish' if lang == 'tr' else lang
    print(f"Language:       {lang_name} ({lang})")
    
    # Quiet hours
    quiet_enabled = config.get('quiet_hours', {}).get('enabled', False)
    if quiet_enabled:
        start = config.get('quiet_hours', {}).get('start', 'N/A')
        end = config.get('quiet_hours', {}).get('end', 'N/A')
        print(f"Quiet Hours:    ENABLED ({start} - {end})")
    else:
        print(f"Quiet Hours:    DISABLED")
    
    print("-" * 40)

def process_argument(arg, config):
    """Process a single configuration argument"""
    if ':' not in arg:
        print(f"Invalid argument: {arg}")
        return False
        
    key, value = arg.split(':', 1)
    
    if key == 'sound':
        if value in ['0', '1']:
            config.setdefault('notifications', {}).setdefault('sound', {})['enabled'] = (value == '1')
            print(f"Sound notifications {'enabled' if value == '1' else 'disabled'}")
            return True
            
    elif key == 'telegram':
        if value in ['0', '1']:
            config.setdefault('notifications', {}).setdefault('telegram', {})['enabled'] = (value == '1')
            print(f"Telegram notifications {'enabled' if value == '1' else 'disabled'}")
            return True
            
    elif key == 'toast':
        if value in ['0', '1']:
            config.setdefault('notifications', {}).setdefault('desktop_toast', {})['enabled'] = (value == '1')
            print(f"Desktop toast notifications {'enabled' if value == '1' else 'disabled'}")
            return True
            
    elif key == 'lang':
        if value in ['en', 'tr']:
            config.setdefault('culture', {})['language'] = value
            lang_name = 'English' if value == 'en' else 'Turkish'
            print(f"Language set to {lang_name}")
            return True
        else:
            print(f"Invalid language: {value}. Use 'en' or 'tr'")
            
    elif key == 'quiet':
        if value in ['0', '1']:
            config.setdefault('quiet_hours', {})['enabled'] = (value == '1')
            print(f"Quiet hours {'enabled' if value == '1' else 'disabled'}")
            return True
        elif '-' in value:
            # Time range format: HH:MM-HH:MM
            try:
                start, end = value.split('-')
                # Basic validation
                start_parts = start.split(':')
                end_parts = end.split(':')
                if len(start_parts) == 2 and len(end_parts) == 2:
                    # Validate hours and minutes
                    start_h, start_m = int(start_parts[0]), int(start_parts[1])
                    end_h, end_m = int(end_parts[0]), int(end_parts[1])
                    
                    if 0 <= start_h <= 23 and 0 <= start_m <= 59 and 0 <= end_h <= 23 and 0 <= end_m <= 59:
                        config.setdefault('quiet_hours', {})['start'] = start
                        config.setdefault('quiet_hours', {})['end'] = end
                        config['quiet_hours']['enabled'] = True
                        print(f"Quiet hours set to {start} - {end}")
                        return True
                    else:
                        print(f"Invalid time values: {value}")
            except:
                print(f"Invalid time format: {value}. Use HH:MM-HH:MM")
    else:
        print(f"Unknown option: {key}")
    
    return False

def show_help():
    """Display help message"""
    print("Claude Code Notification Configurator")
    print()
    print("Usage: python configure.py [options]")
    print()
    print("Options:")
    print("  sound:0/1         - Disable/Enable sound notifications")
    print("  telegram:0/1      - Disable/Enable Telegram notifications")
    print("  toast:0/1         - Disable/Enable desktop toast notifications")
    print("  lang:en/tr        - Set language (English/Turkish)")
    print("  quiet:0/1         - Disable/Enable quiet hours")
    print("  quiet:HH:MM-HH:MM - Set quiet hours time range")
    print("  status            - Show current configuration")
    print()
    print("Examples:")
    print("  python configure.py sound:0 telegram:1")
    print("  python configure.py lang:tr quiet:23:00-07:00")
    print("  python configure.py status")

def main():
    """Main function"""
    args = sys.argv[1:]
    
    # Show help if no arguments
    if not args:
        show_help()
        return
    
    # Load current config
    config = load_config()
    
    # Check if only showing status
    if 'status' in args:
        show_status(config)
        return
    
    # Process all arguments
    changes_made = False
    for arg in args:
        if arg == 'status':
            continue  # Already handled above
        if process_argument(arg, config):
            changes_made = True
    
    # Save config if changes were made
    if changes_made:
        save_config(config)
        print("\nConfiguration saved successfully!")

if __name__ == "__main__":
    main()