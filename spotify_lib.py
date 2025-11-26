import yt_dlp
import requests
import re
import sys
import os
import json
import warnings
from colorama import Fore, Style, init # This library is to make the console look nice and everything
import urllib3


# Suppress any useless console warnings
warnings.filterwarnings("ignore")
urllib3.disable_warnings(urllib3.exceptions.NotOpenSSLWarning)


init(autoreset=True) # colorama


class SpotifyDownloader:
    def __init__(self, download_dir='downloaded'):
        self.download_dir = download_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        })

        # Create download directory if not already created
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            self.print_success(f"Created '{self.download_dir}' directory")

    # ===== Console Output Methods =====
    # These functions are used throughout the code for many different things
    # Its mainly for the overall look and design.

    def print_success(self, message):
        """Print success message"""
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ {message}")

    def print_error(self, message):
        """Print error message"""
        print(f"{Fore.RED}{Style.BRIGHT}✗ {message}")

    def print_warning(self, message):
        """Print warning message"""
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠ {message}")

    def print_info(self, message):
        """Print info message"""
        print(f"{Fore.CYAN}{Style.BRIGHT}• {message}")

    def print_progress_bar(self, percentage, width=40):
        """Just a single progress bar used for downloading"""
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"{Fore.GREEN}{bar}{Fore.WHITE} {percentage:.1f}%"

    # ===== URL Validation =====
    # Anytime a url is parsed, this function will be called

    def validate_url(self, url):
        """
        Validate if the URL is a valid Spotify URL

        Args:
            url (str): URL to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            self.print_error("URL cannot be empty")
            return False

        url = url.strip()

        # Check if it contains spotify.com
        if "spotify.com" not in url:
            self.print_error("URL must be a Spotify URL (must contain 'spotify.com')")
            return False

        # Check if it matches the pattern for track/album/playlist
        pattern = r'spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
        match = re.search(pattern, url)

        if not match:
            self.print_error("Invalid Spotify URL format")
            self.print_info("Expected format: https://open.spotify.com/[track|album|playlist]/ID")
            return False

        content_type = match.group(1)
        # Silent validation, no need for a success message or anything
        #self.print_success(f"Valid Spotify {content_type} URL")
        return True

    # ===== Core Extraction Methods =====

    def extract_spotify_id(self, url):
        """
        Extract Spotify content type and ID from URL (id is needed to download it)

        Args:
            url (str): Spotify URL

        Returns:
            tuple: (content_type, spotify_id) or (None, None) if invalid
        """
        url = url.split('?')[0]
        pattern = r'spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def get_tracks_from_url(self, url):
        """
        fetches track list from Spotify URL

        Args:
            url (str): Spotify URL (track, album, or playlist)

        Returns:
            list: List of track strings in "Artist - Title" format
        """
        tracks = []

        # Validate URL first
        if not self.validate_url(url):
            return tracks

        content_type, spotify_id = self.extract_spotify_id(url)

        if not content_type or not spotify_id:
            self.print_error("Invalid Spotify URL format")
            return tracks

        self.print_info(f"Detected {content_type} with ID: {spotify_id}")

        # Try multiple extraction methods
        approaches = [
            ("oEmbed API", self.try_oembed_api),
            ("Embed Page", self.try_embed_page),
            ("Direct Page", self.try_direct_page)
        ]

        for name, approach in approaches:
            try:
                print(f"{Fore.CYAN}Trying {name}...")
                tracks = approach(content_type, spotify_id, url)
                if tracks:
                    self.print_success(f"Found {len(tracks)} tracks using {name}")
                    break
                else:
                    self.print_warning(f"No tracks found with {name}")
            except Exception as e:
                self.print_error(f"Error with {name}: {str(e)[:50]}...")

        return tracks

    def try_oembed_api(self, content_type, spotify_id, url):
        """Try Spotify's oEmbed API"""
        tracks = []
        try:
            oembed_url = f"https://open.spotify.com/oembed?url={url}"
            response = self.session.get(oembed_url)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', '')
                if title and content_type == 'track':
                    tracks.append(title)
                elif title:
                    self.print_info(f"Found {content_type}: {title}")
        except:
            pass
        return tracks

    def try_embed_page(self, content_type, spotify_id, url):
        """Try the embed page approach"""
        tracks = []
        try:
            embed_url = f"https://open.spotify.com/embed/{content_type}/{spotify_id}"
            response = self.session.get(embed_url)

            if response.status_code == 200:
                html = response.text

                # Look for JSON data in script tags
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

                # Fallback to regex extraction
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
                tracks = self.enhanced_regex_extract(response.text)

        except Exception as e:
            self.print_error(f"Direct page error: {e}")

        return tracks

    def enhanced_regex_extract(self, html):
        """Enhanced regex extraction from HTML"""
        tracks = []

        patterns = [
            r'"@type":"MusicRecording".*?"name":"([^"]+)".*?"byArtist".*?"name":"([^"]+)"',
            r'<meta property="music:song" content="([^"]+)"',
            r'<meta property="og:title" content="([^"]*?(?:by|-).*?)"',
            r'itemprop="name"[^>]*>([^<]+)<.*?itemprop="byArtist"[^>]*>([^<]+)<',
            r'"track":{"uri":"spotify:track:[^"]*","name":"([^"]+)".*?"artists":\[{"name":"([^"]+)"',
            r'"name":"([^"]+)"[^}]*"artists":\[{"name":"([^"]+)"',
            r'"title":"([^"]+)"[^}]*"subtitle":"([^"]+)"',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) >= 2:
                    artist, song = match[0].strip(), match[1].strip()
                    if artist and song and len(artist) > 1 and len(song) > 1:
                        track = f"{artist} - {song}"
                        if track not in tracks:
                            tracks.append(track)
                elif isinstance(match, str):
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

        return unique_tracks[:50]

    def extract_tracks_from_json(self, data):
        """Recursively extract tracks from JSON data"""
        tracks = []

        def recursive_search(obj):
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
                for value in obj.values():
                    recursive_search(value)

            elif isinstance(obj, list):
                for item in obj:
                    recursive_search(item)

        recursive_search(data)
        return tracks

    # ===== Download Methods =====

    def progress_hook(self, d):
        """Progress bar for yt-dlp downloads"""
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

    def download_track(self, query, audio_format='mp3', quality='192'):
        """
        Download a single track from YouTube

        Args:
            query (str): Search query (e.g., "Artist - Title")
            audio_format (str): Output audio format (default: 'mp3')
            quality (str): Audio quality in kbps (default: '192')

        Returns:
            bool: True if successful, False otherwise
        """
        print(f"{Fore.CYAN}Searching for: {Fore.WHITE}'{query}'")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{self.download_dir}/%(title)s.%(ext)s",
            "noplaylist": True,
            "progress_hooks": [self.progress_hook],
            "quiet": True,
            "no_warnings": True,
            "extractaudio": True,
            "audioformat": audio_format,
            "audioquality": f"{quality}K",
            "postprocessors": [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_format,
                'preferredquality': quality,
            }]
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch1:{query}"
                info = ydl.extract_info(search_query, download=False)

                if 'entries' in info and len(info['entries']) > 0:
                    video = info['entries'][0]
                    video_title = video['title']
                    print(f"{Fore.GREEN}✓ Found: {Fore.WHITE}{video_title}")
                    ydl.download([search_query])
                    return True
                else:
                    self.print_error(f"No results found for: {query}")
                    return False

        except Exception as e:
            self.print_error(f"Download failed: {str(e)[:50]}...")
            return False

    def download_playlist(self, url, audio_format='mp3', quality='192'):
        """
        Download all tracks from a Spotify playlist

        Args:
            url (str): Spotify URL (track, album, or playlist)
            audio_format (str): Output audio format (default: 'mp3')
            quality (str): Audio quality in kbps (default: '192')

        Returns:
            dict: Download statistics {'total': int, 'successful': int, 'failed': int}
        """
        # Validate URL first
        if not self.validate_url(url):
            return {'total': 0, 'successful': 0, 'failed': 0}

        self.print_info("Fetching track list from Spotify...")
        tracks = self.get_tracks_from_url(url)

        if not tracks:
            self.print_error("No tracks found")
            return {'total': 0, 'successful': 0, 'failed': 0}

        self.print_success(f"Found {len(tracks)} track(s)")

        # Download statistics
        # Its a little complex but trust me
        # its easy to use if you see my code in main.py
        stats = {'total': len(tracks), 'successful': 0, 'failed': 0}

        for i, track in enumerate(tracks, 1):
            print(f"\n{Fore.MAGENTA}[{i}/{len(tracks)}]")
            if self.download_track(track, audio_format, quality):
                stats['successful'] += 1
            else:
                stats['failed'] += 1

        return stats

    def get_downloaded_files(self):
        """
        Get list of downloaded songs

        Returns:
            list: List of filenames in the downloaded directory
        """
        if os.path.exists(self.download_dir):
            return [f for f in os.listdir(self.download_dir)
                   if f.endswith(('.mp3', '.m4a', '.webm', '.opus'))]
        
        # Returns all forms of audio files in the downloaded dict
        return []

    @staticmethod
    def check_ffmpeg():
        """
        all this does is check if ffmpeg is installed
        ffmpeg is used for all the audio compression and handling stuff
        ffmpeg is ESSENTIAL, without it installed the program wont work

        Returns:
            bool: True if FFmpeg is available, False otherwise
        """
        try:
            import subprocess
            result = subprocess.run(['ffmpeg', '-version'],
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
