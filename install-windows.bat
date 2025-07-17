@echo off
echo ======================================================
echo  Claude Code Hook Notification System - Windows Setup
echo ======================================================
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python yuklu degil!
    echo Python'u https://www.python.org adresinden indirin.
    pause
    exit /b 1
)

echo [OK] Python bulundu
echo.

REM pip guncelleme
echo Python paketleri yukleniyor...
python -m pip install --upgrade pip

REM Bagimliliklari yukle
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [HATA] Bazi paketler yuklenemedi!
    pause
    exit /b 1
)

echo.
echo ======================================================
echo  Kurulum tamamlandi!
echo ======================================================
echo.
echo Simdi yapmaniz gerekenler:
echo.
echo 1. .claude klasorunu projenizin ana dizinine kopyalayin
echo 2. Claude Code'da /hooks komutunu calistirin
echo 3. Test icin: python .claude/hooks/test-notifications.py
echo.
echo Telegram kullanmak icin:
echo - .claude/hooks/telegram-bot/telegram-config.json olusturun
echo - README'deki Telegram kurulum adimlarini takip edin
echo.
pause