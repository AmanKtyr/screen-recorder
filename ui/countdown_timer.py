#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Countdown Timer Module
--------------------
Widget for displaying a countdown before recording starts.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPainter

class CountdownTimer(QWidget):
    """Widget for displaying a countdown before recording starts."""

    # Signal emitted when countdown is complete
    countdown_complete_signal = pyqtSignal()

    def __init__(self, seconds=3, parent=None):
        super().__init__(parent)

        # Set window flags
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        # Set window to be translucent
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Initialize variables
        self.seconds = seconds
        self.current_second = seconds
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self._update_countdown)

        # Set up UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Create countdown label
        self.countdown_label = QLabel(str(self.current_second))
        self.countdown_label.setAlignment(Qt.AlignCenter)

        # Set font
        font = QFont()
        font.setPointSize(100)
        font.setBold(True)
        self.countdown_label.setFont(font)

        # Set style
        self.countdown_label.setStyleSheet(
            "QLabel {"
            "    color: white;"
            "    background-color: transparent;"
            "}"
        )

        # Add label to layout
        layout.addWidget(self.countdown_label)

        # Set layout
        self.setLayout(layout)

        # Set size
        self.setFixedSize(200, 200)

    def paintEvent(self, event):
        """Paint the widget.

        Args:
            event (QPaintEvent): The paint event
        """
        painter = QPainter(self)

        # Enable anti-aliasing
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw semi-transparent circle
        painter.setBrush(QColor(0, 0, 0, 150))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())

    def start_countdown(self):
        """Start the countdown timer."""
        # Reset countdown
        self.current_second = self.seconds
        self.countdown_label.setText(str(self.current_second))

        # Start timer
        self.timer.start()

    def _update_countdown(self):
        """Update the countdown timer."""
        # Decrement counter
        self.current_second -= 1

        # Update label
        self.countdown_label.setText(str(self.current_second))

        # Check if countdown is complete
        if self.current_second <= 0:
            self.timer.stop()
            self.countdown_complete_signal.emit()
            self.close()

    def center_on_screen(self):
        """Center the widget on the screen."""
        from PyQt5.QtWidgets import QApplication

        # Get screen geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Calculate center position
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Move widget to center
        self.move(x, y)

    @staticmethod
    def countdown(seconds=3, parent=None):
        """Static method to show a countdown.

        Args:
            seconds (int, optional): The number of seconds to count down
            parent (QWidget, optional): The parent widget
        """
        from PyQt5.QtWidgets import QApplication

        # Create countdown timer
        countdown = CountdownTimer(seconds, parent)
        countdown.center_on_screen()
        countdown.show()

        # Create event loop
        from PyQt5.QtCore import QEventLoop
        loop = QEventLoop()

        # Connect signal
        countdown.countdown_complete_signal.connect(loop.quit)

        # Start countdown
        countdown.start_countdown()

        # Start event loop
        loop.exec_()
