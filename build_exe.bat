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

if not exist ".venv\Scripts\activate.bat" (
    echo Creating the Python environment...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Could not create the virtual environment.
        pause
        exit /b 1
    )
)

call ".venv\Scripts\activate.bat"
echo Installing/updating dependencies and PyInstaller...
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt
python -m pip install -q --upgrade yt-dlp pyinstaller
if errorlevel 1 (
    echo [ERROR] Installing dependencies failed. Check your connection.
    pause
    exit /b 1
)

echo.
echo Building Cutito.exe (takes a minute or two)...
python -m PyInstaller --noconfirm --clean --onefile --noconsole --name Cutito --icon "cutito.ico" ^
    --add-data "index.html;." ^
    --collect-submodules yt_dlp ^
    app.py
if errorlevel 1 (
    echo [ERROR] Build failed. Read the messages above.
    pause
    exit /b 1
)

copy /y "dist\Cutito.exe" "Cutito.exe" >nul
echo.
echo DONE. Cutito.exe was created in this folder.
echo - Double-click Cutito.exe: no black window, the Cutito window opens.
echo - It closes by itself when you close the window.
echo - Videos end up in Videos\Cutito.
echo - ffmpeg must be installed (winget install Gyan.FFmpeg), or put ffmpeg.exe and
echo   ffprobe.exe in the same folder as Cutito.exe.
echo.
pause
