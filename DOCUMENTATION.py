# DOCUMENTATION!!!!!

# This is how you download a single song/track
# downloader.download_track("Artist Name - Song Title")
# That will start downloading the song and save it to downloaded dict

# This is how you download from a spotify link (works with track, album, or playlist)
# Single track:
# url = "https://open.spotify.com/track/..."
# stats = downloader.download_playlist(url)

# This is how you download all the songs from a playlist
# url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"
# stats = downloader.download_playlist(url)
# print(f"Downloaded: {stats['successful']}/{stats['total']} songs")
# print(f"Failed: {stats['failed']}")
# This basically fetches all the songs in the playlist, then downloads them 1 by 1

# Download an album
# url = "https://open.spotify.com/album/..."
# stats = downloader.download_playlist(url)
# Works the exact same way as playlist, but for albums

# This is how you get the list of downloaded songs
# files = downloader.get_downloaded_files()
# print(f"Downloaded files: {files}")
# This function basically just returns ALL sound files in the downloaded dict

# This allows you to fetch the songs in a playlist, without downloading it
# url = "https://open.spotify.com/playlist/..."
# tracks = downloader.get_tracks_from_url(url)
# print(f"Found {len(tracks)} tracks:")
# for track in tracks:
#     print(f"  - {track}")
# This lets you preview what will be downloaded before actually downloading
# Essentially, you can display whats in the playlist, before deciding to download