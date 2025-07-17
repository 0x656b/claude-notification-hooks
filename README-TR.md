# Claude Code Hook Bildirim Sistemi

Claude Code'un hook özelliğini kullanarak geliştirme sırasında sesli, Telegram ve masaüstü bildirimleri sağlayan kapsamlı bir bildirim sistemi.

[🇬🇧 English README](README.md)

## 📋 İçindekiler

- [Claude Code ve Hook'lar Nedir?](#-claude-code-ve-hooklar-nedir)
- [Proje Yapısı](#-proje-yapısı)
- [Hızlı Başlangıç](#-hızlı-başlangıç)
- [Kurulumu Test Etme](#-kurulumu-test-etme)
- [Kurulum](#-kurulum)
- [Bildirim Türleri](#-bildirim-türleri)
- [Yapılandırma](#️-yapılandırma)
- [Platform Desteği](#-platform-desteği)
- [Telegram Kurulumu](#-telegram-kurulumu)
- [Sorun Giderme](#-sorun-giderme)
- [İleri Düzey Konular](#-i̇leri-düzey-konular)

## 🤖 Claude Code ve Hook'lar Nedir?

### Claude Code
Claude Code, Anthropic'in Claude AI'nın yeteneklerini doğrudan terminalinize getiren resmi CLI aracıdır. Şunlarda yardımcı olur:
- Kod yazma ve düzenleme
- Komut çalıştırma
- Dosya okuma ve analiz etme
- Programlama sorularını yanıtlama
- Ve çok daha fazlası!

### Hook'lar Nedir?
Hook'lar, Claude Code'un çalışması sırasında belirli olaylarda çalıştırdığı komutlardır. Claude bir şey yaptığında tetiklenen "tetikleyiciler" olarak düşünün.

**Örnek Olaylar:**
- `PreToolUse` - Claude bir aracı kullanmadan önce (komut çalıştırmak gibi)
- `PostToolUse` - Claude bir aracı kullandıktan sonra
- `Stop` - Claude bir görevi bitirdiğinde
- `Notification` - Claude dikkatinize ihtiyaç duyduğunda
- `SubagentStop` - Bir alt görev tamamlandığında

**Örnek Hook:**
```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/notify.py"
        }
      ]
    }
  ]
}
```

Bu hook, Claude durduğunda `notify.py`'yi çalıştırır ve "iş tamamlandı" sesi çalar!

## 📁 Proje Yapısı

```
claude-notification-hooks/
├── .claude/                    # Claude Code yapılandırma klasörü
│   ├── settings.json          # Hook tanımlamaları
│   └── hooks/                 # Hook scriptleri ve yapılandırmalar
│       ├── config-manager/    # Merkezi yapılandırma
│       │   ├── notify-all.py  # Ana bildirim dağıtıcı
│       │   ├── notification-config.json  # Kullanıcı ayarları
│       │   └── activity-logger.py
│       ├── settings-manager/  # Yapılandırma araçları
│       │   ├── configure.py   # Ana yapılandırma scripti
│       │   ├── configure-notifications.bat
│       │   └── configure-notifications.sh
│       ├── voice-notifier/    # Sesli bildirim sistemi
│       │   ├── smart-notification.py
│       │   ├── sound-mapping.json
│       │   └── voice/        # MP3 ses dosyaları
│       │       ├── bash.mp3
│       │       ├── editing.mp3
│       │       ├── ready.mp3
│       │       └── ...
│       ├── telegram-bot/      # Telegram entegrasyonu
│       │   ├── telegram-notifier.py
│       │   ├── telegram-config.json  # Bot bilgileri (gitignore'da)
│       │   └── telegram-config.json.template
│       ├── toast-notifier/    # Cross-platform masaüstü bildirimleri
│       │   └── cross-platform-notifier.py
│       └── utils/             # Yardımcı fonksiyonlar
│           └── platform_utils.py
├── configure-notifications.bat # Windows yapılandırma wrapper
├── configure-notifications.sh  # Linux/Mac yapılandırma wrapper
├── debug-hooks.bat            # Sorun giderme için debug aracı
├── README.md                  # İngilizce dokümantasyon
├── README-TR.md              # Bu dosya
├── CLAUDE.md                 # Claude için talimatlar
└── .gitignore               # Git ignore dosyası
```

## 🚀 Hızlı Başlangıç

1. **`.claude` klasörünü** proje ana dizininize kopyalayın
2. **Python bağımlılıklarını kurun:**
   ```bash
   pip install pygame plyer windows-toasts python-telegram-bot
   ```
3. **Claude Code'da hook'ları etkinleştirin:**
   ```bash
   /hooks
   ```
4. **Test edin:** Claude'un bir şey yapmasını sağlayın ve bildirimi duyun!

## 🧪 Kurulumu Test Etme

Kurulumdan sonra, tüm bildirim türlerini test edin:

```bash
python3 .claude/hooks/test-notifications.py
```

Bu test:
- Her bildirim türünü test eder (ses, masaüstü, Telegram)
- Hangi bağımlılıkların kurulu olduğunu gösterir
- Yapılandırma durumunu görüntüler
- Sorunları teşhis etmeye yardımcı olur

## 📦 Kurulum

### Gereksinimler
- Python 3.7+
- Claude Code CLI kurulu
- pip (Python paket yöneticisi)

### Platform Uyumluluğu
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Ubuntu/Debian Linux
- ✅ Python 3.7+ olan çoğu Linux dağıtımı

### Adım 1: Klonlayın veya İndirin
```bash
git clone https://github.com/kullaniciadi/claude-notification-hooks
# VEYA sadece .claude klasörünü projenize kopyalayın
```

### Adım 2: Bağımlılıkları Kurun

Otomatik kurulum için kullanışlı kurulum scriptleri sağlıyoruz:

**Windows (Yönetici olarak çalıştırın):**
```bash
install-windows.bat
```

**macOS/Linux:**
```bash
chmod +x install-mac-linux.sh
./install-mac-linux.sh
```

**Veya manuel olarak kurun:**

**Windows:**
```bash
pip install -r requirements.txt
# Veya manuel:
pip install pygame plyer windows-toasts python-telegram-bot
```

**macOS:**
```bash
pip install -r requirements.txt
# Ses için yerleşik afplay, bildirimler için osascript kullanılır
```

**Linux:**
```bash
pip install -r requirements.txt
# Opsiyonel: sudo apt-get install sox mpg123
```

Kurulum scriptleri şunları yapacak:
- Python kurulumunu kontrol eder
- pip'i en son sürüme günceller
- requirements.txt'ten tüm gerekli bağımlılıkları kurar
- Platforma özel öneriler sunar
- Python scriptlerini çalıştırılabilir yapar (Linux/macOS)

### Adım 3: Yapılandırın (Opsiyonel)

**Hızlı Yapılandırma (Yeni!):**
Komut satırından tek komutla ayarları değiştirin:

```bash
# Windows
configure-notifications.bat sound:0 telegram:1

# Linux/Mac
./configure-notifications.sh lang:tr quiet:23:00-07:00
```

**Manuel Yapılandırma:**
`.claude/hooks/config-manager/notification-config.json` dosyasını düzenleyin:
```json
{
  "notifications": {
    "sound": {
      "enabled": true,
      "events": {
        "Stop": true,
        "Notification": true,
        "PreToolUse": true
      }
    },
    "telegram": {
      "enabled": false,  # Kurulumdan sonra etkinleştirin
      "events": {
        "Stop": true,
        "Notification": true
      }
    }
  }
}
```

### Adım 4: Hook'ları Etkinleştirin
Claude Code'da:
```bash
/hooks
```
Bu, hook arayüzünü açar. Hook'lar zaten `settings.json`'da tanımlıdır.

**Windows için Önemli:** Hook'lar hemen çalışmıyorsa:
1. Geçici bir hook ekleyin (örn: `echo test`)
2. Hemen silin
3. Bu, önbelleği yeniler ve tüm hook'ları etkinleştirir

## 🔔 Bildirim Türleri

### 1. 🔊 Sesli Bildirimler
- Farklı araçlar için özel MP3 sesleri
- MP3'ler eksikse yedek bip sesleri
- Config'de ses kontrolü

**Sesler:**
- `bash.mp3` - Shell komutları
- `editing.mp3` - Dosya düzenlemeleri
- `ready.mp3` - Görev tamamlandı
- `commit.mp3` - Git işlemleri
- Ve daha fazlası!

### 2. 📱 Telegram Bildirimleri
- Telefonunuzda bildirim alın
- Uzun süren görevler için mükemmel
- Emoji'li zengin biçimlendirilmiş mesajlar

### 3. 💻 Masaüstü Toast Bildirimleri
- Yerel işletim sistemi bildirimleri
- Windows/macOS/Linux desteği
- Rahatsız etmeyen açılır pencereler

### 4. 🔌 Özel Plugin Bildirimleri
- Tamamen genişletilebilir plugin mimarisi
- İstediğiniz bildirim yöntemini ekleyin (Discord, Slack, Email vb.)
- Basit JSON yapılandırması
- Detaylar için [Plugin Sistemi](#plugin-sistemi) bölümüne bakın

## ⚙️ Yapılandırma

### Komut Satırı Yapılandırması (Yeni!)

JSON dosyasını elle düzenlemek yerine, komut satırından kolayca yapılandırma yapabilirsiniz:

```bash
# Windows
configure-notifications.bat [seçenekler]

# Linux/Mac
./configure-notifications.sh [seçenekler]
```

**Seçenekler:**
- `sound:0/1` - Ses bildirimlerini kapat/aç
- `telegram:0/1` - Telegram bildirimlerini kapat/aç
- `toast:0/1` - Masaüstü bildirimlerini kapat/aç
- `lang:en/tr` - Dil ayarı (İngilizce/Türkçe)
- `quiet:0/1` - Sessiz saatleri kapat/aç
- `quiet:HH:MM-HH:MM` - Sessiz saat aralığını ayarla
- `status` - Mevcut yapılandırmayı göster

**Örnekler:**
```bash
# Sesi kapat, Telegram'ı aç
configure-notifications.bat sound:0 telegram:1

# Türkçe yap ve sessiz saatleri ayarla
configure-notifications.bat lang:tr quiet:23:00-07:00

# Mevcut ayarları göster
configure-notifications.bat status
```

### Ana Yapılandırma Dosyası
`.claude/hooks/config-manager/notification-config.json`

```json
{
  "notifications": {
    "sound": {
      "enabled": true,
      "script": "voice-notifier/smart-notification.py",
      "volume": 100,
      "events": {
        "Stop": true,
        "Notification": true,
        "PreToolUse": true,
        "PostToolUse": false
      }
    },
    "telegram": {
      "enabled": true,
      "script": "telegram-bot/telegram-notifier.py",
      "events": {
        "Stop": true,
        "Notification": true,
        "SubagentStop": true
      }
    },
    "desktop_toast": {
      "enabled": true,
      "script": "toast-notifier/cross-platform-notifier.py",
      "events": {
        "Stop": true,
        "Notification": true,
        "SubagentStop": true
      }
    }
  },
  "quiet_hours": {
    "enabled": false,
    "start": "23:00",
    "end": "07:00",
    "mute": ["sound"],
    "allow": ["telegram", "desktop_toast"]
  },
  "logging": {
    "enabled": false,
    "max_size_mb": 10
  }
}
```

**Temel Özellikler:**
- **Plugin tabanlı**: Her bildirim türü kendi script'i olan bir plugin
- **Esnek olaylar**: Her plugin'i hangi olayların tetikleyeceğini kontrol edin
- **Tool bazlı kontrol**: Hangi tool'ların bildirim tetikleyeceğini ayarlayın
- **Çoklu dil desteği**: İngilizce ve Türkçe bildirimler (ayarlanabilir)
- **Sessiz saatler**: Gece hangi plugin'lerin çalışacağına ince ayar
- **Genişletilebilir**: Kolayca özel bildirim plugin'i ekleyin

### Tool Bazlı Kontrol

Hangi tool'ların bildirim tetikleyeceğini herhangi bir plugin için ayarlayabilirsiniz. Bu özellik sadece ses için değil, tüm plugin'ler için kullanılabilir:

```json
"sound": {
  "enabled": true,
  "events": {
    "PreToolUse": true  // Genel ayar
  },
  "tools": {
    "enabled": true,    // Tool-bazlı kontrolü etkinleştir
    "custom": {
      "Bash": {"PreToolUse": true, "PostToolUse": false},
      "Edit": {"PreToolUse": true, "PostToolUse": false},
      "Read": {"PreToolUse": true, "PostToolUse": false},
      "Grep": {"PreToolUse": false, "PostToolUse": false},  // Sessiz
      "LS": {"PreToolUse": false, "PostToolUse": false},    // Sessiz
      "Glob": {"PreToolUse": false, "PostToolUse": false}   // Sessiz
    }
  }
}
```

**Seçenekler:**
- `whitelist`: Sadece bu tool'lar ses çıkarır
- `blacklist`: Bu tool'lar asla ses çıkarmaz
- `custom`: Tool başına olay ayarları (genel ayarları geçersiz kılar)

### Dil Ayarları

Telegram ve masaüstü bildirimleri için tercih ettiğiniz dili ayarlayın:

```json
"culture": {
  "language": "tr"  // Seçenekler: "tr" (Türkçe) veya "en" (English)
}
```

### Ses Eşleştirme
`.claude/hooks/voice-notifier/sound-mapping.json`

**MP3 dosyaları hakkında not**: Proje, lisans nedeniyle depoya dahil edilmeyen MP3 ses dosyaları kullanır. Şunları yapabilirsiniz:
1. Yedek bip seslerini kullanın (otomatik)
2. Kendi MP3 dosyalarınızı `.claude/hooks/voice-notifier/voice/` klasörüne ekleyin
3. freesound.org gibi sitelerden telif hakkı olmayan bildirim sesleri kullanın

Hangi aracın hangi sesi tetikleyeceğini özelleştirin:
```json
{
  "tool_sounds": {
    "Bash": "bash.mp3",
    "Edit": "editing.mp3",
    "Read": "listing.mp3"
  },
  "event_sounds": {
    "Stop": "ready.mp3",
    "Notification": "ready.mp3"
  }
}
```

## 🌍 Platform Desteği

Bu proje işletim sisteminizi otomatik olarak algılar ve buna göre davranır!

### Windows
- **Ses**: MP3 için pygame, bip için winsound
- **Toast**: plyer ile Windows 10/11 bildirimleri
- **Yol formatı**: Hem `C:\yol` hem `/c/yol` çalışır

### macOS
- **Ses**: afplay (yerleşik)
- **Toast**: osascript bildirimleri
- **Ek kurulum gerekmez!**

### Linux
- **Ses**: paplay/aplay/mpg123 (otomatik algılanır)
- **Toast**: notify-send
- **Opsiyonel**: `sudo apt-get install sox mpg123`

## 📱 Telegram Kurulumu

### Adım 1: Bot Oluşturun

1. Telegram'ı açın ve [@BotFather](https://t.me/botfather) araması yapın
2. `/newbot` gönderin
3. Bir isim seçin (örn: "Claude Bildirimcim")
4. Bir kullanıcı adı seçin (örn: `benim_claude_botum`)
5. Aldığınız token'ı kopyalayın

### Adım 2: Chat ID'nizi Bulun

1. Bot'unuza herhangi bir mesaj gönderin
2. Tarayıcınızda bu URL'yi açın:
   ```
   https://api.telegram.org/bot<BOT_TOKENINIZ>/getUpdates
   ```
3. Yanıtta chat ID'nizi bulun:
   ```json
   "chat": {"id": 123456789}
   ```

### Adım 3: Yapılandırın

**ÖNEMLİ**: Gerçek kimlik bilgilerinizi asla version control'e commit etmeyin!

Template'i kopyalayın ve kimlik bilgilerinizi ekleyin:
```bash
cp .claude/hooks/telegram-bot/telegram-config.json.template .claude/hooks/telegram-bot/telegram-config.json
```

Sonra `.claude/hooks/telegram-bot/telegram-config.json` dosyasını düzenleyin:
```json
{
  "bot_token": "BOT_TOKENINIZ_BURAYA",
  "chat_id": "CHAT_IDINIZ_BURAYA"
}
```

Veya ortam değişkenleri kullanın:
```bash
export TELEGRAM_BOT_TOKEN="tokeniniz"
export TELEGRAM_CHAT_ID="chat-idiniz"
```

### Adım 4: Config'de Etkinleştirin
`notification-config.json`'da `telegram.enabled`'ı `true` yapın

## 🔧 Sorun Giderme

### Hızlı Tanı
Kurulumunuzu test etmek için:
```bash
python3 .claude/hooks/test-notifications.py
```

### Debug Modu
Sorunları gidermek için debug çıktısını etkinleştirin:

**Windows:**
```batch
set CLAUDE_DEBUG=true
debug-hooks.bat
```

**Linux/Mac:**
```bash
export CLAUDE_DEBUG=true
python3 .claude/hooks/config-manager/notify-all.py Test PreToolUse
```

### Yaygın Sorunlar

#### 1. Hook'lar Hiç Çalışmıyor
**Çözümler:**
- Claude Code'da `/hooks` komutunu çalıştırın
- **Windows Önbellek Sorunu:** Geçici hook ekleyip silin (örn: `echo test`)
- Python 3 PATH'te mi kontrol edin: `python3 --version`

#### 2. Eksik Bağımlılıklar
**Hata:** `ModuleNotFoundError: No module named 'plyer'`

**Çözüm:**
```bash
pip install -r requirements.txt
# Veya otomatik kurulum scriptlerini kullanın (Kurulum bölümüne bakın)
```

#### 3. Ses Gelmiyor
**Windows:** pygame kurun, MP3 dosyalarını kontrol edin
**Linux:** `sudo apt-get install sox mpg123`
**macOS:** Otomatik çalışmalı (afplay)

#### 4. Telegram Sorunları
- Token'ı test edin: `https://api.telegram.org/bot<TOKEN>/getMe`
- Bot'a `/start` mesajı attığınızdan emin olun
- Chat ID'yi kontrol edin

#### 5. Masaüstü Bildirim Sorunları
**Windows:** "Python 3.13" başlığı normaldir
**Linux:** `sudo apt-get install libnotify-bin`
**macOS:** Sistem Tercihleri > Bildirimler'i kontrol edin

#### 6. Özel Plugin Yüklenmiyor
- Script yolunu kontrol edin
- Python sözdizimi hatalarını kontrol edin
- Debug için script başına ekleyin:
```python
print(f"Debug: {sys.argv}", file=sys.stderr)
```

### Hala Sorun mu Var?
Test scriptini çalıştırın ve çıktıyı kontrol edin!

## 🎓 İleri Düzey Konular

### GitHub Actions Entegrasyonu

Bu bildirim sistemini CI/CD pipeline'larınızda kullanabilirsiniz! GitHub Actions Rehberimize ([Türkçe](docs/GITHUB_ACTIONS_TR.md) | [English](docs/GITHUB_ACTIONS.md)) göz atın:

- 🚀 Build bildirimleri için hızlı kurulum
- 🤖 Tam Claude Code otomasyon örnekleri
- 💬 PR yorum komutları (`/claude review`)
- 📊 GitHub'a durum raporlama
- 🔔 Çoklu platform bildirim stratejileri

Örnek workflow'lar `.github/workflows/` klasöründe:
- [`simple-example.yml`](.github/workflows/simple-example.yml) - Basit build bildirimleri
- [`claude-code-example.yml`](.github/workflows/claude-code-example.yml) - Tam Claude Code entegrasyonu

### Claude Code Sandbox Ortamı

Claude Code, bazı tuhaflıkları olan sandbox ortamında çalışır:

1. **Yol Formatları:**
   - Hook tanımları Unix yolları kullanır: `/d/proje/script.py`
   - Python scriptleri Windows yolları kullanabilir: `D:\proje\script.py`
   - Çoğu durumda her iki format da çalışır

2. **Ortam Değişkenleri:**
   - Sandbox sistem ortam değişkenlerine erişemeyebilir
   - Ortam değişkenlerine güvenmek yerine config dosyaları kullanın

3. **Python Çalıştırma:**
   - Windows'ta bile `python3` komutu kullanır
   - Sistemin Python kurulumunu çalıştırır

### Özel Hook'lar

`settings.json`'a kendi hook'larınızı ekleyin:
```json
{
  "BenimÖzelOlayım": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 .claude/hooks/benim-scriptim.py"
        }
      ]
    }
  ]
}
```

### Hook Parametreleri

Hook'lar olay hakkında parametreler alır:
- `%TOOL_NAME%` - Kullanılan aracın adı
- `%EVENT_TYPE%` - Tetiklenen olay türü

Örnek:
```bash
python3 notify.py %TOOL_NAME% %EVENT_TYPE%
```

### Plugin Sistemi

Bildirim sistemi tamamen plugin tabanlıdır! Her bildirim türü `notification-config.json`'da tanımlanan bir plugin'dir.

#### Yerleşik Plugin'ler

```json
{
  "sound": {
    "enabled": true,
    "script": "voice-notifier/smart-notification.py",
    "events": {
      "Stop": true,
      "Notification": true,
      "PreToolUse": true
    }
  }
}
```

#### Özel Plugin Oluşturma

1. **İki parametre alan bildirim script'inizi yazın**:
   ```python
   # benim-bildirimcim.py
   import sys
   tool_name = sys.argv[1]  # örn: "Bash"
   event_type = sys.argv[2]  # örn: "Stop"
   # Bildirim mantığınız buraya
   ```

2. **notification-config.json'a ekleyin**:
   ```json
   "benim_ozel_bildirimcim": {
     "enabled": true,
     "script": "custom/benim-bildirimcim.py",
     "events": {
       "Stop": true,
       "Notification": true
     },
     "tools": {
       "enabled": true,
       "blacklist": ["LS", "Grep"]  // Opsiyonel tool-bazlı kontrol
     },
     "params": ["--ekstra", "parametreler"]
   }
   ```

3. **Hepsi bu!** Plugin otomatik olarak yüklenip çalışacaktır.

#### Plugin Örnekleri

**Discord Webhook:**
```json
"discord": {
  "enabled": true,
  "script": "discord-bot/discord-notifier.py",
  "events": {
    "Stop": true,
    "Notification": true
  },
  "params": ["--webhook-url", "WEBHOOK_URLINIZ"]
}
```

**Slack (Absolute Path):**
```json
"slack": {
  "enabled": true,
  "script": "/home/kullanici/scriptler/slack-notifier.py",
  "events": {
    "Stop": true
  }
}
```

**Email Bildirimleri:**
```json
"email": {
  "enabled": true,
  "script": "email-plugin/email-gonder.py",
  "events": {
    "Stop": true,
    "Notification": true
  },
  "params": ["--kime", "sizin@email.com", "--smtp", "smtp.gmail.com"]
}
```

#### Plugin'ler için Sessiz Saatler

Sessiz saatlerde hangi plugin'lerin çalışacağını kontrol edin:

```json
"quiet_hours": {
  "enabled": true,
  "start": "23:00",
  "end": "07:00",
  "mute": ["sound", "discord"],  // Bunlar çalışmayacak
  "allow": ["telegram", "email"]  // Bunlar her zaman çalışacak
}
```

## 🔒 Güvenlik En İyi Uygulamaları

- **Kimlik bilgilerini commit etmeyin**: Token içeren config dosyaları için `.gitignore` kullanın
- **Ortam değişkenleri kullanın**: CI/CD için sabit değerler yerine secrets kullanın
- **Token'ları düzenli yenileyin**: Bir token açığa çıkarsa hemen yenileyin
- **Minimum izinler**: Bot'lara sadece ihtiyaç duydukları izinleri verin

## 🤝 Katkıda Bulunma

Sorun bildirimleri ve pull request'ler memnuniyetle karşılanır!

## 📝 Lisans

Bu proje açık kaynaklıdır ve MIT Lisansı altında kullanılabilir.

---

**Not**: Bu bir bildirim sistemidir, izleme sistemi değildir. Claude'un aktivitelerini kapsamlı bir şekilde takip etmek için değil, farkında olmanıza yardımcı olmak için tasarlanmıştır.

**Önemli**: Bu projeyi paylaşmadan önce `telegram-config.json`'dan kişisel bilgilerinizi kaldırdığınızdan emin olun!