# 🎵 Spotify Downloader

Download your **Spotify playlists, albums, and tracks** for free!
This script takes a **Spotify link** (album, playlist, or track) and downloads the corresponding audio directly from **YouTube**, converting it with `ffmpeg`.

---

## ✨ Features
- 🔗 Paste a **Spotify link** (playlist / album / track) and let the script do the rest
- 📂 Downloads full **playlists**, **albums**, or single tracks
- 🎶 Converts audio to **MP3** format using `ffmpeg`
- 🎨 Beautiful **colored console output** with progress bars
- 🖥️ **Modern PyQt6 GUI** - Clean, modern desktop interface
- 🌐 **Web Interface** - Gradio-based web UI for browser access
- ⚡ Simple setup with **automated installation scripts**
- 🖥 Cross-platform support: **Windows**, **macOS**, **Linux**
- 🔄 **Multiple extraction methods** - Tries different approaches to fetch track lists
- ✅ **Error handling** - Automatically retries failed downloads

---

## 📦 Requirements
Make sure you have the following before starting:
- [Python 3.10+](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org/download.html) (required for MP3 conversion)
- Internet connection (to fetch from Spotify + YouTube)

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/Daniel-191/collaborative
cd collaborative
```

### 2. Install dependencies
- **Windows:** Double-click `install.bat` or run:
  ```bash
  install.bat
  ```

- **macOS/Linux (Terminal):**
  ```bash
  chmod +x install.sh
  ./install.sh
  ```

- **Manual Installation:**
  ```bash
  pip install -r requirements.txt
  ```

### 3. Install `ffmpeg`
You'll need `ffmpeg` installed and accessible in your system PATH.

- **Windows:**
  1. Download ffmpeg from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
  2. Extract the downloaded ZIP file to a folder
  3. Add ffmpeg to your system PATH:
     - Open **System Properties** → **Environment Variables**
     - Under **System Variables**, find and edit **Path**
     - Add the path to ffmpeg's `bin` folder
     - Click **OK** to save
  4. Restart your command prompt and verify with: `ffmpeg -version`

  **Need help?** Watch this tutorial for guidance: https://www.youtube.com/watch?v=jZLqNocSQDM&t=33s

- **macOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **Linux (Fedora):**
  ```bash
  sudo dnf install ffmpeg
  ```

- **Linux (Arch):**
  ```bash
  sudo pacman -S ffmpeg
  ```

---

## 🚀 Usage

### Choose Your Interface

This application offers three different interfaces:

#### 1️⃣ Desktop GUI (PyQt6) - **Recommended**

Launch the modern desktop application:

```bash
python gui.py
# or
python3 gui.py
# or use the launcher
python run_gui.py
```

Features:
- 🎨 Modern, clean dark-themed interface
- 📊 Real-time progress tracking
- ⚙️ Advanced audio format settings
- 📈 Live statistics display
- 🖱️ Easy-to-use graphical controls

#### 2️⃣ Web Interface (Gradio)

Launch the web-based interface:

```bash
python main.py
# or
python3 main.py
```

> **Note:** After running the installation script, you can also use `run.bat` (Windows) or `./run.sh` (macOS/Linux) as convenient shortcuts.

Access through your browser at `http://localhost:7860`

#### 3️⃣ Command Line Interface (CLI)

For terminal users:

```bash
python cli.py "https://open.spotify.com/playlist/..."
```

### Using the Downloader

When prompted, paste a Spotify link:
- 🎵 **Track** → `https://open.spotify.com/track/...` → downloads the song
- 💿 **Album** → `https://open.spotify.com/album/...` → downloads all songs in the album
- 🎶 **Playlist** → `https://open.spotify.com/playlist/...` → downloads the entire playlist

The script will:
1. Extract track information from Spotify
2. Search for each track on YouTube
3. Download the best audio match
4. Convert to MP3 format
5. Save to the `downloaded/` folder

---

## 🖥 Supported Operating Systems
- ✅ Windows
- ✅ macOS
- ✅ Linux

---

**Contributors:**
- Daniel-191
- ShellDrak3
- JayM2F

---

## 📝 Dependencies
This project uses the following Python packages:

| Package | Purpose |
|---------|---------|
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube downloading |
| [requests](https://requests.readthedocs.io/) | HTTP requests to Spotify |
| [colorama](https://github.com/tartley/colorama) | Colored terminal output |
| [urllib3](https://urllib3.readthedocs.io/) | HTTP client utilities |
| [gradio](https://www.gradio.app) | Web interface |
| [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) | Desktop GUI framework |

**External Dependencies:**
- [FFmpeg](https://ffmpeg.org/) - Audio conversion (must be installed separately)

---

## ⚖️ License
This project is open source and available for educational purposes.

---

> [!WARNING]
> This project is for **educational purposes only**.
> Downloading copyrighted content without permission may violate copyright laws.
> Please support artists by streaming legally on [Spotify](https://spotify.com) or purchasing their music.

---

## 🌟 Star This Repository
If you found this useful, please ⭐ star this repository!

---

**Made with ❤️ by the collaborative team**
