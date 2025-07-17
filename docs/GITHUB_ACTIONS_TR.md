# GitHub Actions'da Claude Code Hook'ları Kullanımı

[🇬🇧 English](GITHUB_ACTIONS.md)

Bu rehber, Claude Code Hook Bildirim Sistemini GitHub Actions workflow'larınıza nasıl entegre edeceğinizi gösterir.

## 🚀 Hızlı Başlangıç

### Minimal Kurulum (Sadece Bildirimler)

CI/CD pipeline'ınızda sadece bildirim istiyorsanız:

1. **Sadece ihtiyacınız olanları** repo'nuza kopyalayın:
   ```
   .claude/hooks/telegram-bot/telegram-notifier.py
   .claude/hooks/config-manager/notify-all.py
   .claude/hooks/config-manager/notification-config.json
   ```

2. **GitHub reponuza secret'lar ekleyin**:
   - Settings → Secrets → Actions'a gidin
   - `TELEGRAM_BOT_TOKEN` ve `TELEGRAM_CHAT_ID` ekleyin

3. **Workflow'unuzda kullanın**:
   ```yaml
   - name: Build başlangıç bildirimi
     run: |
       python3 .claude/hooks/telegram-bot/telegram-notifier.py "Build" "Start"
   ```

## 📋 Tam Entegrasyon Örnekleri

### Örnek 1: Basit Build Bildirimleri

Build adımları sırasında Telegram bildirimleri gönderen basit bir entegrasyon için [`.github/workflows/simple-example.yml`](../.github/workflows/simple-example.yml) dosyasına bakın.

### Örnek 2: Tam Claude Code Entegrasyonu

Şunları yapan kapsamlı bir örnek için [`.github/workflows/claude-code-example.yml`](../.github/workflows/claude-code-example.yml) dosyasına bakın:
- PR yorumlarındaki `/claude` komutlarına yanıt verir
- Claude Code'u belirli görevlerle çalıştırır
- Sonuçları GitHub yorumlarına geri gönderir
- Telegram/Discord bildirimleri gönderir
- Log'ları artifact olarak yükler

## 🔧 Yapılandırma Seçenekleri

### Ortam Değişkenleri

Bildirim sistemi CI'da şu ortam değişkenlerini okur:

```yaml
env:
  # Telegram için
  TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
  TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
  
  # GitHub yorum bildirimleri için
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  GITHUB_REPOSITORY: ${{ github.repository }}
  ISSUE_NUMBER: ${{ github.event.issue.number }}
```

### CI'ya Özel Yapılandırma

Sesi devre dışı bırakıp sadece ilgili bildirimleri etkinleştirmek için CI'ya özel bir config oluşturun:

```python
config = {
    'notifications': {
        'sound': {
            'enabled': False,  # CI'da ses yok
        },
        'telegram': {
            'enabled': True,
            'events': {
                'Stop': True,
                'Notification': True
            }
        },
        'github_comment': {
            'enabled': True,
            'script': 'github-actions/comment-notifier.py',
            'events': {
                'Stop': True
            }
        }
    },
    'quiet_hours': {'enabled': False},
    'logging': {'enabled': True},
    'culture': {'language': 'tr'}  # Türkçe bildirimler
}
```

## 🎯 Kullanım Senaryoları

### 1. Uzun Süren Görevler
Zaman alan işlemler tamamlandığında bildirim gönderin:

```yaml
- name: Entegrasyon testlerini çalıştır
  run: |
    python3 notify.py "EntegrasyonTestleri" "Start"
    npm run test:integration  # Bu 20 dakika sürüyor
    python3 notify.py "EntegrasyonTestleri" "Stop"
```

### 2. Deployment Bildirimleri
Deployment'lar gerçekleştiğinde takıma haber verin:

```yaml
- name: Production'a deploy et
  if: github.ref == 'refs/heads/main'
  run: |
    python3 notify.py "Deploy" "Notification"
    ./deploy.sh
    python3 notify.py "Deploy" "Stop"
```

