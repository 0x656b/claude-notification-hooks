@echo off
:: Debug mode for Claude notifications

echo Debug mode enabled for Claude notifications
echo.

:: Enable debug mode
set CLAUDE_DEBUG=true

:: Test various tool/event combinations
echo Testing Bash PreToolUse:
python .claude\hooks\config-manager\notify-all.py Bash PreToolUse
echo.

echo Testing Edit PreToolUse:
python .claude\hooks\config-manager\notify-all.py Edit PreToolUse
echo.

echo Testing Stop event:
python .claude\hooks\config-manager\notify-all.py default Stop
echo.

pause