# 🎵 Spotify Downloader

Download your **Spotify playlists, albums, and tracks** for free!  
This script takes a **Spotify link** (album, playlist, or track) and downloads the corresponding audio directly from **YouTube**, converting it with `ffmpeg`.  

---

## 🔄 How It Works
```mermaid
flowchart LR
    A[Spotify Link<br>(Playlist / Album / Track)] --> B[Find Match on YouTube]
    B --> C[Download Audio]
    C --> D[Convert with ffmpeg]
    D --> E[Saved MP3 / Audio File]
```

---

## ✨ Features
- 🔗 Paste a **Spotify link** (playlist / album / track) and let the script do the rest
- 📂 Downloads full **playlists**, **albums**, or single tracks
- 🎶 Converts audio to common formats using `ffmpeg`
- ⚡ Simple setup with `install.bat` / `install.sh`
- 🖥 Cross-platform support: **Windows**, **macOS**, **Linux**

---

## 📦 Requirements
Make sure you have the following before starting:
- [Python 3.8+](https://www.python.org/downloads/)  
- [ffmpeg](https://ffmpeg.org/download.html) (must be installed manually)  
- Internet connection (to fetch from Spotify + YouTube)

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/spotify-downloader.git
cd spotify-downloader
```

### 2. Install dependencies
- **Windows:** Double-click `install.bat`  
- **macOS/Linux (Terminal):**
  ```bash
  chmod +x install.sh
  ./install.sh
  ```

### 3. Install `ffmpeg`
You’ll need `ffmpeg` installed and accessible in your system PATH.

- **Windows:**  
  1. Download from [ffmpeg.org](https://ffmpeg.org/download.html).  
  2. Extract the folder (e.g., `ffmpeg-6.0-full_build`).  
  3. Add the `bin` folder to your PATH environment variable.  

- **macOS (Homebrew):**  
  ```bash
  brew install ffmpeg
  ```

- **Linux (Debian/Ubuntu):**  
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

---

## ▶️ Usage

- **Windows (easy way):**  
  Just double-click `main.py` to run the program.  

- **macOS/Linux (Terminal):**  
  ```bash
  python3 main.py
  ```

When prompted, paste a Spotify link:  
- 🎵 Track → downloads the song from YouTube  
- 💿 Album → downloads all songs in the album  
- 🎶 Playlist → downloads the entire playlist  

The script will fetch the best match from YouTube and automatically convert it to an audio file.

---

## 🖥 Supported Operating Systems
- ✅ Windows  
- ✅ macOS  
- ✅ Linux  

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
Please support artists by streaming legally on [Spotify](https://spotify.com).
