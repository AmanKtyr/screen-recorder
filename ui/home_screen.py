#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Home Screen Module
-----------------
The main screen of the application with the "Screen Recorder" button.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QGroupBox, QRadioButton, 
    QButtonGroup, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPixmap

class HomeScreen(QWidget):
    """Home screen widget with the screen recorder button."""
    
    # Signal emitted when the user starts recording
    start_recording_signal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Professional Screen Recorder")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Description
        desc_label = QLabel(
            "Record your screen with audio from your microphone, system, or both."
        )
        desc_label.setAlignment(Qt.AlignCenter)
        desc_font = QFont()
        desc_font.setPointSize(12)
        desc_label.setFont(desc_font)
        
        # Add title and description to layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(desc_label)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator)
        
        # Audio source selection
        audio_group = QGroupBox("Audio Source")
        audio_layout = QVBoxLayout()
        
        # Radio buttons for audio source
        self.mic_radio = QRadioButton("Microphone")
        self.system_radio = QRadioButton("System Sound")
        self.both_radio = QRadioButton("Both Microphone and System Sound")
        self.none_radio = QRadioButton("No Audio")
        
        # Set microphone as default
        self.mic_radio.setChecked(True)
        
        # Add radio buttons to layout
        audio_layout.addWidget(self.mic_radio)
        audio_layout.addWidget(self.system_radio)
        audio_layout.addWidget(self.both_radio)
        audio_layout.addWidget(self.none_radio)
        
        # Set layout for audio group
        audio_group.setLayout(audio_layout)
        
        # Add audio group to main layout
        main_layout.addWidget(audio_group)
        
        # Add spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
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
            "    border-radius: 5px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #45a049;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #3d8b40;"
            "}"
        )
        
        # Connect button click to start recording
        self.start_button.clicked.connect(self.start_recording)
        
        # Add button to main layout
        main_layout.addWidget(self.start_button)
        
        # Set main layout
        self.setLayout(main_layout)
        
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
        
        # Emit signal to start recording
        self.start_recording_signal.emit(audio_source)
