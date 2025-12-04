"""
Spotify Downloader - Main Entry Point

Python Version: 3.13.7
Collaborators: Daniel-191, ShellDrak3, JayM2F
"""

from interface.ui import create_ui


if __name__ == "__main__":
    # Launch the Gradio web interface
    webpage_UI = create_ui()
    webpage_UI.launch()
