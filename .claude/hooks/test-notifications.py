#!/usr/bin/env python3
"""
Claude Code Hook Notification System - Test Script
Tüm bildirim türlerini test eder
"""
import sys
import time
import json
import os
import subprocess

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'utils'))
try:
    from platform_utils import get_platform_info
except:
    pass

def print_header(text):
    """Başlık yazdır"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def test_notification(tool_name, event_type, description):
    """Tek bir bildirimi test et"""
    print(f"\n🧪 Test: {description}")
    print(f"   Tool: {tool_name}, Event: {event_type}")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    notify_script = os.path.join(script_dir, "config-manager", "notify-all.py")
    
    try:
        subprocess.run([sys.executable, notify_script, tool_name, event_type])
        print("   ✅ Başarılı")
        return True
    except Exception as e:
        print(f"   ❌ Hata: {e}")
        return False

def check_dependencies():
    """Python bağımlılıklarını kontrol et"""
    print_header("Bağımlılık Kontrolü")
    
    dependencies = {
        "pygame": "Ses bildirimleri için (Windows)",
        "plyer": "Desktop toast bildirimleri için",
        "telegram": "Telegram bildirimleri için",
        "windows_toasts": "Windows toast bildirimleri için (opsiyonel)"
    }
    
    missing = []
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module}: {description}")
        except ImportError:
            print(f"❌ {module}: {description} - YÜKLÜ DEĞİL")
            missing.append(module)
    
    return missing

def check_config():
    """Config dosyasını kontrol et"""
    print_header("Yapılandırma Kontrolü")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config-manager", "notification-config.json")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        notifications = config.get("notifications", {})
        enabled_count = 0
        
        print("\nAktif Plugin'ler:")
        for name, plugin_config in notifications.items():
            if name.startswith("_"):
                continue
            if plugin_config.get("enabled", False):
                enabled_count += 1
                events = [e for e, v in plugin_config.get("events", {}).items() if v]
                print(f"  ✅ {name}: {', '.join(events)}")
            else:
                print(f"  ❌ {name}: Devre dışı")
        
        if enabled_count == 0:
            print("\n⚠️  Hiçbir bildirim aktif değil!")
            
        # Quiet hours kontrolü
        quiet = config.get("quiet_hours", {})
        if quiet.get("enabled", False):
            print(f"\n🌙 Sessiz Saatler: {quiet['start']} - {quiet['end']}")
            print(f"   Kapalı: {', '.join(quiet.get('mute', []))}")
            print(f"   Açık: {', '.join(quiet.get('allow', []))}")
            
    except Exception as e:
        print(f"❌ Config dosyası okunamadı: {e}")

def main():
    """Ana test fonksiyonu"""
    print("🎯 Claude Code Hook Notification System - Test")
    print("=" * 50)
    
    # Platform bilgisi
    try:
        info = get_platform_info()
        print(f"Platform: {info['system'].title()}")
    except:
        print("Platform: Belirlenemedi")
    
    # Bağımlılık kontrolü
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Eksik bağımlılıklar: {', '.join(missing)}")
        print("Kurulum için: pip install -r requirements.txt")
    
    # Config kontrolü
    check_config()
    
    # Test bildirimleri
    print_header("Bildirim Testleri")
    
    response = input("\nBildirimleri test etmek ister misiniz? (e/h): ")
    if response.lower() != 'e':
        print("Test iptal edildi.")
        return
    
    tests = [
        ("Bash", "PreToolUse", "Bash komutu çalıştırılıyor bildirimi"),
        ("Edit", "PreToolUse", "Dosya düzenleniyor bildirimi"),
        ("Stop", "Stop", "İş tamamlandı bildirimi"),
        ("Notification", "Notification", "Dikkat gerekiyor bildirimi"),
        ("SubagentStop", "SubagentStop", "Alt görev tamamlandı bildirimi")
    ]
    
    print("\n⏳ Bildirimler 2 saniye arayla gönderilecek...")
    
    success_count = 0
    for tool, event, desc in tests:
        if test_notification(tool, event, desc):
            success_count += 1
        time.sleep(2)
    
    # Sonuç
    print_header("Test Sonucu")
    print(f"Başarılı: {success_count}/{len(tests)}")
    
    if success_count == len(tests):
        print("\n🎉 Tüm testler başarılı!")
    else:
        print("\n⚠️  Bazı testler başarısız oldu.")
        print("Sorun giderme için README'deki Troubleshooting bölümüne bakın.")

if __name__ == "__main__":
    main()