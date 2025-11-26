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

def spotify_cli():
    """CLI interface for Spotify downloader"""
    parser = argparse.ArgumentParser(
        description="Spotify Downloader CLI"  # Fixed: was 'descriptions'
    )
    parser.add_argument(
        "link",
        help="Spotify track, album or playlist"
    )
    args = parser.parse_args()  # Fixed: was missing ()
    link = args.link
    
    print("\n - - - Spotify Downloader CLI - - - ")  # Fixed typo: Donwloader -> Downloader
    print(f"Processing ->: {link}")
    print(" --------------------------------------")
    
    downloader = SpotifyDownloader(download_dir='downloaded')
    
    try:
        stats = downloader.download_playlist(link)
        print("\n" + "="*50)
        print(f"Download Complete!")
        print(f"Total tracks: {stats['total']}")
        print(f"Successfully downloaded: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print("="*50)
    except Exception as e:  # Fixed: 'exception' -> 'Exception' (capital E)
        print(f"\nSorry, an error has occurred: {e}")

def download_spotify(spotify_url):
    """Gradio function to download Spotify content"""
    if not spotify_url or not spotify_url.strip():
        return "❌ Please enter a valid Spotify URL"
    
    downloader = SpotifyDownloader(download_dir='downloaded')
    
    try:
        # The downloader function will handle everything:
        # Downloading the songs, validating if the URL is valid etc
        stats = downloader.download_playlist(spotify_url)

        # Print results to console
        print("\n" + "="*50)
        print(f"Download Complete!")
        print(f"Total tracks: {stats['total']}")
        print(f"Successfully downloaded: {stats['successful']}")
        print(f"Failed: {stats['failed']}")
        print("="*50)
        
        # Return formatted results to UI
        result = f"""
✅ Download Complete!

📊 Statistics:
• Total tracks: {stats['total']}
• Successfully downloaded: {stats['successful']}
• Failed: {stats['failed']}
• Success rate: {(stats['successful']/stats['total']*100) if stats['total'] > 0 else 0:.1f}%

📁 Files saved to: ./downloaded/

(See console for detailed logs)
"""
        return result
        
    except Exception as e:  # Fixed: 'exception' -> 'Exception'
        error_msg = f"❌ Error occurred: {str(e)}\n\nPlease check:\n• URL is valid\n• Internet connection is active\n• VPN is disabled (if applicable)"
        print(f"\n⚠️ ERROR: {e}")
        return error_msg

if __name__ == "__main__":
    # Use this to get input from user
    webpage_UI = gr.Interface(
        fn=download_spotify,
        inputs=gr.Textbox(
            label="Spotify URL",
            placeholder="https://open.spotify.com/playlist/...",
            lines=1
        ),
        outputs=gr.Textbox(
            label="Results",
            lines=10
        ),
        title="🎵 Spotify Downloader",
        description="Download Spotify playlists, albums, or tracks. Paste your Spotify URL below and click Submit.",
        api_name="download"  # Changed from "predict" to be more descriptive
    )

    # See gradio docs here: https://www.gradio.app/guides/quickstart
    webpage_UI.launch()  # Add share=True if you want to share the demo globally
