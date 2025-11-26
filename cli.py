"""
CLI Interface for Spotify Downloader
"""

import argparse
from lib import SpotifyDownloader


def run_cli():
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


if __name__ == "__main__":
    run_cli()
