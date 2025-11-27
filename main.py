"""
Spotify Downloader - Main Entry Point

Python Version: 3.13.7
Collaborators: Daniel-191, ShellDrak3, JayM2F
Project Start Date: 23/11/25
Project End Date: xx/xx/xx

PLEASE SEE DOCUMENTATION.py FOR DOCS
"""

from interface.ui import create_ui


if __name__ == "__main__":
    # Launch the Gradio web interface
    webpage_UI = create_ui()
    webpage_UI.launch()
