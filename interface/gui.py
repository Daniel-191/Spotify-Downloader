"""
Super Simple Test GUI to verify layout works
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SimpleGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Test GUI")
        self.setMinimumSize(700, 550)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        # Main layout
        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Title
        title = QLabel("🎵 Spotify Downloader")
        title.setStyleSheet("font-size: 20px; color: #00ffcc; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # URL Section
        url_label = QLabel("Spotify URL:")
        url_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://open.spotify.com/playlist/...")
        self.url_input.setMinimumHeight(35)
        layout.addWidget(self.url_input)

        # Settings Section
        settings_label = QLabel("Settings:")
        settings_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(settings_label)

        settings_layout = QHBoxLayout()

        format_layout = QVBoxLayout()
        format_layout.setSpacing(5)
        format_lbl = QLabel("Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "AAC", "M4A", "Opus", "Vorbis", "FLAC", "WAV", "ALAC"])
        self.format_combo.setMinimumHeight(30)
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
        quality_layout.setSpacing(5)
        quality_lbl = QLabel("Quality:")
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["auto", "320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps"])
        self.quality_combo.setMinimumHeight(30)
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
        self.progress_bar.setMinimumHeight(30)
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

        self.download_btn = QPushButton("Start Download")
        self.download_btn.setMinimumHeight(40)
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
        layout.addWidget(self.download_btn)

        # Console
        console_label = QLabel("Console:")
        console_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffcc;")
        layout.addWidget(console_label)

        self.console = QTextEdit()
        self.console.setFixedHeight(120)
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

def main():
    app = QApplication(sys.argv)
    window = SimpleGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
