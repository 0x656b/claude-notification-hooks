#!/usr/bin/env python3
"""
Platform detection and utilities
"""
import platform
import os
import sys

def get_platform():
    """
    Returns: 'windows', 'macos', 'linux'
    """
    system = platform.system().lower()
    if system == 'darwin':
        return 'macos'
    return system

def get_platform_info():
    """
    Detailed platform information
    """
    return {
        'system': get_platform(),
        'version': platform.version(),
        'machine': platform.machine(),
        'python': sys.version,
        'is_windows': get_platform() == 'windows',
        'is_macos': get_platform() == 'macos',
        'is_linux': get_platform() == 'linux'
    }

def get_notification_command():
    """
    Platform-specific notification commands
    """
    system = get_platform()
    
    if system == 'windows':
        return None  # Windows uses Python libraries
    elif system == 'macos':
        return 'osascript -e \'display notification "{message}" with title "{title}"\''
    elif system == 'linux':
        return 'notify-send "{title}" "{message}"'
    
def get_sound_player():
    """
    Platform-specific sound player commands
    """
    system = get_platform()
    
    if system == 'windows':
        return None  # Windows uses pygame/winsound
    elif system == 'macos':
        return 'afplay "{file}"'
    elif system == 'linux':
        # Try multiple options
        if os.system('which paplay >/dev/null 2>&1') == 0:
            return 'paplay "{file}"'
        elif os.system('which aplay >/dev/null 2>&1') == 0:
            return 'aplay -q "{file}"'
        elif os.system('which mpg123 >/dev/null 2>&1') == 0:
            return 'mpg123 -q "{file}"'
        else:
            return 'play "{file}"'  # sox

def get_beep_command():
    """
    Platform-specific beep commands
    """
    system = get_platform()
    
    if system == 'windows':
        return None  # Uses winsound.Beep
    elif system == 'macos':
        return 'osascript -e "beep 1" 2>/dev/null || printf "\\a"'
    elif system == 'linux':
        return 'printf "\\a" || beep 2>/dev/null || play -n synth 0.3 sine 1000 2>/dev/null'

def normalize_path(path):
    """
    Normalize path for current platform
    """
    return os.path.normpath(path)

if __name__ == "__main__":
    # Test
    info = get_platform_info()
    print(f"Platform: {info['system']}")
    print(f"Version: {info['version']}")
    print(f"Sound player: {get_sound_player()}")
    print(f"Notification command: {get_notification_command()}")