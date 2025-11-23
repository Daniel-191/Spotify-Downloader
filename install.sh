#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "  SPOTIFY DOWNLOADER - INSTALLATION"
echo ""

# Detect OS
OS_TYPE=$(uname -s)

# Step 1: Check Python Installation
echo -e "${CYAN}[1/6] Checking Python installation...${NC}"

PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}${ERROR} Python is not installed${NC}"
    echo ""
    echo "Please install Python 3.7 or higher:"
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo "  macOS: brew install python3"
        echo "  Or download from: https://www.python.org/downloads/"
    elif [[ "$OS_TYPE" == "Linux" ]]; then
        echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
        echo "  Fedora: sudo dnf install python3 python3-pip"
        echo "  Arch: sudo pacman -S python python-pip"
    fi
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}[SUCCESS] Python ${PYTHON_VERSION} found${NC}"
echo ""

# Check Python version is 3.7+
MAJOR_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info.major)')
MINOR_VERSION=$($PYTHON_CMD -c 'import sys; print(sys.version_info.minor)')

if [[ $MAJOR_VERSION -lt 3 ]] || [[ $MAJOR_VERSION -eq 3 && $MINOR_VERSION -lt 7 ]]; then
    echo -e "${RED}${ERROR} Python 3.7 or higher is required${NC}"
    echo "Current version: ${PYTHON_VERSION}"
    echo "Please upgrade Python"
    exit 1
fi

# Step 2: Check pip
echo -e "${CYAN}[2/6] Checking pip installation...${NC}"

if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo -e "${RED}[ERROR] pip is not installed bruh${NC}"
    echo "Installing pip..."

    if [[ "$OS_TYPE" == "Darwin" ]]; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        $PYTHON_CMD get-pip.py
        rm get-pip.py
    elif [[ "$OS_TYPE" == "Linux" ]]; then
        if command -v apt &> /dev/null; then
            sudo apt install python3-pip -y
        elif command -v dnf &> /dev/null; then
            sudo dnf install python3-pip -y
        elif command -v pacman &> /dev/null; then
            sudo pacman -S python-pip --noconfirm
        else
            $PYTHON_CMD -m ensurepip --default-pip
        fi
    fi

    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        echo -e "${RED}${ERROR} Failed to install pip${NC}"
        exit 1
    fi
fi

PIP_VERSION=$($PYTHON_CMD -m pip --version | awk '{print $2}')
echo -e "${GREEN}[SUCCESS] pip is available${NC}"
echo ""

# Step 3: Upgrade pip
echo -e "${CYAN}[3/6] Upgrading pip to latest version...${NC}"

if $PYTHON_CMD -m pip install --upgrade pip --quiet 2>/dev/null; then
    echo -e "${GREEN}[SUCCESS] pip upgraded successfully${NC}"
else
    echo -e "${YELLOW}[WARNING] Failed to upgrade pip, continuing with current version${NC}"
fi
echo ""

# Step 4: Install required packages
echo -e "${CYAN}[4/6] Installing required Python packages...${NC}"
echo "This may take a few minutes..."
echo ""

PACKAGES=("yt-dlp" "requests" "colorama" "urllib3")
INSTALL_ERROR=0

for package in "${PACKAGES[@]}"; do
    echo "Installing ${package}..."

    if $PYTHON_CMD -m pip install "$package" --quiet --disable-pip-version-check 2>/dev/null; then
        echo -e "${GREEN}[SUCCESS] ${package} installed${NC}"
    else
        echo -e "${RED}[ERROR] Failed to install ${package}${NC}"
        echo "Retrying with --user flag..."
        if $PYTHON_CMD -m pip install "$package" --user --quiet --disable-pip-version-check 2>/dev/null; then
            echo -e "${GREEN}[SUCCESS] ${package} installed with --user flag${NC}"
        else
            echo -e "${RED}[ERROR] Failed to install ${package} even with --user flag${NC}"
            echo "Please try manually: pip install ${package}"
            INSTALL_ERROR=1
        fi
    fi
