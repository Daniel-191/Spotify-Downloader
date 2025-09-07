@echo off
echo ==============================
echo   Spotify Downloader Setup
echo ==============================

REM Upgrade pip (it might be needed)
python -m pip install --upgrade pip

pip install -r requirements.txt

REM Display a nice finish message
echo.
echo ==============================
echo   Setup Complete!
echo   Run with:
echo   python main.py
echo ==============================
pause
