#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Screen Recorder Application
---------------------------
A professional screen recording application with the ability to record:
- Screen video
- Microphone audio
- System audio
- Both audio sources simultaneously
- Region selection
- Hotkey support
- Countdown timer
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox,
    QAction, QMenu, QSystemTrayIcon, QStyle
)
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QIcon

from ui.home_screen import HomeScreen
from ui.recording_screen import RecordingScreen
from ui.settings_screen import SettingsScreen
from ui.recordings_manager import RecordingsManager
from ui.region_selector import RegionSelector
from ui.countdown_timer import CountdownTimer
from core.screen_recorder import ScreenRecorder
from core.audio_manager import AudioManager
from utils.settings import Settings
from utils.hotkey_manager import HotkeyManager

class ScreenRecorderApp(QMainWindow):
    """Main application class for the Screen Recorder."""

    def __init__(self):
        super().__init__()

        # Initialize settings
        self.settings = Settings()

        # Initialize audio manager
        self.audio_manager = AudioManager()

        # Initialize screen recorder
        self.screen_recorder = ScreenRecorder(self.audio_manager)

        # Initialize hotkey manager
        self.hotkey_manager = HotkeyManager(self.settings)

        # Initialize variables
        self.is_recording = False
        self.is_paused = False
        self.selected_region = None
        self.tray_icon = None

        # Set up UI
        self.init_ui()

        # Connect signals
        self.connect_signals()

    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Professional Screen Recorder")
        self.setMinimumSize(800, 600)

        # Create menu bar
        self.create_menu_bar()

        # Create system tray icon
        self.create_tray_icon()

        # Set up home screen as the central widget
        self.home_screen = HomeScreen(self)
        self.setCentralWidget(self.home_screen)

        # Create other screens (not shown initially)
        self.recording_screen = RecordingScreen(self)
        self.settings_screen = SettingsScreen(self.settings)
        self.recordings_manager = RecordingsManager(self.settings)

        # Show the window
        self.show()

    def create_menu_bar(self):
        """Create the menu bar."""
        # File menu
        file_menu = self.menuBar().addMenu("File")

        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        file_menu.addAction(settings_action)

        # Recordings manager action
        recordings_action = QAction("Recordings Manager", self)
        recordings_action.triggered.connect(self.show_recordings_manager)
        file_menu.addAction(recordings_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Recording menu
        recording_menu = self.menuBar().addMenu("Recording")

        # Start recording action
        self.start_action = QAction("Start Recording", self)
        self.start_action.triggered.connect(self.start_recording_menu)
        recording_menu.addAction(self.start_action)

        # Stop recording action
        self.stop_action = QAction("Stop Recording", self)
        self.stop_action.triggered.connect(self.stop_recording)
        self.stop_action.setEnabled(False)
        recording_menu.addAction(self.stop_action)

        # Pause/Resume recording action
        self.pause_action = QAction("Pause Recording", self)
        self.pause_action.triggered.connect(self.toggle_pause_resume)
        self.pause_action.setEnabled(False)
        recording_menu.addAction(self.pause_action)

        recording_menu.addSeparator()

        # Select region action
        self.region_action = QAction("Select Region", self)
        self.region_action.triggered.connect(self.select_region)
        recording_menu.addAction(self.region_action)

        # Help menu
        help_menu = self.menuBar().addMenu("Help")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_tray_icon(self):
        """Create the system tray icon."""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # Create tray menu
        tray_menu = QMenu()

        # Show/hide action
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        # Start recording action
        start_action = QAction("Start Recording", self)
        start_action.triggered.connect(self.start_recording_menu)
        tray_menu.addAction(start_action)

        # Stop recording action
        stop_action = QAction("Stop Recording", self)
        stop_action.triggered.connect(self.stop_recording)
        tray_menu.addAction(stop_action)

        tray_menu.addSeparator()

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)

        # Set tray menu
        self.tray_icon.setContextMenu(tray_menu)

        # Show tray icon
        self.tray_icon.show()

    def connect_signals(self):
        """Connect signals and slots."""
        # Connect home screen signals
        self.home_screen.start_recording_signal.connect(self.start_recording)

        # Connect recording screen signals
        self.recording_screen.stop_recording_signal.connect(self.stop_recording)
        self.recording_screen.pause_recording_signal.connect(self.pause_recording)
        self.recording_screen.resume_recording_signal.connect(self.resume_recording)
        self.recording_screen.toggle_mic_signal.connect(self.toggle_microphone)
        self.recording_screen.toggle_system_audio_signal.connect(self.toggle_system_audio)

        # Connect settings screen signals
        self.settings_screen.settings_saved_signal.connect(self.on_settings_saved)
        self.settings_screen.settings_canceled_signal.connect(self.on_settings_canceled)

        # Connect hotkey manager signals
        self.hotkey_manager.start_stop_signal.connect(self.toggle_start_stop)
        self.hotkey_manager.pause_resume_signal.connect(self.toggle_pause_resume)
        self.hotkey_manager.toggle_mic_signal.connect(self.toggle_mic_hotkey)
        self.hotkey_manager.toggle_system_signal.connect(self.toggle_system_hotkey)

    def start_recording_menu(self):
        """Start recording from menu action."""
        # Use default audio source from settings
        audio_source = self.settings.get("default_audio_source", "mic")
        self.start_recording(audio_source)

    def start_recording(self, audio_source):
        """Start the recording process.

        Args:
            audio_source (str): The audio source to record from ('mic', 'system', 'both', or 'none')
        """
        try:
            # Check if already recording
            if self.is_recording:
                return

            # Show countdown if enabled
            if self.settings.get("show_countdown", True):
                countdown_seconds = self.settings.get("countdown_seconds", 3)
                CountdownTimer.countdown(countdown_seconds, self)

            # Select region if not recording fullscreen
            if not self.settings.get("record_fullscreen", True) and self.selected_region is None:
                self.select_region()

                # Check if region selection was canceled
                if self.selected_region is None:
                    return

            # Configure audio sources
            self.audio_manager.configure_audio_source(audio_source)

            # Configure screen recorder
            if self.selected_region is not None:
                self.screen_recorder.set_region(self.selected_region)
            else:
                self.screen_recorder.set_fullscreen()

            # Start recording
            self.screen_recorder.start_recording()

            # Update state
            self.is_recording = True
            self.is_paused = False

            # Update UI
            self.start_action.setEnabled(False)
            self.stop_action.setEnabled(True)
            self.pause_action.setEnabled(True)
            self.pause_action.setText("Pause Recording")
            self.region_action.setEnabled(False)

            # Switch to recording screen
            self.setCentralWidget(self.recording_screen)
            self.recording_screen.start_timer()

            # Minimize to tray if enabled
            if self.settings.get("minimize_on_record", False):
                self.hide()
                self.tray_icon.showMessage(
                    "Screen Recorder",
                    "Recording started and minimized to tray",
                    QSystemTrayIcon.Information,
                    2000
                )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start recording: {str(e)}")

    def stop_recording(self):
        """Stop the recording process."""
        output_file = None

        try:
            # Check if recording
            if not self.is_recording:
                return

            # Update state first to prevent race conditions
            self.is_recording = False
            self.is_paused = False

            # Update UI
            self.start_action.setEnabled(True)
            self.stop_action.setEnabled(False)
            self.pause_action.setEnabled(False)
            self.region_action.setEnabled(True)

            # Stop recording first
            output_file = self.screen_recorder.stop_recording()

            # Create a completely new home screen
            try:
                # Remove old home screen if it exists
                if hasattr(self, 'home_screen') and self.home_screen is not None:
                    try:
                        self.home_screen.deleteLater()
                    except:
                        pass

                # Create new home screen
                self.home_screen = HomeScreen(self)
                self.home_screen.start_recording_signal.connect(self.start_recording)

                # Switch to home screen
                self.setCentralWidget(self.home_screen)
            except Exception as e:
                import traceback
                print(f"Error creating new home screen: {e}")
                print(traceback.format_exc())

                # As a fallback, create a simple widget
                from PyQt5.QtWidgets import QLabel
                fallback_widget = QLabel("Recording completed. Please restart the application.")
                fallback_widget.setAlignment(Qt.AlignCenter)
                self.setCentralWidget(fallback_widget)

            # Add to recent recordings
            if output_file:
                self.settings.add_recent_recording(output_file)

            # Show window if hidden
            if not self.isVisible():
                self.show()
                self.activateWindow()

            # Show success message
            if output_file:
                QMessageBox.information(
                    self,
                    "Recording Complete",
                    f"Recording saved to:\n{output_file}"
                )

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to stop recording: {str(e)}\n\nDetails:\n{error_details}"
            )

            # Try to recover UI
            try:
                from PyQt5.QtWidgets import QLabel
                fallback_widget = QLabel("An error occurred. Please restart the application.")
                fallback_widget.setAlignment(Qt.AlignCenter)
                self.setCentralWidget(fallback_widget)
            except:
                pass

    def pause_recording(self):
        """Pause the recording process."""
        try:
            # Check if recording and not paused
            if not self.is_recording or self.is_paused:
                return

            # Pause recording
            self.screen_recorder.pause_recording()
            self.recording_screen.pause_timer()

            # Update state
            self.is_paused = True

            # Update UI
            self.pause_action.setText("Resume Recording")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to pause recording: {str(e)}")

    def resume_recording(self):
        """Resume the recording process."""
        try:
            # Check if recording and paused
            if not self.is_recording or not self.is_paused:
                return

            # Resume recording
            self.screen_recorder.resume_recording()
            self.recording_screen.resume_timer()

            # Update state
            self.is_paused = False

            # Update UI
            self.pause_action.setText("Pause Recording")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to resume recording: {str(e)}")

    def toggle_pause_resume(self):
        """Toggle between pause and resume states."""
        if self.is_paused:
            self.resume_recording()
        else:
            self.pause_recording()

    def toggle_start_stop(self):
        """Toggle between start and stop states."""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording_menu()

    def toggle_microphone(self, enabled):
        """Toggle microphone recording on/off.

        Args:
            enabled (bool): Whether to enable microphone recording
        """
        try:
            self.audio_manager.toggle_microphone(enabled)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to toggle microphone: {str(e)}")

    def toggle_system_audio(self, enabled):
        """Toggle system audio recording on/off.

        Args:
            enabled (bool): Whether to enable system audio recording
        """
        try:
            self.audio_manager.toggle_system_audio(enabled)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to toggle system audio: {str(e)}")

    def toggle_mic_hotkey(self):
        """Toggle microphone on/off via hotkey."""
        if self.is_recording:
            current_state = self.recording_screen.mic_button.isChecked()
            self.recording_screen.mic_button.setChecked(not current_state)
            self.toggle_microphone(not current_state)

    def toggle_system_hotkey(self):
        """Toggle system audio on/off via hotkey."""
        if self.is_recording:
            current_state = self.recording_screen.system_button.isChecked()
            self.recording_screen.system_button.setChecked(not current_state)
            self.toggle_system_audio(not current_state)

    def select_region(self):
        """Select a region of the screen to record."""
        # Hide main window temporarily
        self.hide()

        # Show region selector
        region = RegionSelector.get_region()

        # Show main window again
        self.show()

        # Set selected region
        if region is not None:
            self.selected_region = region
            self.settings.set("record_fullscreen", False)

    def show_settings(self):
        """Show the settings screen."""
        # Switch to settings screen
        self.setCentralWidget(self.settings_screen)

    def show_recordings_manager(self):
        """Show the recordings manager screen."""
        # Refresh recordings
        self.recordings_manager.load_recordings()

        # Switch to recordings manager screen
        self.setCentralWidget(self.recordings_manager)

    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About Screen Recorder",
            "Professional Screen Recorder\n\n"
            "A feature-rich screen recording application with audio support.\n\n"
            "Version: 1.0.0\n"
            "© 2025 Your Company"
        )

    def on_settings_saved(self):
        """Handle settings saved event."""
        try:
            # Update hotkey manager
            self.hotkey_manager.update_hotkeys()

            # Create a new home screen if needed
            try:
                # Remove old home screen if it exists
                if hasattr(self, 'home_screen') and self.home_screen is not None:
                    try:
                        self.home_screen.deleteLater()
                    except:
                        pass

                # Create new home screen
                self.home_screen = HomeScreen(self)
                self.home_screen.start_recording_signal.connect(self.start_recording)

                # Switch to home screen
                self.setCentralWidget(self.home_screen)
            except Exception as e:
                import traceback
                print(f"Error creating new home screen: {e}")
                print(traceback.format_exc())

                # As a fallback, create a simple widget
                from PyQt5.QtWidgets import QLabel
                fallback_widget = QLabel("Settings saved. Please restart the application.")
                fallback_widget.setAlignment(Qt.AlignCenter)
                self.setCentralWidget(fallback_widget)
        except Exception as e:
            import traceback
            print(f"Error in on_settings_saved: {e}")
            print(traceback.format_exc())

    def on_settings_canceled(self):
        """Handle settings canceled event."""
        try:
            # Create a new home screen if needed
            try:
                # Remove old home screen if it exists
                if hasattr(self, 'home_screen') and self.home_screen is not None:
                    try:
                        self.home_screen.deleteLater()
                    except:
                        pass

                # Create new home screen
                self.home_screen = HomeScreen(self)
                self.home_screen.start_recording_signal.connect(self.start_recording)

                # Switch to home screen
                self.setCentralWidget(self.home_screen)
            except Exception as e:
                import traceback
                print(f"Error creating new home screen: {e}")
                print(traceback.format_exc())

                # As a fallback, create a simple widget
                from PyQt5.QtWidgets import QLabel
                fallback_widget = QLabel("Settings canceled. Please restart the application.")
                fallback_widget.setAlignment(Qt.AlignCenter)
                self.setCentralWidget(fallback_widget)
        except Exception as e:
            import traceback
            print(f"Error in on_settings_canceled: {e}")
            print(traceback.format_exc())

    def closeEvent(self, event):
        """Handle window close event.

        Args:
            event (QCloseEvent): The close event
        """
        try:
            # Check if recording
            if self.is_recording:
                reply = QMessageBox.question(
                    self,
                    "Confirm Exit",
                    "Recording is in progress. Are you sure you want to exit?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )

                if reply == QMessageBox.No:
                    event.ignore()
                    return

                # Update state first
                self.is_recording = False
                self.is_paused = False

                # Stop recording directly without UI updates
                try:
                    # Set stop flag directly
                    self.screen_recorder.stop_requested = True

                    # Wait for recording thread with short timeout
                    if hasattr(self.screen_recorder, 'recording_thread') and self.screen_recorder.recording_thread and self.screen_recorder.recording_thread.is_alive():
                        self.screen_recorder.recording_thread.join(timeout=1.0)

                    # Stop audio recording
                    if hasattr(self.audio_manager, 'stop_requested'):
                        self.audio_manager.stop_requested = True
                except Exception as e:
                    print(f"Error stopping recording during close: {e}")

            # Hide tray icon
            if hasattr(self, 'tray_icon') and self.tray_icon is not None:
                try:
                    self.tray_icon.hide()
                except:
                    pass

            # Accept event
            event.accept()

        except Exception as e:
            import traceback
            print(f"Error in closeEvent: {e}")
            print(traceback.format_exc())
            event.accept()  # Always close the application

def main():
    """Main entry point for the application."""
    # Check if QApplication already exists
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Set application info
    app.setApplicationName("Professional Screen Recorder")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Your Company")
    app.setOrganizationDomain("yourcompany.com")

    # Create and show the main window
    window = ScreenRecorderApp()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