### 3. Hata Bildirimleri
Hatalar oluştuğunda uyarı gönderin:

```yaml
- name: Build
  id: build
  run: npm run build
  
- name: Hata bildirimi
  if: failure()
  run: |
    python3 notify.py "Build" "Error"
```

### 4. Claude Code Otomasyonu
PR yorumlarından Claude Code'u tetikleyin:

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  claude-gorevi:
    if: contains(github.event.comment.body, '/claude')
    runs-on: ubuntu-latest
    steps:
      # ... kurulum ...
      - name: Claude'u çalıştır
        run: |
          TASK="${{ github.event.comment.body }}"
          TASK=${TASK#/claude }  # Prefix'i kaldır
          claude-code --task "$TASK" --hooks-enabled
```

## 🛠️ Özel GitHub Actions Bildirici

PR yorumlarına gönderen özel bir bildirici oluşturun:

```python
# .claude/hooks/github-actions/comment-notifier.py
import os
import json
import urllib.request

def yorum_gonder(mesaj):
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    pr_numarasi = os.environ.get('PR_NUMBER')
    
    url = f"https://api.github.com/repos/{repo}/issues/{pr_numarasi}/comments"
    
    veri = json.dumps({'body': mesaj}).encode()
    istek = urllib.request.Request(url, data=veri, headers={
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    })
    
    urllib.request.urlopen(istek)
```

## 🔒 Güvenlik En İyi Uygulamaları

1. **Kimlik bilgilerini asla commit etmeyin** - Her zaman GitHub Secrets kullanın
2. **Token izinlerini sınırlayın** - Minimum kapsam kullanın
3. **Girdileri doğrulayın** - PR yorumlarını işlemeden önce temizleyin
4. **Ortam kısıtlamaları kullanın** - Secret'ları belirli ortamlarla sınırlandırın

## 📊 Durum Rozeti

README'nize durum rozeti ekleyin:

```markdown
![Claude Code Bildirimleri](https://github.com/KULLANICI_ADINIZ/REPO_ADINIZ/actions/workflows/claude-code-example.yml/badge.svg)
```

## 🤖 Bot Komutları

PR yorum komutları uyguluyorsanız:

- `/claude review` - Kod incelemesi
- `/claude test` - Eksik testleri ekle
- `/claude docs` - Dokümantasyonu güncelle
- `/claude fix-lint` - Linting hatalarını düzelt

## 💡 İpuçları

1. **Paralel bildirimler**: Bildirimleri engellemeden göndermek için `&` kullanın:
   ```bash
   python3 notify.py "Build" "Start" &
   ```

2. **Koşullu bildirimler**: Sadece main branch'te bildirim gönderin:
   ```yaml
   if: github.ref == 'refs/heads/main'
   ```

3. **Matrix bildirimleri**: İşletim sistemi başına farklı bildirimler:
   ```yaml
   strategy:
     matrix:
       os: [ubuntu-latest, windows-latest]
   ```

4. **Zamanlanmış bildirimler**: Düzenli görevler için:
   ```yaml
   on:
     schedule:
       - cron: '0 9 * * 1'  # Her Pazartesi
   ```

## 🔍 Hata Ayıklama

Debug log'ları etkinleştirin:

```yaml
- name: Debug ile çalıştır
  env:
    ACTIONS_STEP_DEBUG: true
  run: |
    python3 -u notify.py "Debug" "Test"
```

Webhook teslimatlarını kontrol edin:
- GitHub: Settings → Webhooks → Son Teslimatlar
- Telegram: `/getUpdates` API endpoint'ini kullanın
- Discord: Sunucu ayarlarında webhook log'larını kontrol edin

## 📚 Ek Kaynaklar

- [GitHub Actions Dokümantasyonu](https://docs.github.com/tr/actions)
- [Claude Code Dokümantasyonu](https://docs.anthropic.com/en/docs/claude-code)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Discord Webhook'ları](https://discord.com/developers/docs/resources/webhook)