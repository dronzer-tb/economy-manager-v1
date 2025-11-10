@echo off
REM Installation Script for Economy Manager V1 (Windows)
REM Version: 0.1.0

echo ================================
echo Economy Manager V1 - Installation
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo X pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo [OK] pip found
echo.

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully
echo.

echo ================================
echo Installation Complete!
echo ================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env
echo 2. Edit .env with your configuration
echo 3. Run setup: python scripts\setup.py
echo 4. Start the bot: python bot\main.py
echo.
pause
