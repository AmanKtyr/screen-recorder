#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings Module
-------------
Handles application settings and configuration.
"""

import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

class Settings(QObject):
    """Settings class to manage application configuration."""
    
    # Signals
    settings_changed_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        # Default settings
        self.default_settings = {
            "output_directory": os.path.join(os.path.expanduser("~"), "Videos", "ScreenRecordings"),
            "video_quality": "high",  # high, medium, low
            "frame_rate": 30,
            "audio_sample_rate": 44100,
            "audio_channels": 2,
            "default_audio_source": "mic",  # mic, system, both, none
            "show_countdown": True,
            "countdown_seconds": 3,
            "minimize_on_record": False,
            "recent_recordings": []
        }
        
        # Current settings
        self.settings = self.default_settings.copy()
        
        # Settings file path
        self.settings_file = os.path.join(
            os.path.expanduser("~"), 
            ".screen_recorder_settings.json"
        )
        
        # Load settings
        self.load_settings()
        
    def load_settings(self):
        """Load settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                    # Update settings with loaded values
                    for key, value in loaded_settings.items():
                        if key in self.settings:
                            self.settings[key] = value
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Use default settings
            self.settings = self.default_settings.copy()
            
    def save_settings(self):
        """Save settings to file."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
                
            # Emit signal
            self.settings_changed_signal.emit()
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get(self, key, default=None):
        """Get a setting value.
        
        Args:
            key (str): The setting key
            default: The default value to return if key is not found
            
        Returns:
            The setting value or default if not found
        """
        return self.settings.get(key, default)
        
    def set(self, key, value):
        """Set a setting value.
        
        Args:
            key (str): The setting key
            value: The setting value
        """
        if key in self.settings:
            self.settings[key] = value
            self.save_settings()
            
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.settings = self.default_settings.copy()
        self.save_settings()
        
    def add_recent_recording(self, file_path):
        """Add a file to recent recordings.
        
        Args:
            file_path (str): Path to the recording file
        """
        recent = self.settings.get("recent_recordings", [])
        
        # Add to the beginning of the list
        if file_path in recent:
            recent.remove(file_path)
        
        recent.insert(0, file_path)
        
        # Keep only the 10 most recent
        self.settings["recent_recordings"] = recent[:10]
        
        # Save settings
        self.save_settings()
