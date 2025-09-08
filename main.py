import yt_dlp
import requests
import re
import sys
import os
import json
import warnings
from colorama import Fore, Style, init, Back
from urllib.parse import urlparse, parse_qs
import urllib3
import time
import shutil

# Feel free to fork and contribute all you want.

# Supress any console logging or warning errors (they not needed)
warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)

init(autoreset=True) # this is for colorama

# Main class for the downloader
class SpotifyDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
        # Create download directory if it doesn't exist
        if not os.path.exists('downloaded'):
            os.makedirs('downloaded')
            self.print_success("Created 'downloaded' directory")
    
    # These functions are used for the CLI design etc

    def get_terminal_width(self):
        """Get terminal width for responsive design"""
        try:
            return shutil.get_terminal_size().columns
        except:
            return 80
    
    def print_header(self):
        """Print clean header"""
        width = self.get_terminal_width()
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * width}")
        print(f"{Fore.CYAN}{Style.BRIGHT}  SPOTIFY DOWNLOADER")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * width}")
    
    def print_separator(self):
        """Print section separator"""
        width = self.get_terminal_width()
        print(f"\n{Fore.CYAN}{'-' * width}")
    
    def print_success(self, message):
        """Print success message with icon"""
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ {message}")
    
    def print_warning(self, message):
        """Print warning message with icon"""
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠ {message}")
    
    def print_error(self, message):
        """Print error message with icon"""
        print(f"{Fore.RED}{Style.BRIGHT}✗ {message}")
    
    def print_info(self, message):
        """Print info message with icon"""
        print(f"{Fore.CYAN}{Style.BRIGHT}• {message}")
    
    def print_progress_bar(self, percentage, width=40):
        """Print a clean progress bar"""
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"{Fore.GREEN}{bar}{Fore.WHITE} {percentage:.1f}%"
    
    # Extract spotify id
    def extract_spotify_id(self, url):
        url = url.split('?')[0]  # Remove query parameters
        pattern = r'spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    # If link is playlist or album
    # This function will be used to fetch the list of tracks/songs
    def get_tracks_from_url(self, url):
        tracks = []
        content_type, spotify_id = self.extract_spotify_id(url)
        
        # Double check if url is valid
        if not content_type or not spotify_id:
            self.print_error("Invalid Spotify URL format")
            return tracks
        
        self.print_info(f"Detected {content_type} with ID: {spotify_id}")
        
        # Try multiple approaches
        approaches = [
            ("oEmbed API", self.try_oembed_api),
            ("Embed Page", self.try_embed_page),
            ("Direct Page", self.try_direct_page),
            ("Manual Input", self.try_manual_input)
        ]
        
        # Loop through tracks adding them to the list
        for name, approach in approaches:
            try:
                print(f"\n{Fore.CYAN}Trying {name}...")
                tracks = approach(content_type, spotify_id, url)
                if tracks:
                    self.print_success(f"Found {len(tracks)} tracks using {name}")
                    break
                else:
                    self.print_warning(f"No tracks found with {name}")
            except Exception as e:
                self.print_error(f"Error with {name}: {str(e)[:50]}...")
        
        # return list of tracks to be downloaded
        return tracks
    
    # API used to fetching track info
    def try_oembed_api(self, content_type, spotify_id, url):
        """Try Spotify's oEmbed API"""
        tracks = []
        try:
            oembed_url = f"https://open.spotify.com/oembed?url={url}"
            response = self.session.get(oembed_url)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', '')
                if title:
                    # For single tracks, the title normally has "artist - song"
                    if content_type == 'track':
                        tracks.append(title)
                    else: # This runs if the link is an album or playlsit
                        # For playlists and albums we need to extrack the tracks differently
                        self.print_info(f"Found {content_type}: {title}")
        except:
            pass
        return tracks
    
    def try_embed_page(self, content_type, spotify_id, url):
        """Try the embed page approach with better parsing"""
        tracks = []
        try:
            embed_url = f"https://open.spotify.com/embed/{content_type}/{spotify_id}"
            
            response = self.session.get(embed_url)
            if response.status_code == 200:
                html = response.text
                
                # Look for JSON data in various script tags
                json_patterns = [
                    r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                    r'window\.__PRELOADED_STATE__\s*=\s*({.*?});',
                    r'window\.Spotify\s*=\s*({.*?});',
                    r'__NEXT_DATA__"\s*type="application/json">({.*?})</script>',
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, html, re.DOTALL)
                    for match in matches:
                        try:
                            data = json.loads(match)
                            extracted = self.extract_tracks_from_json(data)
                            if extracted:
                                tracks.extend(extracted)
                        except:
                            continue
                
                # If no JSON found, try regex
                if not tracks:
                    tracks = self.enhanced_regex_extract(html)
                    
        except Exception as e:
            self.print_error(f"Embed page error: {e}")
        
        return tracks
    
    def try_direct_page(self, content_type, spotify_id, url):
        """Try the direct Spotify page"""
        tracks = []
        try:
            direct_url = f"https://open.spotify.com/{content_type}/{spotify_id}"
            
            response = self.session.get(direct_url)
            if response.status_code == 200:
                html = response.text
                tracks = self.enhanced_regex_extract(html)
                
        except Exception as e:
            self.print_error(f"Direct page error: {e}")
        
        return tracks
    
    # Manually input tracks via entering them in this format
    # 'Artist Name - Title'
    def try_manual_input(self, content_type, spotify_id, url):
        """Fallback to manual input"""
        print(f"\n{Fore.YELLOW}Automatic extraction failed. Manual input required.")
        print(f"{Fore.CYAN}Please open this URL in your browser: {Fore.WHITE}{url}")
        
        input(f"\n{Fore.MAGENTA}Press Enter when ready to input songs...")
        
        tracks = []
        print(f"\n{Fore.GREEN}Enter songs in format: 'Artist - Song Title'")
        print(f"{Fore.CYAN}Press Enter on empty line when done")
        
        while True:
            prompt = f"{Fore.MAGENTA}Song {len(tracks) + 1}: {Fore.WHITE}"
            song = input(prompt).strip()
            if not song:
                if len(tracks) == 0:
                    self.print_warning("No songs entered. Try again or press Enter to skip.")
                    continue
                break
            tracks.append(song)
            self.print_success(f"Added: {song}")
        
        return tracks
    
    # Used for some extraction stuff
    def enhanced_regex_extract(self, html):
        """Enhanced regex extraction with multiple patterns"""
        tracks = []
        
        # More comprehensive regex patterns
        patterns = [
            # JSON-LD structured data
            r'"@type":"MusicRecording".*?"name":"([^"]+)".*?"byArtist".*?"name":"([^"]+)"',
            # Open Graph meta tags
            r'<meta property="music:song" content="([^"]+)"',
            r'<meta property="og:title" content="([^"]*?(?:by|-).*?)"',
            # Schema.org microdata
            r'itemprop="name"[^>]*>([^<]+)<.*?itemprop="byArtist"[^>]*>([^<]+)<',
            # Spotify embed data
            r'"track":{"uri":"spotify:track:[^"]*","name":"([^"]+)".*?"artists":\[{"name":"([^"]+)"',
            # Alternative JSON structures
            r'"name":"([^"]+)"[^}]*"artists":\[{"name":"([^"]+)"',
            r'"title":"([^"]+)"[^}]*"subtitle":"([^"]+)"',
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    artist, song = match[0].strip(), match[1].strip()
                    if artist and song and len(artist) > 1 and len(song) > 1:
                        track = f"{artist} - {song}"
                        if track not in tracks:
                            tracks.append(track)
                elif isinstance(match, str):
                    # Single match, try to parse artist - song format
                    match = match.strip()
                    if ' - ' in match or ' by ' in match:
                        if match not in tracks:
                            tracks.append(match)
        
        # Remove duplicates and filter
        unique_tracks = []
        seen = set()
        for track in tracks:
            track_clean = re.sub(r'\s+', ' ', track).strip()
            if (track_clean not in seen and 
                len(track_clean) > 5 and 
                not track_clean.lower().startswith('spotify') and
                ' - ' in track_clean):
                seen.add(track_clean)
                unique_tracks.append(track_clean)
        
        return unique_tracks[:50]  # Limit to 50 tracks
    
    def extract_tracks_from_json(self, data):
        """Recursively extract tracks from JSON data"""
        tracks = []
        
        def recursive_search(obj, path=""):
            if isinstance(obj, dict):
                # Look for track patterns
                if 'name' in obj and 'artists' in obj:
                    track_name = obj.get('name', '').strip()
                    artists = obj.get('artists', [])
                    if isinstance(artists, list) and len(artists) > 0:
                        artist_name = ''
                        if isinstance(artists[0], dict):
                            artist_name = artists[0].get('name', '').strip()
                        elif isinstance(artists[0], str):
                            artist_name = artists[0].strip()
                        
                        if track_name and artist_name:
                            track = f"{artist_name} - {track_name}"
                            if track not in tracks:
                                tracks.append(track)
                
                # Continue recursive search
                for key, value in obj.items():
                    recursive_search(value, f"{path}.{key}" if path else key)
                    
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    recursive_search(item, f"{path}[{i}]" if path else f"[{i}]")
        
        recursive_search(data)
        return tracks
    
    # This is used to create the download progess bar when downloading tracks
    def progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percent_str = d.get('_percent_str', '0.0%').replace('%', '')
                percent = float(percent_str) if percent_str.replace('.', '').isdigit() else 0
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')
                
                progress_bar = self.print_progress_bar(percent, 30)
                sys.stdout.write(
                    f"\r{Fore.CYAN}Downloading {progress_bar} {Fore.MAGENTA}| {Fore.GREEN}{speed} {Fore.MAGENTA}| {Fore.YELLOW}{eta}     "
                )
                sys.stdout.flush()
            except:
                sys.stdout.write(f"\r{Fore.CYAN}Downloading...     ")
                sys.stdout.flush()
        elif d['status'] == 'finished':
            filename = os.path.basename(d['filename'])
            print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Completed: {Fore.WHITE}{filename}")
    
    # After fetching tracks from spotify
    # Tracks are downloaded from youtube
    def download_from_youtube(self, query):
        print(f"{Fore.CYAN}Searching for: {Fore.WHITE}'{query}'")
        
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloaded/%(title)s.%(ext)s",
            "noplaylist": True,
            "progress_hooks": [self.progress_hook],
            "quiet": True,  # Suppress most output
            "no_warnings": True,  # Suppress warnings
            "extractaudio": True,
            "audioformat": "mp3",
            "audioquality": "192K",
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                search_query = f"ytsearch1:{query}"  # Only get first result
                info = ydl.extract_info(search_query, download=False)
                
                if 'entries' in info and len(info['entries']) > 0:
                    video = info['entries'][0]
                    video_title = video['title']
                    print(f"{Fore.GREEN}✓ Found: {Fore.WHITE}{video_title}")
                    
                    # Download the video
                    ydl.download([search_query])
                else:
                    self.print_error(f"No results found for: {query}")
                    
            except Exception as e:
                self.print_error(f"Download failed for '{query}': {str(e)[:50]}...")
    
    # Displays all tracks before being downloaded
    def display_tracks_preview(self, songs):
        """Display tracks in a clean list format"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Found {len(songs)} track(s):")
        
        for i, song in enumerate(songs, 1):
            print(f"{Fore.CYAN}{i:3d}. {Fore.WHITE}{song}")
    
    # Confirm download
    def download_from_spotify(self, url):
        print(f"\n{Fore.CYAN}Processing Spotify URL...")
        
        songs = self.get_tracks_from_url(url)
        
        if not songs:
            self.print_error("No tracks found. Exiting...")
            return
        
        self.display_tracks_preview(songs)
        
        print(f"\n{Fore.YELLOW}Continue with download? {Fore.WHITE}[Y/n]: ", end="")
        proceed = input().lower()
        if proceed not in ['y', 'yes', '']:
            self.print_info("Download cancelled")
            return
        
        self.print_separator()
        print(f"{Fore.CYAN}{Style.BRIGHT}Starting downloads...\n")
        
        # Download each song
        for i, song in enumerate(songs, 1):
            print(f"\n{Fore.MAGENTA}[{i}/{len(songs)}] ", end="")
            self.download_from_youtube(song)
            
            if i < len(songs):  # Don't sleep after the last song
                time.sleep(1)  # Small delay between downloads
        
        self.show_download_summary()
    
    # Download summary once its complete
    def show_download_summary(self):
        """Show clean download summary"""
        self.print_separator()
        
        if os.path.exists('downloaded'):
            files = [f for f in os.listdir('downloaded') if f.endswith(('.mp3', '.m4a', '.webm'))]
            if files:
                print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ Successfully downloaded {len(files)} files")
                print(f"{Fore.CYAN}Location: {Fore.WHITE}./downloaded/")
                
                # Show first few files
                print(f"\n{Fore.CYAN}Files:")
                for i, file in enumerate(files[:5], 1):
                    print(f"{Fore.WHITE}  {file}")
                
                if len(files) > 5:
                    print(f"{Fore.CYAN}  ... and {len(files) - 5} more files")
            else:
                self.print_warning("No audio files found in download folder")
        
        print(f"\n{Fore.CYAN}Press Enter to exit...")
        input()

# Checks depedencies b4 running
# Returns error message if ffmeg is missing
def check_dependencies():
    """Check and display dependency status"""
    downloader = SpotifyDownloader()
    
    # Check FFmpeg
    ffmpeg_available = False
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            downloader.print_success("FFmpeg available - MP3 conversion enabled")
            ffmpeg_available = True
        else:
            downloader.print_warning("FFmpeg issue detected")
    except FileNotFoundError:
        downloader.print_warning("FFmpeg not found - files will be in original format")
        print(f"{Fore.CYAN}To get MP3 files, install FFmpeg:")
        print(f"{Fore.WHITE}  macOS: {Fore.YELLOW}brew install ffmpeg")
        print(f"{Fore.WHITE}  Ubuntu: {Fore.YELLOW}sudo apt install ffmpeg")
        print(f"{Fore.WHITE}  Windows: Download from https://ffmpeg.org")
        
        proceed = input(f"\n{Fore.CYAN}Continue without MP3 conversion? [Y/n]: ")
        if proceed.lower() not in ['y', 'yes', '']:
            exit(1)
    
    downloader.print_success("yt-dlp ready")
    downloader.print_success("Download directory prepared")
    
    return downloader


if __name__ == "__main__":
    # clear terminal
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # check requirements
    sd = check_dependencies()

    sd.print_header()
    
    # url input
    print(f"\n{Fore.CYAN}Enter Spotify URL (track, album, or playlist):")
    print(f"{Fore.YELLOW}Example: https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh")
    
    link = input(f"\n{Fore.MAGENTA}URL: {Fore.WHITE}")
    
    # Download song/playlist/album
    if link.strip():
        sd.download_from_spotify(link.strip())
    else:
        sd.print_error("No URL provided. Exiting...")
        time.sleep(2)