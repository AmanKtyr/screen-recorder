#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Recordings Manager Module
-----------------------
Widget for managing and viewing recorded videos.
"""

import os
import sys
import subprocess
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QMenu,
    QFileDialog, QMessageBox, QAbstractItemView,
    QInputDialog, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont

class RecordingItem(QListWidgetItem):
    """List widget item for a recording."""

    def __init__(self, file_path, parent=None):
        super().__init__(parent)

        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

        # Get file info
        file_size = os.path.getsize(file_path)
        file_date = datetime.fromtimestamp(os.path.getmtime(file_path))

        # Format file size
        if file_size < 1024:
            size_str = f"{file_size} B"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.1f} KB"
        elif file_size < 1024 * 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{file_size / (1024 * 1024 * 1024):.1f} GB"

        # Format date
        date_str = file_date.strftime("%Y-%m-%d %H:%M:%S")

        # Set text
        self.setText(f"{self.file_name}\nSize: {size_str} | Date: {date_str}")

        # Set icon
        self.setIcon(QIcon.fromTheme("video-x-generic"))

        # Set size hint
        self.setSizeHint(QSize(0, 60))

class RecordingsManager(QWidget):
    """Widget for managing and viewing recorded videos."""

    def __init__(self, settings, parent=None):
        super().__init__(parent)

        self.settings = settings
        self.init_ui()
        self.load_recordings()

    def init_ui(self):
        """Initialize the user interface."""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title
        title_label = QLabel("Recordings Manager")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)

        # Add title to layout
        main_layout.addWidget(title_label)

        # Recordings list
        self.recordings_list = QListWidget()
        self.recordings_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.recordings_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.recordings_list.customContextMenuRequested.connect(self._show_context_menu)
        self.recordings_list.itemDoubleClicked.connect(self._play_recording)

        # Add recordings list to layout
        main_layout.addWidget(self.recordings_list)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_recordings)

        # Open folder button
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self._open_recordings_folder)

        # Play button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self._play_selected_recording)

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self._delete_selected_recording)

        # Add buttons to layout
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addWidget(self.open_folder_button)
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.delete_button)

        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)

        # Set main layout
        self.setLayout(main_layout)

    def load_recordings(self):
        """Load recordings from the output directory."""
        # Clear list
        self.recordings_list.clear()

        # Get output directory
        output_dir = self.settings.get("output_directory")

        # Check if directory exists
        if not os.path.exists(output_dir):
            return

        # Get all video files
        video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".wmv"]
        video_files = []

        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file)
                if ext.lower() in video_extensions:
                    video_files.append(file_path)

        # Sort by modification time (newest first)
        video_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Add to list
        for file_path in video_files:
            item = RecordingItem(file_path)
            self.recordings_list.addItem(item)

    def _show_context_menu(self, position):
        """Show context menu for recordings list.

        Args:
            position (QPoint): The position where the context menu should be shown
        """
        # Get selected item
        item = self.recordings_list.itemAt(position)

        if item is None:
            return

        # Create menu
        menu = QMenu()

        # Add actions
        play_action = menu.addAction("Play")
        open_folder_action = menu.addAction("Open Containing Folder")
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")

        # Show menu and get selected action
        action = menu.exec_(self.recordings_list.mapToGlobal(position))

        # Handle action
        if action == play_action:
            self._play_recording(item)
        elif action == open_folder_action:
            self._open_containing_folder(item)
        elif action == rename_action:
            self._rename_recording(item)
        elif action == delete_action:
            self._delete_recording(item)

    def _play_recording(self, item):
        """Play a recording.

        Args:
            item (RecordingItem): The recording item to play
        """
        # Get file path
        file_path = item.file_path

        # Open with default player
        if sys.platform == "win32":
            os.startfile(file_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", file_path])
        else:
            subprocess.call(["xdg-open", file_path])

    def _play_selected_recording(self):
        """Play the selected recording."""
        # Get selected item
        items = self.recordings_list.selectedItems()

        if not items:
            return

        # Play recording
        self._play_recording(items[0])

    def _open_containing_folder(self, item):
        """Open the folder containing a recording.

        Args:
            item (RecordingItem): The recording item
        """
        # Get file path
        file_path = item.file_path

        # Get directory
        directory = os.path.dirname(file_path)

        # Open directory
        if sys.platform == "win32":
            os.startfile(directory)
        elif sys.platform == "darwin":
            subprocess.call(["open", directory])
        else:
            subprocess.call(["xdg-open", directory])

    def _open_recordings_folder(self):
        """Open the recordings folder."""
        # Get output directory
        output_dir = self.settings.get("output_directory")

        # Check if directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Open directory
        if sys.platform == "win32":
            os.startfile(output_dir)
        elif sys.platform == "darwin":
            subprocess.call(["open", output_dir])
        else:
            subprocess.call(["xdg-open", output_dir])

    def _rename_recording(self, item):
        """Rename a recording.

        Args:
            item (RecordingItem): The recording item to rename
        """
        # Get file path
        file_path = item.file_path

        # Get directory and extension
        directory = os.path.dirname(file_path)
        _, ext = os.path.splitext(file_path)

        # Get new file name
        new_file_name, ok = QInputDialog.getText(
            self,
            "Rename Recording",
            "Enter new file name:",
            QLineEdit.Normal,
            item.file_name
        )

        if not ok or not new_file_name:
            return

        # Add extension if not present
        if not new_file_name.endswith(ext):
            new_file_name += ext

        # Create new file path
        new_file_path = os.path.join(directory, new_file_name)

        # Check if file already exists
        if os.path.exists(new_file_path):
            QMessageBox.warning(
                self,
                "File Exists",
                f"A file named '{new_file_name}' already exists."
            )
            return

        try:
            # Rename file
            os.rename(file_path, new_file_path)

            # Update item
            item.file_path = new_file_path
            item.file_name = new_file_name

            # Reload recordings
            self.load_recordings()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to rename file: {str(e)}"
            )

    def _delete_recording(self, item):
        """Delete a recording.

        Args:
            item (RecordingItem): The recording item to delete
        """
        # Get file path
        file_path = item.file_path

        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{item.file_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        try:
            # Delete file
            os.remove(file_path)

            # Remove item from list
            row = self.recordings_list.row(item)
            self.recordings_list.takeItem(row)

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to delete file: {str(e)}"
            )

    def _delete_selected_recording(self):
        """Delete the selected recording."""
        # Get selected item
        items = self.recordings_list.selectedItems()

        if not items:
            return

        # Delete recording
        self._delete_recording(items[0])
