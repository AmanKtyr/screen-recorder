#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings Screen Module
--------------------
Screen for configuring application settings.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QSpinBox, QCheckBox, QTabWidget,
    QGroupBox, QFormLayout, QFileDialog, QLineEdit,
    QSlider, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class SettingsScreen(QWidget):
    """Settings screen widget for configuring the application."""
    
    # Signals
    settings_saved_signal = pyqtSignal()
    settings_canceled_signal = pyqtSignal()
    
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        # Add title to layout
        main_layout.addWidget(title_label)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # General settings tab
        general_tab = QWidget()
        tab_widget.addTab(general_tab, "General")
        
        # Video settings tab
        video_tab = QWidget()
        tab_widget.addTab(video_tab, "Video")
        
        # Audio settings tab
        audio_tab = QWidget()
        tab_widget.addTab(audio_tab, "Audio")
        
        # Hotkeys tab
        hotkeys_tab = QWidget()
        tab_widget.addTab(hotkeys_tab, "Hotkeys")
        
        # Add tab widget to main layout
        main_layout.addWidget(tab_widget)
        
        # Set up general tab
        self._setup_general_tab(general_tab)
        
        # Set up video tab
        self._setup_video_tab(video_tab)
        
        # Set up audio tab
        self._setup_audio_tab(audio_tab)
        
        # Set up hotkeys tab
        self._setup_hotkeys_tab(hotkeys_tab)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._on_cancel)
        
        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet(
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
        self.save_button.clicked.connect(self._on_save)
        
        # Add buttons to layout
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        
        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        
    def _setup_general_tab(self, tab):
        """Set up the general settings tab.
        
        Args:
            tab (QWidget): The tab widget to set up
        """
        # Layout
        layout = QVBoxLayout()
        
        # Output directory group
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout()
        
        # Output directory field
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setText(self.settings.get("output_directory"))
        self.output_dir_edit.setReadOnly(True)
        
        # Browse button
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._browse_output_dir)
        
        # Add widgets to layout
        output_layout.addWidget(self.output_dir_edit)
        output_layout.addWidget(browse_button)
        
        # Set layout for output group
        output_group.setLayout(output_layout)
        
        # Add output group to tab layout
        layout.addWidget(output_group)
        
        # Recording options group
        options_group = QGroupBox("Recording Options")
        options_layout = QFormLayout()
        
        # Show countdown option
        self.show_countdown_check = QCheckBox()
        self.show_countdown_check.setChecked(self.settings.get("show_countdown"))
        options_layout.addRow("Show countdown before recording:", self.show_countdown_check)
        
        # Countdown seconds
        self.countdown_spin = QSpinBox()
        self.countdown_spin.setRange(1, 10)
        self.countdown_spin.setValue(self.settings.get("countdown_seconds"))
        options_layout.addRow("Countdown seconds:", self.countdown_spin)
        
        # Minimize on record option
        self.minimize_check = QCheckBox()
        self.minimize_check.setChecked(self.settings.get("minimize_on_record"))
        options_layout.addRow("Minimize to tray when recording:", self.minimize_check)
        
        # Default audio source
        self.audio_source_combo = QComboBox()
        self.audio_source_combo.addItems(["Microphone", "System Sound", "Both", "None"])
        
        # Set current index based on settings
        audio_source = self.settings.get("default_audio_source")
        if audio_source == "mic":
            self.audio_source_combo.setCurrentIndex(0)
        elif audio_source == "system":
            self.audio_source_combo.setCurrentIndex(1)
        elif audio_source == "both":
            self.audio_source_combo.setCurrentIndex(2)
        else:  # "none"
            self.audio_source_combo.setCurrentIndex(3)
            
        options_layout.addRow("Default audio source:", self.audio_source_combo)
        
        # Set layout for options group
        options_group.setLayout(options_layout)
        
        # Add options group to tab layout
        layout.addWidget(options_group)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Set layout for tab
        tab.setLayout(layout)
        
    def _setup_video_tab(self, tab):
        """Set up the video settings tab.
        
        Args:
            tab (QWidget): The tab widget to set up
        """
        # Layout
        layout = QVBoxLayout()
        
        # Video quality group
        quality_group = QGroupBox("Video Quality")
        quality_layout = QFormLayout()
        
        # Video quality combo
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["Low", "Medium", "High", "Ultra"])
        
        # Set current index based on settings
        quality = self.settings.get("video_quality")
        if quality == "low":
            self.quality_combo.setCurrentIndex(0)
        elif quality == "medium":
            self.quality_combo.setCurrentIndex(1)
        elif quality == "high":
            self.quality_combo.setCurrentIndex(2)
        else:  # "ultra"
            self.quality_combo.setCurrentIndex(3)
            
        quality_layout.addRow("Quality preset:", self.quality_combo)
        
        # Frame rate
        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(15, 60)
        self.fps_spin.setValue(self.settings.get("frame_rate"))
        quality_layout.addRow("Frame rate (FPS):", self.fps_spin)
        
        # Set layout for quality group
        quality_group.setLayout(quality_layout)
        
        # Add quality group to tab layout
        layout.addWidget(quality_group)
        
        # Region selection group
        region_group = QGroupBox("Region Selection")
        region_layout = QFormLayout()
        
        # Full screen option
        self.fullscreen_check = QCheckBox()
        self.fullscreen_check.setChecked(self.settings.get("record_fullscreen", True))
        self.fullscreen_check.stateChanged.connect(self._toggle_region_selection)
        region_layout.addRow("Record full screen:", self.fullscreen_check)
        
        # Region selection option
        self.region_check = QCheckBox()
        self.region_check.setChecked(not self.settings.get("record_fullscreen", True))
        self.region_check.stateChanged.connect(self._toggle_fullscreen)
        region_layout.addRow("Record selected region:", self.region_check)
        
        # Set layout for region group
        region_group.setLayout(region_layout)
        
        # Add region group to tab layout
        layout.addWidget(region_group)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Set layout for tab
        tab.setLayout(layout)
        
    def _setup_audio_tab(self, tab):
        """Set up the audio settings tab.
        
        Args:
            tab (QWidget): The tab widget to set up
        """
        # Layout
        layout = QVBoxLayout()
        
        # Audio quality group
        quality_group = QGroupBox("Audio Quality")
        quality_layout = QFormLayout()
        
        # Sample rate combo
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["44100 Hz", "48000 Hz", "96000 Hz"])
        
        # Set current index based on settings
        sample_rate = self.settings.get("audio_sample_rate")
        if sample_rate == 44100:
            self.sample_rate_combo.setCurrentIndex(0)
        elif sample_rate == 48000:
            self.sample_rate_combo.setCurrentIndex(1)
        else:  # 96000
            self.sample_rate_combo.setCurrentIndex(2)
            
        quality_layout.addRow("Sample rate:", self.sample_rate_combo)
        
        # Channels combo
        self.channels_combo = QComboBox()
        self.channels_combo.addItems(["Mono (1)", "Stereo (2)"])
        
        # Set current index based on settings
        channels = self.settings.get("audio_channels")
        if channels == 1:
            self.channels_combo.setCurrentIndex(0)
        else:  # 2
            self.channels_combo.setCurrentIndex(1)
            
        quality_layout.addRow("Channels:", self.channels_combo)
        
        # Set layout for quality group
        quality_group.setLayout(quality_layout)
        
        # Add quality group to tab layout
        layout.addWidget(quality_group)
        
        # Volume levels group
        volume_group = QGroupBox("Volume Levels")
        volume_layout = QFormLayout()
        
        # Microphone volume
        self.mic_volume_slider = QSlider(Qt.Horizontal)
        self.mic_volume_slider.setRange(0, 100)
        self.mic_volume_slider.setValue(self.settings.get("mic_volume", 80))
        volume_layout.addRow("Microphone volume:", self.mic_volume_slider)
        
        # System volume
        self.system_volume_slider = QSlider(Qt.Horizontal)
        self.system_volume_slider.setRange(0, 100)
        self.system_volume_slider.setValue(self.settings.get("system_volume", 80))
        volume_layout.addRow("System volume:", self.system_volume_slider)
        
        # Set layout for volume group
        volume_group.setLayout(volume_layout)
        
        # Add volume group to tab layout
        layout.addWidget(volume_group)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Set layout for tab
        tab.setLayout(layout)
        
    def _setup_hotkeys_tab(self, tab):
        """Set up the hotkeys settings tab.
        
        Args:
            tab (QWidget): The tab widget to set up
        """
        # Layout
        layout = QVBoxLayout()
        
        # Hotkeys group
        hotkeys_group = QGroupBox("Keyboard Shortcuts")
        hotkeys_layout = QFormLayout()
        
        # Start/Stop recording hotkey
        self.start_stop_edit = QLineEdit()
        self.start_stop_edit.setText(self.settings.get("hotkey_start_stop", "Ctrl+R"))
        hotkeys_layout.addRow("Start/Stop recording:", self.start_stop_edit)
        
        # Pause/Resume recording hotkey
        self.pause_resume_edit = QLineEdit()
        self.pause_resume_edit.setText(self.settings.get("hotkey_pause_resume", "Ctrl+P"))
        hotkeys_layout.addRow("Pause/Resume recording:", self.pause_resume_edit)
        
        # Toggle microphone hotkey
        self.toggle_mic_edit = QLineEdit()
        self.toggle_mic_edit.setText(self.settings.get("hotkey_toggle_mic", "Ctrl+M"))
        hotkeys_layout.addRow("Toggle microphone:", self.toggle_mic_edit)
        
        # Toggle system audio hotkey
        self.toggle_system_edit = QLineEdit()
        self.toggle_system_edit.setText(self.settings.get("hotkey_toggle_system", "Ctrl+S"))
        hotkeys_layout.addRow("Toggle system audio:", self.toggle_system_edit)
        
        # Set layout for hotkeys group
        hotkeys_group.setLayout(hotkeys_layout)
        
        # Add hotkeys group to tab layout
        layout.addWidget(hotkeys_group)
        
        # Enable hotkeys checkbox
        self.enable_hotkeys_check = QCheckBox("Enable global hotkeys")
        self.enable_hotkeys_check.setChecked(self.settings.get("enable_hotkeys", True))
        layout.addWidget(self.enable_hotkeys_check)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Set layout for tab
        tab.setLayout(layout)
        
    def _browse_output_dir(self):
        """Open a file dialog to select the output directory."""
        current_dir = self.output_dir_edit.text()
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Output Directory",
            current_dir
        )
        
        if directory:
            self.output_dir_edit.setText(directory)
            
    def _toggle_region_selection(self, state):
        """Toggle the region selection checkbox based on fullscreen state.
        
        Args:
            state (int): The state of the fullscreen checkbox
        """
        self.region_check.setChecked(state != Qt.Checked)
            
    def _toggle_fullscreen(self, state):
        """Toggle the fullscreen checkbox based on region selection state.
        
        Args:
            state (int): The state of the region selection checkbox
        """
        self.fullscreen_check.setChecked(state != Qt.Checked)
            
    def _on_save(self):
        """Save the settings and emit the saved signal."""
        # General settings
        self.settings.set("output_directory", self.output_dir_edit.text())
        self.settings.set("show_countdown", self.show_countdown_check.isChecked())
        self.settings.set("countdown_seconds", self.countdown_spin.value())
        self.settings.set("minimize_on_record", self.minimize_check.isChecked())
        
        # Audio source
        audio_source_index = self.audio_source_combo.currentIndex()
        if audio_source_index == 0:
            self.settings.set("default_audio_source", "mic")
        elif audio_source_index == 1:
            self.settings.set("default_audio_source", "system")
        elif audio_source_index == 2:
            self.settings.set("default_audio_source", "both")
        else:  # 3
            self.settings.set("default_audio_source", "none")
            
        # Video settings
        quality_index = self.quality_combo.currentIndex()
        if quality_index == 0:
            self.settings.set("video_quality", "low")
        elif quality_index == 1:
            self.settings.set("video_quality", "medium")
        elif quality_index == 2:
            self.settings.set("video_quality", "high")
        else:  # 3
            self.settings.set("video_quality", "ultra")
            
        self.settings.set("frame_rate", self.fps_spin.value())
        self.settings.set("record_fullscreen", self.fullscreen_check.isChecked())
        
        # Audio settings
        sample_rate_index = self.sample_rate_combo.currentIndex()
        if sample_rate_index == 0:
            self.settings.set("audio_sample_rate", 44100)
        elif sample_rate_index == 1:
            self.settings.set("audio_sample_rate", 48000)
        else:  # 2
            self.settings.set("audio_sample_rate", 96000)
            
        channels_index = self.channels_combo.currentIndex()
        if channels_index == 0:
            self.settings.set("audio_channels", 1)
        else:  # 1
            self.settings.set("audio_channels", 2)
            
        self.settings.set("mic_volume", self.mic_volume_slider.value())
        self.settings.set("system_volume", self.system_volume_slider.value())
        
        # Hotkey settings
        self.settings.set("hotkey_start_stop", self.start_stop_edit.text())
        self.settings.set("hotkey_pause_resume", self.pause_resume_edit.text())
        self.settings.set("hotkey_toggle_mic", self.toggle_mic_edit.text())
        self.settings.set("hotkey_toggle_system", self.toggle_system_edit.text())
        self.settings.set("enable_hotkeys", self.enable_hotkeys_check.isChecked())
        
        # Emit signal
        self.settings_saved_signal.emit()
        
    def _on_cancel(self):
        """Cancel the settings changes and emit the canceled signal."""
        self.settings_canceled_signal.emit()
