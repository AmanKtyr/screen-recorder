#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hotkey Manager Module
-------------------
Manages global hotkeys for the application.
"""

import sys
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication

class HotkeyManager(QObject):
    """Manages global hotkeys for the application."""
    
    # Signals
    start_stop_signal = pyqtSignal()
    pause_resume_signal = pyqtSignal()
    toggle_mic_signal = pyqtSignal()
    toggle_system_signal = pyqtSignal()
    
    def __init__(self, settings):
        super().__init__()
        
        self.settings = settings
        self.enabled = settings.get("enable_hotkeys", True)
        
        # Parse hotkeys
        self.hotkeys = {
            "start_stop": self._parse_hotkey(settings.get("hotkey_start_stop", "Ctrl+R")),
            "pause_resume": self._parse_hotkey(settings.get("hotkey_pause_resume", "Ctrl+P")),
            "toggle_mic": self._parse_hotkey(settings.get("hotkey_toggle_mic", "Ctrl+M")),
            "toggle_system": self._parse_hotkey(settings.get("hotkey_toggle_system", "Ctrl+S"))
        }
        
        # Install event filter
        QApplication.instance().installEventFilter(self)
        
    def _parse_hotkey(self, hotkey_str):
        """Parse a hotkey string into modifiers and key.
        
        Args:
            hotkey_str (str): The hotkey string (e.g., "Ctrl+R")
            
        Returns:
            tuple: (modifiers, key)
        """
        parts = hotkey_str.split("+")
        
        # Initialize modifiers
        modifiers = Qt.NoModifier
        
        # Parse modifiers
        for i in range(len(parts) - 1):
            modifier = parts[i].lower()
            
            if modifier == "ctrl":
                modifiers |= Qt.ControlModifier
            elif modifier == "alt":
                modifiers |= Qt.AltModifier
            elif modifier == "shift":
                modifiers |= Qt.ShiftModifier
            elif modifier == "meta":
                modifiers |= Qt.MetaModifier
                
        # Parse key
        key_str = parts[-1].upper()
        
        # Handle function keys
        if key_str.startswith("F") and len(key_str) > 1:
            try:
                key_num = int(key_str[1:])
                if 1 <= key_num <= 12:
                    key = getattr(Qt, f"Key_F{key_num}")
                else:
                    key = None
            except ValueError:
                key = None
        else:
            # Handle regular keys
            key_map = {
                "A": Qt.Key_A,
                "B": Qt.Key_B,
                "C": Qt.Key_C,
                "D": Qt.Key_D,
                "E": Qt.Key_E,
                "F": Qt.Key_F,
                "G": Qt.Key_G,
                "H": Qt.Key_H,
                "I": Qt.Key_I,
                "J": Qt.Key_J,
                "K": Qt.Key_K,
                "L": Qt.Key_L,
                "M": Qt.Key_M,
                "N": Qt.Key_N,
                "O": Qt.Key_O,
                "P": Qt.Key_P,
                "Q": Qt.Key_Q,
                "R": Qt.Key_R,
                "S": Qt.Key_S,
                "T": Qt.Key_T,
                "U": Qt.Key_U,
                "V": Qt.Key_V,
                "W": Qt.Key_W,
                "X": Qt.Key_X,
                "Y": Qt.Key_Y,
                "Z": Qt.Key_Z,
                "0": Qt.Key_0,
                "1": Qt.Key_1,
                "2": Qt.Key_2,
                "3": Qt.Key_3,
                "4": Qt.Key_4,
                "5": Qt.Key_5,
                "6": Qt.Key_6,
                "7": Qt.Key_7,
                "8": Qt.Key_8,
                "9": Qt.Key_9,
                "SPACE": Qt.Key_Space,
                "RETURN": Qt.Key_Return,
                "ENTER": Qt.Key_Enter,
                "TAB": Qt.Key_Tab,
                "ESCAPE": Qt.Key_Escape,
                "ESC": Qt.Key_Escape,
                "BACKSPACE": Qt.Key_Backspace,
                "DELETE": Qt.Key_Delete,
                "DEL": Qt.Key_Delete,
                "INSERT": Qt.Key_Insert,
                "INS": Qt.Key_Insert,
                "HOME": Qt.Key_Home,
                "END": Qt.Key_End,
                "PAGEUP": Qt.Key_PageUp,
                "PAGEDOWN": Qt.Key_PageDown,
                "UP": Qt.Key_Up,
                "DOWN": Qt.Key_Down,
                "LEFT": Qt.Key_Left,
                "RIGHT": Qt.Key_Right
            }
            
            key = key_map.get(key_str, None)
            
        return (modifiers, key)
        
    def eventFilter(self, obj, event):
        """Filter events to catch global hotkeys.
        
        Args:
            obj (QObject): The object that received the event
            event (QEvent): The event
            
        Returns:
            bool: True if the event was handled, False otherwise
        """
        if not self.enabled:
            return False
            
        if event.type() == event.KeyPress:
            # Get modifiers and key
            modifiers = event.modifiers()
            key = event.key()
            
            # Check if this is a hotkey
            if (modifiers, key) == self.hotkeys["start_stop"]:
                self.start_stop_signal.emit()
                return True
                
            elif (modifiers, key) == self.hotkeys["pause_resume"]:
                self.pause_resume_signal.emit()
                return True
                
            elif (modifiers, key) == self.hotkeys["toggle_mic"]:
                self.toggle_mic_signal.emit()
                return True
                
            elif (modifiers, key) == self.hotkeys["toggle_system"]:
                self.toggle_system_signal.emit()
                return True
                
        return False
        
    def update_hotkeys(self):
        """Update hotkeys from settings."""
        self.enabled = self.settings.get("enable_hotkeys", True)
        
        # Parse hotkeys
        self.hotkeys = {
            "start_stop": self._parse_hotkey(self.settings.get("hotkey_start_stop", "Ctrl+R")),
            "pause_resume": self._parse_hotkey(self.settings.get("hotkey_pause_resume", "Ctrl+P")),
            "toggle_mic": self._parse_hotkey(self.settings.get("hotkey_toggle_mic", "Ctrl+M")),
            "toggle_system": self._parse_hotkey(self.settings.get("hotkey_toggle_system", "Ctrl+S"))
        }
        
    def enable(self):
        """Enable hotkeys."""
        self.enabled = True
        
    def disable(self):
        """Disable hotkeys."""
        self.enabled = False
