"""
Modern PyQt6 GUI for Spotify Downloader

Python Version: 3.13.7
Collaborators: Daniel-191, ShellDrak3, JayM2F
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox,
    QProgressBar, QFrame, QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPalette, QColor, QTextCursor, QIcon
from lib import SpotifyDownloader


class DownloadWorker(QThread):
    """Worker thread for downloading tracks"""
    progress = pyqtSignal(str, str)  # message, status
    track_progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal(dict)  # stats

    def __init__(self, url, audio_format='mp3', quality='auto'):
        super().__init__()
        self.url = url
        self.audio_format = audio_format
        self.quality = quality
        self.downloader = SpotifyDownloader(download_dir='downloaded')

    def run(self):
        """Run the download process"""
        try:
            # Validate URL
            self.progress.emit("Validating URL...", "info")
            if not self.downloader.validate_url(self.url):
                self.progress.emit("Invalid Spotify URL", "error")
                self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})
                return

            # Get tracks
            self.progress.emit("Fetching track list from Spotify...", "info")
            tracks = self.downloader.get_tracks_from_url(self.url)

            if not tracks:
                self.progress.emit("No tracks found", "error")
                self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})
                return

            self.progress.emit(f"Found {len(tracks)} track(s)", "success")

            # Download tracks
            stats = {'total': len(tracks), 'successful': 0, 'failed': 0}

            for i, track in enumerate(tracks, 1):
                self.track_progress.emit(i, len(tracks))
                self.progress.emit(f"[{i}/{len(tracks)}] Downloading: {track}", "info")

                if self.downloader.download_track(track, self.audio_format, self.quality):
                    stats['successful'] += 1
                    self.progress.emit(f"✓ Completed: {track}", "success")
                else:
                    stats['failed'] += 1
                    self.progress.emit(f"✗ Failed: {track}", "error")

            self.finished.emit(stats)

        except Exception as e:
            self.progress.emit(f"Error: {str(e)}", "error")
            self.finished.emit({'total': 0, 'successful': 0, 'failed': 0})


class ModernButton(QPushButton):
    """Custom styled button with hover effects"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #00d9ff, stop:1 #00a8cc);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
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


