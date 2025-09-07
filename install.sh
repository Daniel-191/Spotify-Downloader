#!/bin/bash
echo "=============================="
echo "   Spotify Downloader Setup"
echo "=============================="

# Upgrade pip (if its needed)
pip install --upgrade pip

pip install -r requirements.txt

# Display a nice finish message
echo
echo "=============================="
echo "   Setup Complete!"
echo "   Run with:"
echo "   python3 main.py"
echo "=============================="
