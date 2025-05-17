#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Region Selector Module
--------------------
Tool for selecting a region of the screen to record.
"""

import sys
from PyQt5.QtWidgets import (
    QWidget, QApplication, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QRubberBand
)
from PyQt5.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QCursor

class RegionSelector(QWidget):
    """Widget for selecting a region of the screen to record."""

    # Signal emitted when region is selected
    region_selected_signal = pyqtSignal(QRect)

    # Signal emitted when selection is canceled
    selection_canceled_signal = pyqtSignal()

    def __init__(self, parent=None):
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
        self.start_point = QPoint()
        self.end_point = QPoint()
        self.is_selecting = False
        self.selection_rect = QRect()
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        # Set up UI
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        # Set cursor to crosshair
        self.setCursor(Qt.CrossCursor)

        # Create info label
        self.info_label = QLabel("Click and drag to select a region. Press Esc to cancel.")
        self.info_label.setStyleSheet(
            "QLabel {"
            "    color: white;"
            "    background-color: rgba(0, 0, 0, 150);"
            "    padding: 5px;"
            "    border-radius: 5px;"
            "}"
        )
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Create buttons layout
        buttons_layout = QHBoxLayout()

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet(
            "QPushButton {"
            "    background-color: #f44336;"
            "    color: white;"
            "    border-radius: 5px;"
            "    padding: 5px 10px;"
            "}"
            "QPushButton:hover {"
            "    background-color: #d32f2f;"
            "}"
            "QPushButton:pressed {"
            "    background-color: #b71c1c;"
            "}"
        )
        self.cancel_button.clicked.connect(self.cancel_selection)

        # Select button
        self.select_button = QPushButton("Select")
        self.select_button.setStyleSheet(
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
        )
        self.select_button.clicked.connect(self.confirm_selection)

        # Add buttons to layout
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.select_button)

        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.info_label, 0, Qt.AlignTop | Qt.AlignHCenter)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout, 0)

        # Set layout
        self.setLayout(main_layout)

        # Hide buttons initially
        self.select_button.hide()
        self.cancel_button.hide()

    def show_fullscreen(self):
        """Show the widget in fullscreen mode."""
        # Get screen geometry
        screen_geometry = QApplication.desktop().screenGeometry()

        # Set widget geometry to cover the entire screen
        self.setGeometry(screen_geometry)

        # Show the widget
        self.showFullScreen()

    def paintEvent(self, event):
        """Paint the widget.

        Args:
            event (QPaintEvent): The paint event
        """
        painter = QPainter(self)

        # Draw semi-transparent background
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        # Draw selection rectangle if available
        if not self.selection_rect.isNull():
            # Clear the selected region
            painter.setBrush(Qt.NoBrush)
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.selection_rect)

            # Draw border around selected region
            painter.setPen(QPen(QColor(0, 120, 215), 2, Qt.SolidLine))
            painter.drawRect(self.selection_rect)

            # Draw size label
            size_text = f"{self.selection_rect.width()} x {self.selection_rect.height()}"
            painter.setPen(Qt.white)
            painter.drawText(
                self.selection_rect.x(),
                self.selection_rect.y() - 5,
                size_text
            )

    def mousePressEvent(self, event):
        """Handle mouse press events.

        Args:
            event (QMouseEvent): The mouse event
        """
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.is_selecting = True
            self.selection_rect = QRect()
            self.rubber_band.setGeometry(QRect(self.start_point, QSize()))
            self.rubber_band.show()

            # Hide buttons
            self.select_button.hide()
            self.cancel_button.hide()

            # Update
            self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse move events.

        Args:
            event (QMouseEvent): The mouse event
        """
        if self.is_selecting:
            self.end_point = event.pos()
            self.selection_rect = QRect(self.start_point, self.end_point).normalized()
            self.rubber_band.setGeometry(self.selection_rect)

            # Update
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events.

        Args:
            event (QMouseEvent): The mouse event
        """
        if event.button() == Qt.LeftButton and self.is_selecting:
            self.end_point = event.pos()
            self.is_selecting = False
            self.selection_rect = QRect(self.start_point, self.end_point).normalized()

            # Show buttons near the selection
            self._position_buttons()
            self.select_button.show()
            self.cancel_button.show()

            # Update
            self.update()

    def keyPressEvent(self, event):
        """Handle key press events.

        Args:
            event (QKeyEvent): The key event
        """
        if event.key() == Qt.Key_Escape:
            self.cancel_selection()

    def _position_buttons(self):
        """Position the buttons near the selection rectangle."""
        # Position buttons below the selection
        buttons_x = self.selection_rect.x() + self.selection_rect.width() - self.select_button.width() - self.cancel_button.width() - 10
        buttons_y = self.selection_rect.y() + self.selection_rect.height() + 10

        # Ensure buttons are visible
        if buttons_x < 0:
            buttons_x = 0
        if buttons_y + self.select_button.height() > self.height():
            buttons_y = self.selection_rect.y() - self.select_button.height() - 10

        # Position buttons
        self.layout().setAlignment(self.cancel_button, Qt.AlignBottom | Qt.AlignRight)
        self.layout().setAlignment(self.select_button, Qt.AlignBottom | Qt.AlignRight)

    def confirm_selection(self):
        """Confirm the selection and emit the region_selected signal."""
        if not self.selection_rect.isNull():
            self.region_selected_signal.emit(self.selection_rect)
            self.close()

    def cancel_selection(self):
        """Cancel the selection and emit the selection_canceled signal."""
        self.selection_canceled_signal.emit()
        self.close()

    @staticmethod
    def get_region(parent=None):
        """Static method to get a region selection.

        Args:
            parent (QWidget, optional): The parent widget

        Returns:
            QRect: The selected region, or None if canceled
        """
        selector = RegionSelector(parent)
        selector.show_fullscreen()

        # Create event loop
        from PyQt5.QtCore import QEventLoop
        loop = QEventLoop()

        # Selected region
        selected_region = [None]

        # Connect signals
        def on_region_selected(region):
            selected_region[0] = region
            loop.quit()

        def on_selection_canceled():
            loop.quit()

        selector.region_selected_signal.connect(on_region_selected)
        selector.selection_canceled_signal.connect(on_selection_canceled)

        # Start event loop
        loop.exec_()

        return selected_region[0]