class SpotifyDownloaderGUI(QMainWindow):
    """Main GUI window for Spotify Downloader"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🎵 Spotify Downloader")
        self.setMinimumSize(900, 700)

        # Set dark theme
        self.set_dark_theme()

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # URL Input Section
        url_section = self.create_url_section()
        main_layout.addWidget(url_section)

        # Settings Section
        settings_section = self.create_settings_section()
        main_layout.addWidget(settings_section)

        # Progress Section
        progress_section = self.create_progress_section()
        main_layout.addWidget(progress_section)

        # Output Console
        console_section = self.create_console_section()
        main_layout.addWidget(console_section)

        # Stats Section
        stats_section = self.create_stats_section()
        main_layout.addWidget(stats_section)

        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)

    def set_dark_theme(self):
        """Set dark theme for the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 26))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 217, 255))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

        self.setPalette(palette)

        # Application-wide stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1a1a1a, stop:1 #0d0d0d);
            }
            QGroupBox {
                border: 2px solid #00ffcc;
                border-radius: 10px;
                margin-top: 10px;
                padding: 15px;
                font-weight: bold;
                color: #00ffcc;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 6px;
                padding: 10px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #00ffcc;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #444444;
                border-radius: 6px;
                padding: 8px;
                color: white;
                font-size: 13px;
                min-height: 25px;
            }
            QComboBox:hover {
                border: 2px solid #00d9ff;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #00ffcc;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 2px solid #00ffcc;
                selection-background-color: #00d9ff;
                color: white;
            }
            QTextEdit {
                background-color: #1a1a1a;
                border: 2px solid #00ffcc;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            QProgressBar {
                border: 2px solid #444444;
                border-radius: 8px;
                text-align: center;
                background-color: #2d2d2d;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ffcc, stop:1 #00d9ff);
                border-radius: 6px;
            }
            QLabel {
                color: white;
            }
        """)

    def create_header(self):
        """Create header section"""
        header = QLabel("🎵 Spotify Downloader")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #00ffcc;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(0, 255, 204, 0.1), stop:0.5 rgba(0, 217, 255, 0.1), stop:1 rgba(0, 255, 204, 0.1));
            border-radius: 10px;
        """)
        return header

    def create_url_section(self):
        """Create URL input section"""
        group = QGroupBox("Spotify URL")
        layout = QVBoxLayout()

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://open.spotify.com/playlist/...")
        layout.addWidget(self.url_input)

        # Description
        desc = QLabel("Enter a Spotify track, album, or playlist URL")
        desc.setStyleSheet("color: #888888; font-size: 11px; padding: 5px;")
        layout.addWidget(desc)

        group.setLayout(layout)
        return group

    def create_settings_section(self):
        """Create settings section"""
        group = QGroupBox("⚙️ Download Settings")
        layout = QHBoxLayout()

        # Audio format
        format_layout = QVBoxLayout()
        format_label = QLabel("Audio Format:")
        format_label.setStyleSheet("color: #00d9ff; font-weight: bold;")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "AAC", "M4A", "Opus", "Vorbis", "FLAC", "WAV", "ALAC"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)

        # Quality
        quality_layout = QVBoxLayout()
        quality_label = QLabel("Quality:")
        quality_label.setStyleSheet("color: #00d9ff; font-weight: bold;")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["auto", "320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps"])
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.quality_combo)

        layout.addLayout(format_layout)
        layout.addLayout(quality_layout)

        group.setLayout(layout)
        return group

    def create_progress_section(self):
        """Create progress bar section"""
        group = QGroupBox("📊 Download Progress")
        layout = QVBoxLayout()

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # Current track label
        self.current_track_label = QLabel("Ready to download")
        self.current_track_label.setStyleSheet("color: #00d9ff; padding: 5px;")
        self.current_track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_track_label)

        # Download button
        self.download_btn = ModernButton("Start Download")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        group.setLayout(layout)
        return group

    def create_console_section(self):
        """Create console output section"""
        group = QGroupBox("📝 Console Output")
        layout = QVBoxLayout()

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMinimumHeight(200)
        layout.addWidget(self.console)

        group.setLayout(layout)
        return group

    def create_stats_section(self):
        """Create statistics section"""
        group = QGroupBox("📈 Statistics")
        layout = QHBoxLayout()

        # Total
        self.total_label = QLabel("Total: 0")
        self.total_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")

        # Successful
        self.success_label = QLabel("Successful: 0")
        self.success_label.setStyleSheet("color: #00ff88; font-size: 14px; font-weight: bold;")

        # Failed
        self.failed_label = QLabel("Failed: 0")
        self.failed_label.setStyleSheet("color: #ff6b6b; font-size: 14px; font-weight: bold;")

        layout.addWidget(self.total_label)
        layout.addStretch()
        layout.addWidget(self.success_label)
        layout.addStretch()
        layout.addWidget(self.failed_label)

        group.setLayout(layout)
        return group

    def create_footer(self):
        """Create footer section"""
        footer = QLabel(
            "Made with ❤️ by "
            '<a href="https://github.com/Daniel-191" style="color:#00ffcc; text-decoration:none;">Daniel-191</a>, '
            '<a href="https://github.com/ShellDrak3" style="color:#00ffcc; text-decoration:none;">ShellDrak3</a>, '
            '<a href="https://github.com/JayM2F" style="color:#00ffcc; text-decoration:none;">JayM2F</a>'
        )
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #888888; font-size: 12px; padding: 10px;")
        footer.setOpenExternalLinks(True)
        return footer

    def log_message(self, message, status="info"):
        """Log message to console with color coding"""
        color_map = {
            "info": "#00d9ff",
            "success": "#00ff88",
            "error": "#ff6b6b",
            "warning": "#ffaa00"
        }

        color = color_map.get(status, "#ffffff")
        timestamp = QTimer()

        html = f'<span style="color: {color};">{message}</span>'
        self.console.append(html)

        # Auto-scroll to bottom
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console.setTextCursor(cursor)

    def start_download(self):
        """Start the download process"""
        url = self.url_input.text().strip()

        if not url:
            self.log_message("⚠ Please enter a Spotify URL", "warning")
            return

        # Get settings
        audio_format = self.format_combo.currentText().lower()
        quality = self.quality_combo.currentText().split()[0]  # Extract number or 'auto'

        # Disable button
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading...")

        # Clear console
        self.console.clear()

        # Reset stats
        self.total_label.setText("Total: 0")
        self.success_label.setText("Successful: 0")
        self.failed_label.setText("Failed: 0")
        self.progress_bar.setValue(0)

        # Create and start worker thread
        self.worker = DownloadWorker(url, audio_format, quality)
        self.worker.progress.connect(self.log_message)
        self.worker.track_progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.start()

    def update_progress(self, current, total):
        """Update progress bar"""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.current_track_label.setText(f"Downloading track {current} of {total}")

    def download_finished(self, stats):
        """Handle download completion"""
        # Update stats
        self.total_label.setText(f"Total: {stats['total']}")
        self.success_label.setText(f"Successful: {stats['successful']}")
        self.failed_label.setText(f"Failed: {stats['failed']}")

        # Re-enable button
        self.download_btn.setEnabled(True)
        self.download_btn.setText("Start Download")

        # Show completion message
        if stats['total'] > 0:
            success_rate = (stats['successful'] / stats['total']) * 100
            self.log_message(
                f"\n✅ Download Complete! Success rate: {success_rate:.1f}%",
                "success"
            )
            self.log_message(f"📁 Files saved to: ./downloaded/", "info")
            self.current_track_label.setText("Download complete!")
            self.progress_bar.setValue(100)
        else:
            self.current_track_label.setText("Ready to download")
            self.log_message("No tracks were downloaded", "error")


def main():
    """Main entry point for the GUI application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Spotify Downloader")

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show main window
    window = SpotifyDownloaderGUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
