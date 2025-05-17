#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Recording Screen Module
----------------------
The screen shown during recording with controls to stop, pause, and toggle audio sources.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QProgressBar, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon

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
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Recording status
        status_layout = QHBoxLayout()
        
        # Recording indicator
        self.rec_indicator = QLabel("● REC")
        self.rec_indicator.setStyleSheet("color: red; font-weight: bold;")
        rec_font = QFont()
        rec_font.setPointSize(16)
        self.rec_indicator.setFont(rec_font)
        
        # Timer display
        self.timer_label = QLabel("00:00:00")
        timer_font = QFont()
        timer_font.setPointSize(16)
        timer_font.setFamily("Monospace")
        self.timer_label.setFont(timer_font)
        self.timer_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # Add widgets to status layout
        status_layout.addWidget(self.rec_indicator)
        status_layout.addStretch()
        status_layout.addWidget(self.timer_label)
        
        # Add status layout to main layout
        main_layout.addLayout(status_layout)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Audio controls
        audio_layout = QHBoxLayout()
        
        # Microphone toggle button
        self.mic_button = QPushButton("Microphone")
        self.mic_button.setCheckable(True)
        self.mic_button.setChecked(True)
        self.mic_button.clicked.connect(self.toggle_microphone)
        
        # System audio toggle button
        self.system_button = QPushButton("System Audio")
        self.system_button.setCheckable(True)
        self.system_button.setChecked(True)
        self.system_button.clicked.connect(self.toggle_system_audio)
        
        # Add buttons to audio layout
        audio_layout.addWidget(self.mic_button)
        audio_layout.addWidget(self.system_button)
        
        # Add audio layout to main layout
        main_layout.addLayout(audio_layout)
        
        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Recording controls
        controls_layout = QHBoxLayout()
        
        # Pause/Resume button
        self.pause_button = QPushButton("Pause")
        self.pause_button.setMinimumHeight(40)
        self.pause_button.clicked.connect(self.toggle_pause_resume)
        
        # Stop button
        self.stop_button = QPushButton("Stop Recording")
        self.stop_button.setMinimumHeight(40)
        self.stop_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #f44336;"
            "    color: white;"
            "    border-radius: 5px;"
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
        
        # Add controls layout to main layout
        main_layout.addLayout(controls_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        
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
        self.rec_indicator.setStyleSheet("color: orange; font-weight: bold;")
        self.pause_button.setText("Resume")
        
    def resume_timer(self):
        """Resume the recording timer."""
        self.timer.start()
        self.is_paused = False
        self.rec_indicator.setText("● REC")
        self.rec_indicator.setStyleSheet("color: red; font-weight: bold;")
        self.pause_button.setText("Pause")
        
    def update_timer(self):
        """Update the timer display."""
        self.recording_time += 1
        hours = self.recording_time // 3600
        minutes = (self.recording_time % 3600) // 60
        seconds = self.recording_time % 60
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.setText(time_str)
        
    def toggle_pause_resume(self):
        """Toggle between pause and resume states."""
        if self.is_paused:
            self.resume_recording_signal.emit()
        else:
            self.pause_recording_signal.emit()
            
    def stop_recording(self):
        """Stop the recording."""
        self.timer.stop()
        self.stop_recording_signal.emit()
        
    def toggle_microphone(self, checked):
        """Toggle microphone recording.
        
        Args:
            checked (bool): Whether the microphone button is checked
        """
        self.toggle_mic_signal.emit(checked)
        
    def toggle_system_audio(self, checked):
        """Toggle system audio recording.
        
        Args:
            checked (bool): Whether the system audio button is checked
        """
        self.toggle_system_audio_signal.emit(checked)
