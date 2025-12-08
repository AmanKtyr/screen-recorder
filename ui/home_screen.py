#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Home Screen Module
-----------------
The main screen of the application with the "Screen Recorder" button.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QComboBox, QGroupBox, QRadioButton,
    QButtonGroup, QSpacerItem, QSizePolicy, QFrame,
    QCheckBox, QToolButton, QTabWidget, QApplication,
    QStyle
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor, QPalette

class HomeScreen(QWidget):
    """Home screen widget with the screen recorder button."""

    # Signal emitted when the user starts recording
    start_recording_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Header layout
        header_layout = QHBoxLayout()

        # Logo (if available)
        # Try multiple paths to find the logo
        possible_logo_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "logo.png"),
            os.path.join(os.getcwd(), "static", "logo.png"),
            "static/logo.png"
        ]

        logo_found = False
        for logo_path in possible_logo_paths:
            if os.path.exists(logo_path):
                try:
                    logo_label = QLabel()
                    logo_pixmap = QPixmap(logo_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    if not logo_pixmap.isNull():
                        logo_label.setPixmap(logo_pixmap)
                        header_layout.addWidget(logo_label)
                        logo_found = True
                        print(f"Logo loaded from: {logo_path}")
                        break
                except Exception as e:
                    print(f"Error loading logo from {logo_path}: {e}")

        if not logo_found:
            # Create a fallback label if logo is not found
            print("Using fallback logo")
            logo_label = QLabel("SR")
            logo_label.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px; padding: 10px;")
            logo_label.setFixedSize(64, 64)
            logo_label.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            logo_label.setFont(font)
            header_layout.addWidget(logo_label)

        # Title and description in vertical layout
        title_layout = QVBoxLayout()

        # Title
        title_label = QLabel("Professional Screen Recorder")
        title_label.setAlignment(Qt.AlignLeft)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)

        # Description
        desc_label = QLabel(
            "Record your screen with audio from your microphone, system, or both."
        )
        desc_label.setAlignment(Qt.AlignLeft)
        desc_font = QFont()
        desc_font.setPointSize(12)
        desc_label.setFont(desc_font)
        title_layout.addWidget(desc_label)

        # Add title layout to header
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        # Add theme toggle button
        self.theme_button = QToolButton()

        # Try multiple paths to find the theme icon
        possible_theme_paths = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "theme_icon.png"),
            os.path.join(os.getcwd(), "static", "theme_icon.png"),
            "static/theme_icon.png"
        ]

        theme_icon_found = False
        for theme_path in possible_theme_paths:
            if os.path.exists(theme_path):
                try:
                    icon = QIcon(theme_path)
                    if not icon.isNull():
                        self.theme_button.setIcon(icon)
                        theme_icon_found = True
                        print(f"Theme icon loaded from: {theme_path}")
                        break
                except Exception as e:
                    print(f"Error loading theme icon from {theme_path}: {e}")

        if not theme_icon_found:
            # Set a default icon from system if theme icon is not found
            print("Using fallback theme icon")
            self.theme_button.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))

        self.theme_button.setIconSize(QSize(24, 24))
        self.theme_button.setToolTip("Toggle Dark/Light Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)

        # Add header to main layout
        main_layout.addLayout(header_layout)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)

        # Create tabs for different settings
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 10px;
                background-color: #f8f8f8;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #f8f8f8;
                border-bottom: 1px solid #f8f8f8;
            }
            QTabBar::tab:hover {
                background-color: #eeeeee;
            }
        """)

        # Audio tab
        audio_tab = QWidget()
        audio_layout = QVBoxLayout(audio_tab)

        # Audio source selection
        audio_group = QGroupBox("Audio Source")
        audio_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #2196F3;
            }
        """)
        audio_source_layout = QVBoxLayout()

        # Radio buttons for audio source
        radio_button_style = """
            QRadioButton {
                spacing: 8px;
                padding: 4px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QRadioButton::indicator:checked {
                background-color: #2196F3;
                border: 2px solid #2196F3;
                border-radius: 8px;
            }
            QRadioButton::indicator:unchecked {
                border: 2px solid #999999;
                border-radius: 8px;
            }
        """

        self.mic_radio = QRadioButton("Microphone")
        self.mic_radio.setStyleSheet(radio_button_style)

        self.system_radio = QRadioButton("System Sound")
        self.system_radio.setStyleSheet(radio_button_style)

        self.both_radio = QRadioButton("Both Microphone and System Sound")
        self.both_radio.setStyleSheet(radio_button_style)

        self.none_radio = QRadioButton("No Audio")
        self.none_radio.setStyleSheet(radio_button_style)

        # Set microphone as default
        self.mic_radio.setChecked(True)

        # Add radio buttons to layout
        audio_source_layout.addWidget(self.mic_radio)
        audio_source_layout.addWidget(self.system_radio)
        audio_source_layout.addWidget(self.both_radio)
        audio_source_layout.addWidget(self.none_radio)

        # Set layout for audio group
        audio_group.setLayout(audio_source_layout)

        # Add audio group to audio tab layout
        audio_layout.addWidget(audio_group)
        audio_layout.addStretch()

        # Video tab
        video_tab = QWidget()
        video_layout = QVBoxLayout(video_tab)

        # Video quality selection
        quality_group = QGroupBox("Video Quality")
        quality_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #2196F3;
            }
        """)
        quality_layout = QVBoxLayout()

        # Radio buttons for video quality
        self.high_radio = QRadioButton("High Quality (1080p)")
        self.medium_radio = QRadioButton("Medium Quality (720p)")
        self.low_radio = QRadioButton("Low Quality (480p)")

        # Set high quality as default
        self.high_radio.setChecked(True)

        # Add radio buttons to layout
        quality_layout.addWidget(self.high_radio)
        quality_layout.addWidget(self.medium_radio)
        quality_layout.addWidget(self.low_radio)

        # Set layout for quality group
        quality_group.setLayout(quality_layout)

        # Add quality group to video tab layout
        video_layout.addWidget(quality_group)

        # Frame rate selection
        fps_group = QGroupBox("Frame Rate")
        fps_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #2196F3;
            }
        """)
        fps_layout = QVBoxLayout()

        # Radio buttons for frame rate
        self.fps_60_radio = QRadioButton("60 FPS (Smoother, larger file)")
        self.fps_30_radio = QRadioButton("30 FPS (Recommended)")
        self.fps_15_radio = QRadioButton("15 FPS (Smaller file size)")

        # Set 30 FPS as default
        self.fps_30_radio.setChecked(True)

        # Add radio buttons to layout
        fps_layout.addWidget(self.fps_60_radio)
        fps_layout.addWidget(self.fps_30_radio)
        fps_layout.addWidget(self.fps_15_radio)

        # Set layout for fps group
        fps_group.setLayout(fps_layout)

        # Add fps group to video tab layout
        video_layout.addWidget(fps_group)
        video_layout.addStretch()

        # Options tab
        options_tab = QWidget()
        options_layout = QVBoxLayout(options_tab)

        # Recording options
        options_group = QGroupBox("Recording Options")
        options_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                color: #2196F3;
            }
        """)
        options_inner_layout = QVBoxLayout()

        # Checkboxes for options
        checkbox_style = """
            QCheckBox {
                spacing: 8px;
                padding: 4px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background-color: #2196F3;
                border: 2px solid #2196F3;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #999999;
            }
        """

        self.show_cursor_check = QCheckBox("Show Cursor")
        self.show_cursor_check.setStyleSheet(checkbox_style)
        self.show_cursor_check.setChecked(True)

        self.countdown_check = QCheckBox("Show Countdown Before Recording")
        self.countdown_check.setStyleSheet(checkbox_style)
        self.countdown_check.setChecked(True)

        self.minimize_check = QCheckBox("Minimize to Tray When Recording")
        self.minimize_check.setStyleSheet(checkbox_style)
        self.minimize_check.setChecked(False)

        self.region_check = QCheckBox("Record Selected Region (Instead of Full Screen)")
        self.region_check.setStyleSheet(checkbox_style)
        self.region_check.setChecked(False)

        # Add checkboxes to layout
        options_inner_layout.addWidget(self.show_cursor_check)
        options_inner_layout.addWidget(self.countdown_check)
        options_inner_layout.addWidget(self.minimize_check)
        options_inner_layout.addWidget(self.region_check)

        # Set layout for options group
        options_group.setLayout(options_inner_layout)

        # Add options group to options tab layout
        options_layout.addWidget(options_group)
        options_layout.addStretch()

        # Add tabs to tab widget
        tabs.addTab(audio_tab, "Audio")
        tabs.addTab(video_tab, "Video")
        tabs.addTab(options_tab, "Options")

        # Add tabs to main layout
        main_layout.addWidget(tabs)

        # Add spacer
        main_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Select region button
        self.region_button = QPushButton("Select Region")
        self.region_button.setMinimumHeight(40)
        self.region_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #2196F3;"
            "    color: white;"
            "    border-radius: 6px;"
            "    padding: 8px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #0b7dda;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #0a69b7;"
            "}"
        )
        self.region_button.clicked.connect(self.select_region)
        buttons_layout.addWidget(self.region_button)

        # Start recording button
        self.start_button = QPushButton("Start Recording")
        self.start_button.setMinimumHeight(50)
        start_font = QFont()
        start_font.setPointSize(14)
        start_font.setBold(True)
        self.start_button.setFont(start_font)
        self.start_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-radius: 8px;"
            "    padding: 12px;"
            "    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3d8b40;"
            "    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);"
            "}"
        )

        # Connect button click to start recording
        self.start_button.clicked.connect(self.start_recording)
        buttons_layout.addWidget(self.start_button)

        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)

        # Set main layout
        self.setLayout(main_layout)

        # Apply initial theme
        self.apply_theme()

    def start_recording(self):
        """Start recording with the selected audio source."""
        # Determine selected audio source
        if self.mic_radio.isChecked():
            audio_source = "mic"
        elif self.system_radio.isChecked():
            audio_source = "system"
        elif self.both_radio.isChecked():
            audio_source = "both"
        else:  # none_radio is checked
            audio_source = "none"

        # Save settings
        if hasattr(self.parent, 'settings'):
            # Video quality
            if self.high_radio.isChecked():
                self.parent.settings.set("video_quality", "high")
            elif self.medium_radio.isChecked():
                self.parent.settings.set("video_quality", "medium")
            else:
                self.parent.settings.set("video_quality", "low")

            # Frame rate
            if self.fps_60_radio.isChecked():
                self.parent.settings.set("frame_rate", 60)
            elif self.fps_30_radio.isChecked():
                self.parent.settings.set("frame_rate", 30)
            else:
                self.parent.settings.set("frame_rate", 15)

            # Options
            self.parent.settings.set("show_cursor", self.show_cursor_check.isChecked())
            self.parent.settings.set("show_countdown", self.countdown_check.isChecked())
            self.parent.settings.set("minimize_on_record", self.minimize_check.isChecked())
            self.parent.settings.set("record_fullscreen", not self.region_check.isChecked())

        # Emit signal to start recording
        self.start_recording_signal.emit(audio_source)

    def select_region(self):
        """Signal to select a region for recording."""
        if hasattr(self.parent, 'select_region'):
            self.parent.select_region()
            # Update checkbox
            self.region_check.setChecked(True)

    def toggle_theme(self):
        """Toggle between light and dark theme."""
        if hasattr(self.parent, 'settings'):
            current_theme = self.parent.settings.get("theme", "light")
            new_theme = "dark" if current_theme == "light" else "light"
            self.parent.settings.set("theme", new_theme)
            self.apply_theme()

    def apply_theme(self):
        """Apply the current theme."""
        if not hasattr(self.parent, 'settings'):
            return

        theme = self.parent.settings.get("theme", "light")

        if theme == "dark":
            # Dark theme
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)

            QApplication.setPalette(palette)

            # Update theme button icon
            self.theme_button.setToolTip("Switch to Light Mode")
        else:
            # Light theme
            QApplication.setPalette(QApplication.style().standardPalette())

            # Update theme button icon
            self.theme_button.setToolTip("Switch to Dark Mode")
