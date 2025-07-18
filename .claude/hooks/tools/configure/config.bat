@echo off
:: Claude Code Hook Notification Configurator
:: Works from any location - finds the correct paths automatically

setlocal

:: Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python 3.7 or later
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

:: Set the config file path as environment variable (v2.0 structure)
set CLAUDE_NOTIFICATION_CONFIG=%SCRIPT_DIR%..\..\core\config.yaml

:: Run the configuration tool with relative path
%PYTHON% "%SCRIPT_DIR%configure.py" %*

endlocal