done
echo ""

if [ $INSTALL_ERROR -ne 0 ]; then
    echo -e "${YELLOW}[WARNING] Some packages failed to install${NC}"
    echo "Please check the errors above"
    echo ""
fi

# Step 5: Check FFmpeg
echo -e "${CYAN}[5/6] Checking FFmpeg installation...${NC}"

if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n 1 | awk '{print $3}')
    echo -e "${GREEN}[SUCCESS] FFmpeg is installed${NC}"
    echo "FFmpeg version: ${FFMPEG_VERSION}"
    FFMPEG_MISSING=0
else
    echo -e "${YELLOW}[WARNING] FFmpeg is not installed or not in PATH${NC}"
    echo ""
    echo "FFmpeg is required for MP3 conversion"
    echo ""
    echo "To install FFmpeg:"
    if [[ "$OS_TYPE" == "Darwin" ]]; then
        echo "  macOS: brew install ffmpeg"
    elif [[ "$OS_TYPE" == "Linux" ]]; then
        echo "  Ubuntu/Debian: sudo apt install ffmpeg"
        echo "  Fedora: sudo dnf install ffmpeg"
        echo "  Arch: sudo pacman -S ffmpeg"
    fi
    echo ""
    echo "Without FFmpeg, downloads will be in original format (WebM/M4A, so unreadable lol)"
    echo ""
    FFMPEG_MISSING=1
fi
echo ""

# Step 6: Verify installation
echo -e "${CYAN}[6/6] Verifying installation...${NC}"
echo ""

# Test imports
if ! $PYTHON_CMD -c "import yt_dlp; import requests; import colorama; import urllib3" 2>/dev/null; then
    echo -e "${RED}[ERROR] Failed to import required packages${NC}"
    echo "Please check the installation errors above"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Test library import
if [ -f "spotify_lib.py" ]; then
    if ! $PYTHON_CMD -c "from spotify_lib import SpotifyDownloader; print('Library import successful')" 2>/dev/null; then
        echo -e "${RED}[ERROR] Failed to import spotify_lib.py${NC}"
        echo "Please check if the file exists and has no syntax errors"
        echo ""
        read -p "Press Enter to exit..."
        exit 1
    fi
    echo -e "${GREEN}[SUCCESS] spotify_lib.py verified${NC}"
else
    echo -e "${YELLOW}[WARNING] spotify_lib.py not found in current directory${NC}"
    echo "Make sure you run this script from the project directory"
fi
echo ""

# Create download directory
if [ ! -d "downloaded" ]; then
    if mkdir downloaded 2>/dev/null; then
        echo -e "${GREEN}[SUCCESS] Created 'downloaded' directory${NC}"
    else
        echo -e "${YELLOW}[WARNING] Failed to create 'downloaded' directory${NC}"
    fi
else
    echo -e "${GREEN}[SUCCESS] 'downloaded' directory already exists${NC}"
fi
echo ""

# Installation summary
echo "========================================"
echo "  INSTALLATION SUMMARY"
echo "========================================"
echo ""
echo "Python Version: ${PYTHON_VERSION}"
echo "Required Packages: [OK]"

if [ $FFMPEG_MISSING -eq 1 ]; then
    echo "FFmpeg: [NOT FOUND]"
else
    echo "FFmpeg: [OK]"
fi
echo ""

if [ $FFMPEG_MISSING -eq 1 ]; then
    echo "[NOTICE] Installation completed with warnings"
    echo "Please install FFmpeg for full functionality"
else
    echo "[SUCCESS] Installation completed successfully!"
fi
echo ""
echo "You can now run: $PYTHON_CMD main.py"
echo ""

# Create a run script for convenience
cat > run.sh << EOF
#!/bin/bash
$PYTHON_CMD main.py
EOF

chmod +x run.sh
echo "[INFO] Created run.sh for easy launching"

echo ""
echo "Press any key to exit..."
read
