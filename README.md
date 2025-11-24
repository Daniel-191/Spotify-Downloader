# 🎵 Spotify Downloader

Download your **Spotify playlists, albums, and tracks** for free!
This script takes a **Spotify link** (album, playlist, or track) and downloads the corresponding audio directly from **YouTube**, converting it with `ffmpeg`.

---

## ✨ Features
- 🔗 Paste a **Spotify link** (playlist / album / track) and let the script do the rest
- 📂 Downloads full **playlists**, **albums**, or single tracks
- 🎶 Converts audio to **MP3** format using `ffmpeg`
- 🎨 Beautiful **colored console output** with progress bars
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
  ```Due to Ffmpeg being a bit of a pain to install, we fully recommened watching this video for window users: https://www.youtube.com/watch?v=jZLqNocSQDM&t=33s
   ```

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

### Quick Start

Run the program with:

```bash
python main.py
# or
python3 main.py
```

> **Note:** After running the installation script, you can also use `run.bat` (Windows) or `./run.sh` (macOS/Linux) as convenient shortcuts.

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

### Example
```
  SPOTIFY DOWNLOADER - INSTALLATION

Enter Spotify URL (track, album, or playlist):
Example: https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh

URL: https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M

• Detected playlist with ID: 37i9dQZF1DXcBWIGoYBM5M
✓ Found 50 tracks using Embed Page

[1/50] Searching for: 'Artist Name - Song Title'
✓ Found: Song Title - Artist Name
Downloading ████████████████████████████ 100.0% | 1.2 MB/s | 00:00
✓ Completed: Song Title.mp3
```

---

## 📂 Project Structure
```
spotify-downloader/
├── main.py                 # Main program entry point
├── spotify_lib.py          # Core library for downloading
├── install.bat             # Windows installation script
├── install.sh              # macOS/Linux installation script
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── downloaded/             # Downloaded audio files (auto-created)
```

**Note:** `run.bat` and `run.sh` launcher scripts are automatically created after running the installation.

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
| [gradio](https://www.gradio.app) | Webpage |

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
