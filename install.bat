@echo off
setlocal enabledelayedexpansion
title nstallation Script
color 0B

echo   SPOTIFY DOWNLOADER - INSTALLATION
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Run bat file as administrator (if possible)
    echo Some stuff might need admin perms to install
    echo.
    timeout /t 3 >nul
)

:: Step 1: Check Python Installation
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found
echo.

:: Check Python version is 3.7+
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if !MAJOR! LSS 3 (
    echo [ERROR] Python 3.7 or higher is required
    echo Current version: %PYTHON_VERSION%
    echo Please upgrade Python
    pause
    exit /b 1
)

if !MAJOR! EQU 3 if !MINOR! LSS 7 (
    echo [ERROR] Python 3.7 or higher is required
    echo Current version: %PYTHON_VERSION%
    echo Please upgrade Python
    pause
    exit /b 1
)

:: Step 2: Check pip
echo [2/6] Checking pip installation...
python -m pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] pip is not installed bruh
    echo Installing pip...
    python -m ensurepip --default-pip
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to install pip
        pause
        exit /b 1
    )
)
echo [SUCCESS] pip is available
echo.

:: Step 3: Upgrade pip
echo [3/6] Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet
if %errorLevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing with current version
) else (
    echo [SUCCESS] pip upgraded successfully
)
echo.

:: Step 4: Install required packages
echo [4/6] Installing required Python packages...
echo This may take a few minutes...
echo.

set PACKAGES=yt-dlp requests colorama urllib3

for %%p in (%PACKAGES%) do (
    echo Installing %%p...
    python -m pip install %%p --quiet --disable-pip-version-check
    if !errorLevel! neq 0 (
        echo [ERROR] Failed to install %%p
        echo Retrying with --user flag...
        python -m pip install %%p --user --quiet --disable-pip-version-check
        if !errorLevel! neq 0 (
            echo [ERROR] Failed to install %%p even with --user flag
            echo Please try manually: pip install %%p
            set INSTALL_ERROR=1
        ) else (
            echo [SUCCESS] %%p installed with --user flag
        )
    ) else (
        echo [SUCCESS] %%p installed
    )
)
echo.

if defined INSTALL_ERROR (
    echo [WARNING] Some packages failed to install
    echo Please check the errors above
    echo.
)

:: Step 5: Check FFmpeg
echo [5/6] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] FFmpeg is not installed or not in PATH
    echo.
    echo FFmpeg is required for MP3 conversion
    echo.
    echo To install FFmpeg:
    echo   1. Download from: https://ffmpeg.org/download.html
    echo   2. Extract the ZIP file
    echo   3. Add the 'bin' folder to your system PATH
    echo.
    echo Without FFmpeg, downloads will be in original format (WebM/M4A , so unreadable lol)
    echo.
    set FFMPEG_MISSING=1
) else (
    echo [SUCCESS] FFmpeg is installed
    for /f "tokens=3" %%i in ('ffmpeg -version 2^>^&1 ^| findstr "ffmpeg version"') do (
        echo FFmpeg version: %%i
    )
)
echo.

:: Step 6: Verify installation
echo [6/6] Verifying installation...
echo.

:: Test imports
python -c "import yt_dlp; import requests; import colorama; import urllib3" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Failed to import required packages
    echo Please check the installation errors above
    echo.
    pause
    exit /b 1
)

:: Test library import
if exist spotify_lib.py (
    python -c "from spotify_lib import SpotifyDownloader; print('Library import successful')" >nul 2>&1
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to import spotify_lib.py
        echo Please check if the file exists and has no syntax errors
        echo.
        pause
        exit /b 1
    )
    echo [SUCCESS] spotify_lib.py verified
) else (
    echo [WARNING] spotify_lib.py not found in current directory
    echo Make sure you run this script from the project directory
)
echo.

:: Create download directory
if not exist "downloaded" (
    mkdir downloaded
    if %errorLevel% equ 0 (
        echo [SUCCESS] Created 'downloaded' directory
    ) else (
        echo [WARNING] Failed to create 'downloaded' directory
    )
) else (
    echo [SUCCESS] 'downloaded' directory already exists
)
echo.

:: Installation summary
echo ========================================
echo   INSTALLATION SUMMARY
echo ========================================
echo.
echo Python Version: %PYTHON_VERSION%
echo Required Packages: [OK]
if defined FFMPEG_MISSING (
    echo FFmpeg: [NOT FOUND]
) else (
    echo FFmpeg: [OK]
)
echo.

if defined FFMPEG_MISSING (
    echo [NOTICE] Installation completed with warnings
    echo Please install FFmpeg for full functionality
) else (
    echo [SUCCESS] Installation completed successfully!
)
echo.
echo You can now run: python main.py
echo.

:: Create a run script for convenience
echo @echo off > run.bat
echo python main.py >> run.bat
echo pause >> run.bat
echo [INFO] Created run.bat for easy launching

echo.
echo Press any key to exit...
pause >nul
