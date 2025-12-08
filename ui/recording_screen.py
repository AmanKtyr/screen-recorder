#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Recording Screen Module
----------------------
The screen shown during recording with controls to stop, pause, and toggle audio sources.
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QProgressBar, QSpacerItem, QSizePolicy, QFrame,
    QToolButton, QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette

class RecordingScreen(QWidget):
    """Recording screen widget with recording controls."""

    # Signals
    stop_recording_signal = pyqtSignal()
    pause_recording_signal = pyqtSignal()
    resume_recording_signal = pyqtSignal()
    toggle_mic_signal = pyqtSignal(bool)
    toggle_system_audio_signal = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize variables
        self.recording_time = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update_timer)
        self.is_paused = False
        self.parent = parent

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Recording status panel
        status_panel = QFrame()
        status_panel.setFrameShape(QFrame.StyledPanel)
        status_panel.setFrameShadow(QFrame.Raised)
        status_panel.setStyleSheet(
            "QFrame {"
            "    background-color: rgba(0, 0, 0, 0.1);"
            "    border-radius: 10px;"
            "    padding: 10px;"
            "}"
        )

        status_layout = QHBoxLayout(status_panel)

        # Recording indicator with pulsing animation
        self.rec_indicator = QLabel("● REC")
        self.rec_indicator.setStyleSheet(
            "color: red; font-weight: bold; padding: 5px 10px;"
            "background-color: rgba(255, 0, 0, 0.1); border-radius: 5px;"
        )
        rec_font = QFont()
        rec_font.setPointSize(16)
        self.rec_indicator.setFont(rec_font)

        # Timer display
        self.timer_label = QLabel("00:00:00")
        timer_font = QFont()
        timer_font.setPointSize(24)
        timer_font.setFamily("Monospace")
        timer_font.setBold(True)
        self.timer_label.setFont(timer_font)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet(
            "padding: 5px 15px;"
            "background-color: rgba(0, 0, 0, 0.05);"
            "border-radius: 5px;"
        )

        # Add widgets to status layout
        status_layout.addWidget(self.rec_indicator)
        status_layout.addStretch()
        status_layout.addWidget(self.timer_label)

        # Add status panel to main layout
        main_layout.addWidget(status_panel)

        # Audio controls panel
        audio_panel = QFrame()
        audio_panel.setFrameShape(QFrame.StyledPanel)
        audio_panel.setFrameShadow(QFrame.Raised)
        audio_panel.setStyleSheet(
            "QFrame {"
            "    background-color: rgba(0, 0, 0, 0.05);"
            "    border-radius: 10px;"
            "    padding: 10px;"
            "}"
        )

        audio_layout = QHBoxLayout(audio_panel)

        # Audio controls label
        audio_label = QLabel("Audio Controls:")
        audio_label.setFont(QFont("", 12, QFont.Bold))
        audio_layout.addWidget(audio_label)

        # Microphone toggle button
        self.mic_button = QPushButton("Microphone")
        self.mic_button.setCheckable(True)
        self.mic_button.setChecked(True)
        self.mic_button.setMinimumHeight(36)
        self.mic_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "mic_icon.png")))
        self.mic_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-radius: 5px;"
            "    padding: 5px 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3d8b40;"
            "}"
            "QPushButton:checked {"
            "    background-color: #4CAF50;"
            "}"
            "QPushButton:!checked {"
            "    background-color: #f44336;"
            "}"
        )
        self.mic_button.clicked.connect(self.toggle_microphone)

        # System audio toggle button
        self.system_button = QPushButton("System Audio")
        self.system_button.setCheckable(True)
        self.system_button.setChecked(True)
        self.system_button.setMinimumHeight(36)
        self.system_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "speaker_icon.png")))
        self.system_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #4CAF50;"
            "    color: white;"
            "    border-radius: 5px;"
            "    padding: 5px 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3d8b40;"
            "}"
            "QPushButton:checked {"
            "    background-color: #4CAF50;"
            "}"
            "QPushButton:!checked {"
            "    background-color: #f44336;"
            "}"
        )
        self.system_button.clicked.connect(self.toggle_system_audio)

        # Add buttons to audio layout
        audio_layout.addWidget(self.mic_button)
        audio_layout.addWidget(self.system_button)

        # Add audio panel to main layout
        main_layout.addWidget(audio_panel)

        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Recording info
        info_label = QLabel("Recording in progress. Use the controls below to manage your recording.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_font = QFont()
        info_font.setPointSize(11)
        info_label.setFont(info_font)
        main_layout.addWidget(info_label)

        # Recording controls panel
        controls_panel = QFrame()
        controls_panel.setFrameShape(QFrame.StyledPanel)
        controls_panel.setFrameShadow(QFrame.Raised)
        controls_panel.setStyleSheet(
            "QFrame {"
            "    background-color: rgba(0, 0, 0, 0.05);"
            "    border-radius: 10px;"
            "    padding: 15px;"
            "}"
        )

        controls_layout = QHBoxLayout(controls_panel)

        # Pause/Resume button
        self.pause_button = QPushButton("Pause Recording")
        self.pause_button.setMinimumHeight(50)
        self.pause_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "pause_icon.png")))
        self.pause_button.setIconSize(QSize(24, 24))
        self.pause_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #2196F3;"
            "    color: white;"
            "    border-radius: 5px;"
            "    padding: 10px;"
            "    font-weight: bold;"
            "    font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #1976D2;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #0D47A1;"
            "}"
        )
        self.pause_button.clicked.connect(self.toggle_pause_resume)

        # Stop button
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "stop_icon.png")))
        self.stop_button.setIconSize(QSize(24, 24))
        self.stop_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #f44336;"
            "    color: white;"
            "    border-radius: 5px;"
            "    padding: 10px;"
            "    font-weight: bold;"
            "    font-size: 14px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #d32f2f;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #b71c1c;"
            "}"
        )
        self.stop_button.clicked.connect(self.stop_recording)

        # Add buttons to controls layout
        controls_layout.addWidget(self.pause_button)
        controls_layout.addWidget(self.stop_button)

        # Add controls panel to main layout
        main_layout.addWidget(controls_panel)

        # Set main layout
        self.setLayout(main_layout)

        # Apply theme if available
        self.apply_theme()

        # Start pulsing animation for recording indicator
        self.pulse_timer = QTimer()
        self.pulse_timer.setInterval(1000)  # 1 second
        self.pulse_timer.timeout.connect(self.pulse_recording_indicator)
        self.pulse_timer.start()

    def start_timer(self):
        """Start the recording timer."""
        self.recording_time = 0
        self.timer.start()
        self.update_timer()

    def pause_timer(self):
        """Pause the recording timer."""
        self.timer.stop()
        self.is_paused = True
        self.rec_indicator.setText("❚❚ PAUSED")
        self.rec_indicator.setStyleSheet(
            "color: orange; font-weight: bold; padding: 5px 10px;"
            "background-color: rgba(255, 165, 0, 0.1); border-radius: 5px;"
        )
        self.pause_button.setText("Resume Recording")
        self.pause_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "play_icon.png")))
        self.pulse_timer.stop()

    def resume_timer(self):
        """Resume the recording timer."""
        self.timer.start()
        self.is_paused = False
        self.rec_indicator.setText("● REC")
        self.rec_indicator.setStyleSheet(
            "color: red; font-weight: bold; padding: 5px 10px;"
            "background-color: rgba(255, 0, 0, 0.1); border-radius: 5px;"
        )
        self.pause_button.setText("Pause Recording")
        self.pause_button.setIcon(QIcon(os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "pause_icon.png")))
        self.pulse_timer.start()

    def update_timer(self):
        """Update the timer display."""
        self.recording_time += 1
        hours = self.recording_time // 3600
        minutes = (self.recording_time % 3600) // 60
        seconds = self.recording_time % 60

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.setText(time_str)

    def pulse_recording_indicator(self):
        """Create a pulsing effect for the recording indicator."""
        if not self.is_paused:
            current_style = self.rec_indicator.styleSheet()
            if "rgba(255, 0, 0, 0.1)" in current_style:
                self.rec_indicator.setStyleSheet(
                    "color: red; font-weight: bold; padding: 5px 10px;"
                    "background-color: rgba(255, 0, 0, 0.3); border-radius: 5px;"
                )
            else:
                self.rec_indicator.setStyleSheet(
                    "color: red; font-weight: bold; padding: 5px 10px;"
                    "background-color: rgba(255, 0, 0, 0.1); border-radius: 5px;"
                )

    def toggle_pause_resume(self):
        """Toggle between pause and resume states."""
        if self.is_paused:
            self.resume_recording_signal.emit()
        else:
            self.pause_recording_signal.emit()

    def stop_recording(self):
        """Stop the recording."""
        self.timer.stop()
        self.pulse_timer.stop()
        self.stop_recording_signal.emit()

    def toggle_microphone(self, checked):
        """Toggle microphone recording.

        Args:
            checked (bool): Whether the microphone button is checked
        """
        self.toggle_mic_signal.emit(checked)
        if checked:
            self.mic_button.setText("Microphone On")
        else:
            self.mic_button.setText("Microphone Off")

    def toggle_system_audio(self, checked):
        """Toggle system audio recording.

        Args:
            checked (bool): Whether the system audio button is checked
        """
        self.toggle_system_audio_signal.emit(checked)
        if checked:
            self.system_button.setText("System Audio On")
        else:
            self.system_button.setText("System Audio Off")

    def apply_theme(self):
        """Apply the current theme if available."""
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
