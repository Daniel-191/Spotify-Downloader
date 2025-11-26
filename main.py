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
> Build CLI/terminal version (Task for JayM2F)
> Add logic to handle Download fail errors (Task for Daniel-191)
> While on a VPN i got this error 'ERROR: [youtube] rvAGVO_A9ig: Sign in to confirm you’re not a bot.'
"""

import argparse
from spotify_lib import process_spotify_link

def spotify_cli():
    parser = argparse.ArgumentParser(
        descriptions = "Spotify Downloader CLI")
    parser.add_argument(
        "link",
        help="Spotify track, album or playlist"
    )
    args = parser.parse_args
    link = args.link
    
    print("\n - - - Spotify Donwloader CLI - - - ")
    print(f"processing ->: {link}")
    print(" --------------------------------------")

    try:
        process_spotify_link(link)
        print("\n Download is complete!")
    except exception as e:
        print(f"\n Sorry an error has occured: {e}")  

# Import the spotify class thing
from spotify_lib import SpotifyDownloader

import gradio as gr

def greet(spotify_url, intensity):
    # The downloader function will handle everything:
    # Downloading the songs, validiating if the URl is valid Etc
    stats = downloader.download_playlist(spotify_url)

    # Print results
    print("\n" + "="*50)
    print(f"Download Complete!")
    print(f"Total tracks: {stats['total']}")
    print(f"Successfully downloaded: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print("="*50)
    return f"Downloading {spotify_url} !! (see console for logs)"

if __name__ == "__main__":
    downloader = SpotifyDownloader(download_dir='downloaded')

    # Use this to get input from user
    webpage_UI = gr.Interface(
        fn=greet,
        inputs=["text"],
        outputs=["text"],
        api_name="predict"
    )

    # see gradio docs here: https://www.gradio.app/guides/quickstart

    webpage_UI.launch() # add share=True if u want to share the demo globally
