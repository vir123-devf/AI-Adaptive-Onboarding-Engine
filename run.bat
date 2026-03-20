@echo off
REM AI-Adaptive Onboarding Engine - Windows Startup Script

setlocal enabledelayedexpansion

echo.
echo ======================================
echo  AI-Adaptive Onboarding Engine
echo ======================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [*] Creating .env file...
    (
        echo ANTHROPIC_API_KEY=your-key-here
        echo HOST=0.0.0.0
        echo PORT=8000
        echo DEBUG=False
        echo CATALOG_PATH=course_catalog.json
        echo MAX_HOURS=40.0
    ) > .env
    echo [!] Please update .env with your API key
)

REM Check if virtual environment exists
if not exist ".venv\" (
    echo [*] Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo [*] Installing dependencies...
pip install -q -r requirements.txt

REM Load environment from .env
echo [*] Loading environment variables...
for /f "delims== tokens=1,2" %%a in (.env) do (
    if "%%a"=="ANTHROPIC_API_KEY" (
        set "ANTHROPIC_API_KEY=%%b"
    )
)

REM Check if API key is set
if "!ANTHROPIC_API_KEY!"=="" (
    echo [ERROR] ANTHROPIC_API_KEY not set in .env
    exit /b 1
)

echo [OK] Starting server on http://localhost:8000
echo.

REM Start the server
python main.py

pause
