"""
Python Version: 3.13.7
Collaborators: Daniel-191, ShellDrak3, JayM2F
Project Start Date: 23/11/25
Project End Date: xx/xx/xx
"""

# PLEASE SEE DOCUMENTATION.py FOR DOCS

"""
---TODO---
> Build UI interface (tkinter or some sort of webpage)
> I suggest using gradio for the web interface, gradio is easy af, tons of tutorials on youtube, and you can easily make it look good
> Integrate with spotify_lib.py
"""

# Import the spotify class thing
from spotify_lib import SpotifyDownloader

if __name__ == "__main__":
    downloader = SpotifyDownloader(download_dir='downloaded')

    # write your code here!! (OOP)

    # Take a look at this simple code here for downloading a track, album or playlist
    # Its just something to give you guys and idea on how to use the library

    print("Enter a Spotify URL (track, album, or playlist)\n")

    url = input("[Spotify URL]: ").strip()

    print("\nStarting download...\n")
    # The downloader function will handle everything:
    # Downloading the songs, validiating if the URl is valid Etc
    stats = downloader.download_playlist(url)

    # Print results
    print("\n" + "="*50)
    print(f"Download Complete!")
    print(f"Total tracks: {stats['total']}")
    print(f"Successfully downloaded: {stats['successful']}")
    print(f"Failed: {stats['failed']}")
    print("="*50)
