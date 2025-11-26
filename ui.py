"""
Gradio Web UI for Spotify Downloader
"""

import os
import time
from lib import SpotifyDownloader
import gradio as gr


def load_css(file_path='assets/styles.css'):
    """Load CSS from external file"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def download_spotify(spotify_url):
    """Gradio function to download Spotify content with live progress"""

    # Box wrapper style
    box_wrapper = "<div style='background: #1a1a1a; border: 2px solid #00ffcc; border-radius: 12px; padding: 20px; font-family: monospace; font-size: 14px; line-height: 1.8; min-height: 400px; color: #ffffff; box-shadow: 0 4px 6px rgba(0, 255, 204, 0.1);'>"
    box_close = "</div>"

    if not spotify_url or not spotify_url.strip():
        yield f"{box_wrapper}<span style='color: #ff6b6b; font-weight: bold;'> Please enter a valid Spotify URL</span>{box_close}"
        return

    downloader = SpotifyDownloader(download_dir='downloaded')

    try:
        # Show fetching message
        output = "<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br>"
        print(f"DEBUG: Yielding initial message")  # Debug
        yield f"{box_wrapper}{output}{box_close}"
        time.sleep(0.1)  # Small delay for UI update

        # Validate and get tracks
        if not downloader.validate_url(spotify_url):
            output += "<span style='color: #ff6b6b; font-weight: bold;'>✗ Invalid Spotify URL</span><br>"
            yield f"{box_wrapper}{output}{box_close}"
            return

        tracks = downloader.get_tracks_from_url(spotify_url)

        if not tracks:
            output += "<span style='color: #ff6b6b; font-weight: bold;'>✗ No tracks found</span><br>"
            yield f"{box_wrapper}{output}{box_close}"
            return

        output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"

        # Initialize track list
        track_lines = []
        for i, track in enumerate(tracks, 1):
            track_lines.append(f"<span style='color: #888888;'>{i}. {track} - Waiting...</span>")

        output += "<br>".join(track_lines) + "<br>"
        yield f"{box_wrapper}{output}{box_close}"
        time.sleep(0.1)

        # Download each track
        successful = 0
        failed = 0

        for i, track in enumerate(tracks, 1):
            # Animate progress from 0% to 95%
            progress_steps = [0, 15, 35, 50, 65, 80, 95]

            for progress in progress_steps:
                track_lines[i-1] = f"<span style='color: #00d9ff;'>{i}. {track} - Downloading - {progress}%</span>"
                output = f"<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br>"
                output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"
                output += "<br>".join(track_lines) + "<br>"
                yield f"{box_wrapper}{output}{box_close}"
                time.sleep(0.15)  # Quick animation

            # Attempt download
            success = downloader.download_track(track, audio_format='mp3', quality='auto')

            # Update track to final status
            if success:
                track_lines[i-1] = f"<span style='color: #00ff88; font-weight: bold;'>{i}. {track} - Downloaded - 100%</span>"
                successful += 1
            else:
                track_lines[i-1] = f"<span style='color: #ff6b6b; font-weight: bold;'>{i}. {track} - Failed</span>"
                failed += 1

            output = f"<span style='color: #00d9ff; font-weight: bold;'>• Fetching track list from Spotify...</span><br>"
            output += f"<span style='color: #00ff88; font-weight: bold;'>✓ Found {len(tracks)} track(s)</span><br><br>"
            output += "<br>".join(track_lines) + "<br>"
            yield f"{box_wrapper}{output}{box_close}"
            time.sleep(0.1)

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

        yield f"{box_wrapper}{output}{box_close}"

    except Exception as e:
        output = f"<span style='color: #ff6b6b; font-weight: bold;'>Error Occurred: {str(e)}</span><br><br>"
        output += "<span style='color: #ffffff;'>Please check:</span><br>"
        output += "<span style='color: #ffffff;'>• URL is correct</span><br>"
        output += "<span style='color: #ffffff;'>• Internet connection</span><br>"
        output += "<span style='color: #ffffff;'>• Chrome browser is closed (needed for cookie extraction)</span>"
        yield f"{box_wrapper}{output}{box_close}"


def create_ui():
    """Create and return the Gradio interface"""
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
            elem_classes="result-output"
        )

        submit_btn = gr.Button("Start Download")

        submit_btn.click(
            fn=download_spotify,
            inputs=spotify_input,
            outputs=result_box,
            show_progress=True
        )

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

    return webpage_UI


if __name__ == "__main__":
    ui = create_ui()
    ui.launch()
