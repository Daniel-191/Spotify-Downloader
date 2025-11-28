"""
Super Simple Test GUI to verify layout works
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QTextCursor

# Import the Spotify downloader
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.spotify_lib import SpotifyDownloader


class ConsoleRedirector:
    """Redirect stdout to GUI console"""
    def __init__(self, signal):
        self.signal = signal

    def write(self, text):
        # Remove ANSI color codes
        import re
        text = re.sub(r'\x1b\[[0-9;]*m', '', text)
        if text.strip():
            self.signal.emit(text)

    def flush(self):
        pass


class DownloadWorker(QThread):
    """Worker thread to handle downloads without freezing the GUI"""
    progress_update = pyqtSignal(int)
    status_update = pyqtSignal(str)
    console_update = pyqtSignal(str)
    stats_update = pyqtSignal(dict)
    finished = pyqtSignal(dict)

    def __init__(self, url, audio_format, quality):
        super().__init__()
        self.url = url
        self.audio_format = audio_format.lower()
        self.quality = quality
        self.downloader = SpotifyDownloader()
        self.is_cancelled = False

    def stop(self):
        """Stop the download process"""
        self.is_cancelled = True

    def run(self):
        """Run the download process"""
        # Redirect stdout to GUI
        import sys
        old_stdout = sys.stdout
        sys.stdout = ConsoleRedirector(self.console_update)

        try:
            self.console_update.emit(f"Starting download...\n")
            self.status_update.emit("Downloading...")

            # Validate URL first
            if not self.downloader.validate_url(self.url):
                self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})
                return

            # Get playlist/album name for subfolder
            playlist_name = self.downloader.get_playlist_name(self.url)
            if playlist_name:
                self.console_update.emit(f"Playlist/Album: {playlist_name}\n")

            self.console_update.emit("Fetching track list...\n")
            tracks = self.downloader.get_tracks_from_url(self.url)

            if not tracks:
                self.console_update.emit("No tracks found\n")
                self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})
                return

            # Download statistics
            stats = {'total': len(tracks), 'successful': 0, 'failed': 0}
            self.stats_update.emit(stats)

            for i, track in enumerate(tracks, 1):
                if self.is_cancelled:
                    self.console_update.emit("\n⚠ Download cancelled by user\n")
                    self.status_update.emit("Cancelled")
                    break

                self.console_update.emit(f"\n[{i}/{len(tracks)}]\n")

                # Download track
                if self.downloader.download_track(track, self.audio_format, self.quality, subfolder=playlist_name):
                    stats['successful'] += 1
                else:
                    stats['failed'] += 1

                # Update progress and stats
                progress = int((i / len(tracks)) * 100)
                self.progress_update.emit(progress)
                self.stats_update.emit(stats)

            # Final update
            if not self.is_cancelled:
                self.progress_update.emit(100)
                self.status_update.emit("Complete!")

            self.finished.emit(stats)

        except Exception as e:
            self.console_update.emit(f"Error: {str(e)}\n")
            self.status_update.emit("Error occurred")
            self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})

        finally:
            # Restore stdout
            sys.stdout = old_stdout


class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Downloader")
        self.setFixedSize(650, 550)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 12, 15, 12)

        # Title
        title = QLabel("Spotify Downloader")
        title.setStyleSheet("font-size: 18px; color: #00ffcc; font-weight: bold; padding: 8px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # URL Section
        url_label = QLabel("Spotify URL:")
        url_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://open.spotify.com/playlist/...")
        self.url_input.setMinimumHeight(32)
        layout.addWidget(self.url_input)

        # Settings Section
        settings_label = QLabel("Settings:")
        settings_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(settings_label)

        settings_layout = QHBoxLayout()

        format_layout = QVBoxLayout()
        format_layout.setSpacing(4)
        format_lbl = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "AAC", "M4A", "Opus", "Vorbis", "FLAC", "WAV", "ALAC"])
        self.format_combo.setMinimumHeight(28)
        self.format_combo.setMaxVisibleItems(10)
        self.format_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 6px;
                padding: 5px;
                color: white;
            }
            QComboBox:hover {
                border: 2px solid #00d9ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 2px solid #00ffcc;
                selection-background-color: #00d9ff;
                color: white;
                padding: 5px;
            }
        """)
        format_layout.addWidget(format_lbl)
        format_layout.addWidget(self.format_combo)

        quality_layout = QVBoxLayout()
        quality_layout.setSpacing(4)
        quality_lbl = QLabel("Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["auto", "320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps"])
        self.quality_combo.setMinimumHeight(28)
        self.quality_combo.setMaxVisibleItems(10)
        self.quality_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 6px;
                padding: 5px;
                color: white;
            }
            QComboBox:hover {
                border: 2px solid #00d9ff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 2px solid #00ffcc;
                selection-background-color: #00d9ff;
                color: white;
                padding: 5px;
            }
        """)
        quality_layout.addWidget(quality_lbl)
        quality_layout.addWidget(self.quality_combo)

        settings_layout.addLayout(format_layout)
        settings_layout.addLayout(quality_layout)
        layout.addLayout(settings_layout)

        # Progress Section
        progress_label = QLabel("Progress:")
        progress_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(28)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444444;
                border-radius: 8px;
                text-align: center;
                background-color: #2d2d2d;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ffcc, stop:1 #00d9ff);
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.download_btn = QPushButton("Start Download")
        self.download_btn.setMinimumHeight(36)
        self.download_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.download_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d9ff, stop:1 #00a8cc);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00ffcc, stop:1 #00d9ff);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00a8cc, stop:1 #008899);
            }
            QPushButton:disabled {
                background: #444444;
                color: #888888;
            }
        """)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setMinimumHeight(36)
        self.stop_btn.setMaximumWidth(100)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b6b, stop:1 #cc5555);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff8888, stop:1 #ff6b6b);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #cc5555, stop:1 #aa4444);
            }
            QPushButton:disabled {
                background: #444444;
                color: #888888;
            }
        """)

        button_layout.addWidget(self.download_btn)
        button_layout.addWidget(self.stop_btn)
        layout.addLayout(button_layout)

        # Console
        console_label = QLabel("Console:")
        console_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(console_label)

        self.console = QTextEdit()
        self.console.setFixedHeight(100)
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        # Stats
        stats_label = QLabel("Statistics:")
        stats_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(stats_label)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        # Total
        self.total_label = QLabel("Total: 0")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px solid #00ffcc;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                color: white;
            }
        """)

        # Success
        self.success_label = QLabel("Success: 0")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px solid #00ff88;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                color: #00ff88;
            }
        """)

        # Failed
        self.failed_label = QLabel("Failed: 0")
        self.failed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.failed_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px solid #ff6b6b;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                font-weight: bold;
                color: #ff6b6b;
            }
        """)

        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.success_label)
        stats_layout.addWidget(self.failed_label)
        layout.addLayout(stats_layout)

        # Connect buttons
        self.download_btn.clicked.connect(self.start_download)
        self.stop_btn.clicked.connect(self.stop_download)

        # Worker thread
        self.worker = None

    def log_to_console(self, message):
        """Add message to console"""
        self.console.append(message.strip())
        # Auto-scroll to bottom
        self.console.moveCursor(QTextCursor.MoveOperation.End)

    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)

    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)

    def update_stats(self, stats):
        """Update statistics labels"""
        self.total_label.setText(f"Total: {stats['total']}")
        self.success_label.setText(f"Success: {stats['successful']}")
        self.failed_label.setText(f"Failed: {stats['failed']}")

    def download_finished(self, stats):
        """Called when download is complete"""
        self.update_stats(stats)
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Start Download")
        self.stop_btn.setEnabled(False)

        if stats['successful'] > 0:
            self.log_to_console(f"\n✓ Download complete! {stats['successful']}/{stats['total']} successful\n")
        else:
            self.log_to_console(f"\n✗ Download failed\n")

    def stop_download(self):
        """Stop the current download"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.log_to_console("\nStopping download...\n")
            self.stop_btn.setEnabled(False)

    def start_download(self):
        """Start the download process"""
        url = self.url_input.text().strip()

        if not url:
            self.log_to_console("Error: Please enter a Spotify URL\n")
            return

        if "spotify.com" not in url:
            self.log_to_console("Error: Invalid Spotify URL\n")
            return

        # Get settings
        audio_format = self.format_combo.currentText()
        quality = self.quality_combo.currentText().split()[0]  # Get just the number or 'auto'

        # Reset UI
        self.console.clear()
        self.progress_bar.setValue(0)
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading...")
        self.stop_btn.setEnabled(True)

        # Create and start worker thread
        self.worker = DownloadWorker(url, audio_format, quality)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.status_update.connect(self.update_status)
        self.worker.console_update.connect(self.log_to_console)
        self.worker.stats_update.connect(self.update_stats)
        self.worker.finished.connect(self.download_finished)
        self.worker.start()

def main():
    app = QApplication(sys.argv)

    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
