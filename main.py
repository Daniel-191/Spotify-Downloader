"""
Python Version: 3.13.7
Collaborators: Daniel-191, ShellDrak3, JayM2F
Project Start Date: 23/11/25
Project End Date: xx/xx/xx
"""

# PLEASE SEE DOCUMENTATION.py FOR DOCS

"""
---TODO---
> Build GUI Interface (task for ShellDrak3 or JayM2F)
> Add logic to handle Download fail errors (Task for Daniel-191)
"""

import argparse
import os
from spotify_lib import SpotifyDownloader
import gradio as gr


def load_css(file_path='styles.css'):
    """Load CSS from external file"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def spotify_cli():
    """CLI interface for Spotify downloader"""
    parser = argparse.ArgumentParser(
        description="Spotify Downloader CLI"
    )
    parser.add_argument(
        "link",
        help="Spotify track, album or playlist"
    )
    args = parser.parse_args()
    link = args.link

    print("\n - - - Spotify Downloader CLI - - - ")
    print(f"Processing ->: {link}")
    print(" --------------------------------------")

    downloader = SpotifyDownloader(
        download_dir='downloaded',
        cookie_browser='chrome',
        download_delay=3
    )

    try:
        stats = downloader.download_playlist(link)
        print("\n" + "=" * 50)
        print(f"Download Complete!")
        print(f"Total tracks: {stats['total']}")
        print(f"Successfully downloaded: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print("=" * 50)
    except Exception as e:
        print(f"\nSorry, an error has occurred: {e}")


def download_spotify(spotify_url):
    """Gradio function to download Spotify content with live progress"""
    if not spotify_url or not spotify_url.strip():
        yield "<span style='color: #ff6b6b; font-weight: bold;'>❌ Please enter a valid Spotify URL</span>"
        return

    downloader = SpotifyDownloader(download_dir='downloaded')

    try:
        # Show fetching message
        output = "<div style='font-family: monospace;'>"
        output += "<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br><br>"
        yield output + "</div>"

        # Validate and get tracks
        if not downloader.validate_url(spotify_url):
            output += "<span style='color: #ff6b6b; font-weight: bold;'>✗ Invalid Spotify URL</span><br>"
            yield output + "</div>"
            return

        tracks = downloader.get_tracks_from_url(spotify_url)

        if not tracks:
            output += "<span style='color: #ff6b6b; font-weight: bold;'>✗ No tracks found</span><br>"
            yield output + "</div>"
            return

        output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"

        # Initialize track list
        track_lines = []
        for i, track in enumerate(tracks, 1):
            track_lines.append(f"<span id='track-{i}'><span style='color: #888888;'>{i}. {track} - Waiting...</span></span>")

        output += "<br>".join(track_lines) + "<br>"
        yield output + "</div>"

        # Download each track
        successful = 0
        failed = 0

        for i, track in enumerate(tracks, 1):
            # Update current track to "Downloading"
            track_lines[i-1] = f"<span style='color: #00d9ff;'>{i}. {track} - Downloading - 0%</span>"
            output = "<div style='font-family: monospace;'>"
            output += f"<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br>"
            output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"
            output += "<br>".join(track_lines) + "<br>"
            yield output + "</div>"

            # Attempt download
            success = downloader.download_track(track, audio_format='mp3', quality='auto')

            # Update track to final status
            if success:
                track_lines[i-1] = f"<span style='color: #00ff88; font-weight: bold;'>{i}. {track} - Downloaded - 100%</span>"
                successful += 1
            else:
                track_lines[i-1] = f"<span style='color: #ff6b6b; font-weight: bold;'>{i}. {track} - Failed</span>"
                failed += 1

            output = "<div style='font-family: monospace;'>"
            output += f"<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br><br>"
            output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"
            output += "<br>".join(track_lines) + "<br>"
            yield output + "</div>"

        # Final summary
        total = len(tracks)
        success_rate = (successful/total*100) if total > 0 else 0

        output += "<br><br><span style='color: #00ff88; font-size: 16px; font-weight: bold;'>✅ Download Complete!</span><br><br>"
        output += "<span style='color: #00d9ff; font-weight: bold;'>📊 Statistics</span><br>"
        output += f"<span style='color: #ffffff;'>• Total: {total}</span> | "
        output += f"<span style='color: #00ff88;'>Successful: {successful}</span> | "
        output += f"<span style='color: #ff6b6b;'>Failed: {failed}</span> | "
        output += f"<span style='color: #ffaa00;'>Success rate: {success_rate:.1f}%</span><br>"
        output += f"<span style='color: #888888;'>📁 Saved to: ./downloaded/</span>"

        yield output + "</div>"

    except Exception as e:
        output = "<div style='font-family: monospace;'>"
        output += f"<span style='color: #ff6b6b; font-weight: bold;'>❌ Error Occurred: {str(e)}</span><br><br>"
        output += "<span style='color: #ffffff;'>Please check:</span><br>"
        output += "<span style='color: #ffffff;'>• URL is correct</span><br>"
        output += "<span style='color: #ffffff;'>• Internet connection</span><br>"
        output += "<span style='color: #ffffff;'>• Chrome browser is closed (needed for cookie extraction)</span>"
        yield output + "</div>"

if __name__ == "__main__":
    with gr.Blocks(title="Spotify Downloader") as webpage_UI:

        gr.HTML(f"<style>{load_css()}</style>")

        gr.Markdown("# 🎵 Spotify Downloader")
        gr.Markdown("Download Spotify playlists, albums, or tracks.")

        spotify_input = gr.Textbox(
            label="Spotify URL",
            placeholder="https://open.spotify.com/playlist/...",
            lines=1,
        )

        result_box = gr.HTML(
            label="Results",
            value="<span style='color: #888888;'>Enter a Spotify URL and click Start Download...</span>"
        )

        submit_btn = gr.Button("Start Download")

        submit_btn.click(fn=download_spotify, inputs=spotify_input, outputs=result_box)

        gr.Markdown(
            """
            <p style="text-align: center; font-size: 15px; color: #bbb;">
            Made with ❤️ by 
            <a href="https://github.com/Daniel-191" style="color:#00ffcc; text-decoration:none;">Daniel-191</a>, 
            <a href="https://github.com/ShellDrak3" style="color:#00ffcc; text-decoration:none;">ShellDrak3</a>, 
            <a href="https://github.com/JayM2F" style="color:#00ffcc; text-decoration:none;">JayM2F</a>
            </p>
            """,
        elem_id="credits"
        )


    webpage_UI.launch()

