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
> While on a VPN i got this error 'ERROR: [youtube] rvAGVO_A9ig: Sign in to confirm you're not a bot.'
"""

import argparse
from spotify_lib import SpotifyDownloader
import gradio as gr


# --------------------------------------------------------
# CSS TO MAKE WEBSITE LOOK NICE, IMPORTANTS TO TRY AND OVERIDE GRADIO
# --------------------------------------------------------

custom_css = """
/* --- GLOBAL PAGE STYLING --- */
body {
    background: #fffff !important;
}

/* --- MAIN APP BACKGROUND --- */
.gradio-container {
    background: #fffff !important;
    color: #EEE;
    font-family: 'Segoe UI', sans-serif;
}

/* --- TITLE STYLING --- */
h1 {
    text-align: center;
    font-size: 2.2rem !important;
    color: #00ffcc !important;
    margin-bottom: 10px !important;
}

/* --- DESCRIPTION TEXT --- */
h2, p {
    text-align: center;
    color: #bbb !important;
}

/* --- INPUT TEXTBOX --- */
.gr-text-input textarea {
    background: #222 !important;
    color: #0ff !important;
    border: 1px solid #444 !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

/* --- OUTPUT BOX --- */
.gr-textbox textarea {
    background: #181818 !important;
    color: #c0ffc0 !important;
    border: 1px solid #333 !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 15px !important;
}

/* --- SUBMIT BUTTON --- */
button {
    background: linear-gradient(135deg, #00ffa6, #008cff) !important;
    color: #000 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    border: none !important;
    transition: 0.2s ease-in-out !important;
}

button:hover {
    transform: scale(1.04) !important;
    opacity: 0.9 !important;
}

/* --- CARD / CONTAINER LOOK FOR BLOCKS --- */
.gr-block {
    border-radius: 16px !important;
}
"""
# --------------------------------------------------------



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

    downloader = SpotifyDownloader(download_dir='downloaded')

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
    """Gradio function to download Spotify content"""
    if not spotify_url or not spotify_url.strip():
        return "❌ Please enter a valid Spotify URL"

    downloader = SpotifyDownloader(download_dir='downloaded')

    try:
        stats = downloader.download_playlist(spotify_url)

        result = f"""
✅ Download Complete!

📊 **Statistics**
• Total tracks: {stats['total']}
• Successful: {stats['successful']}
• Failed: {stats['failed']}
• Success rate: {(stats['successful']/stats['total']*100) if stats['total'] > 0 else 0:.1f}%

📁 Saved to: `./downloaded/`

🔎 See the console for detailed logs.
"""

        return result

    except Exception as e:
        return f"""
❌ Error Occurred: {str(e)}

Please check:
• URL is correct  
• Internet connection  
• Disable VPN if using one
"""

if __name__ == "__main__":
    with gr.Blocks(title="Spotify Downloader") as webpage_UI:

        gr.HTML(f"<style>{custom_css}</style>")

        gr.Markdown("# 🎵 Spotify Downloader")
        gr.Markdown("Download Spotify playlists, albums, or tracks.")

        spotify_input = gr.Textbox(
            label="Spotify URL",
            placeholder="https://open.spotify.com/playlist/...",
            lines=1,
        )

        result_box = gr.Textbox(
            label="Results",
            lines=12,
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

