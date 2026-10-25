@echo off
chcp 65001 >nul
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo [ERROR] Python not found. Install it from https://www.python.org/downloads/
    echo During installation tick "Add python.exe to PATH".
    pause
    exit /b 1
)

where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [ERROR] ffmpeg not found. Open a terminal and run:
    echo     winget install Gyan.FFmpeg
    echo Then close and reopen this window and run start.bat again.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\activate.bat" (
    echo First run: creating the Python environment...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Could not create the virtual environment.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
echo Installing/updating dependencies (yt-dlp is updated on every start, YouTube breaks it often)...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt
python -m pip install -q --upgrade yt-dlp
if errorlevel 1 (
    echo [ERROR] Installing dependencies failed. Check your connection.
    pause
    exit /b 1
)

echo.
echo Starting Cutito at http://127.0.0.1:5000  (close this window to stop it)
python app.py
pause
