"""
DeadlineDock DeadlineCard
-------------------------
Compact glass card with status rail, hover lift, and context menu.
"""

import webbrowser
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QMenu
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent, QColor, QCursor

from app.config import CARD_HEIGHT, CARD_RADIUS, CARD_SPACING, STATUS_RAIL_WIDTH, SMALL_SIZE
from app.models import Deadline
from app.utils import relative_date, format_absolute
from app.theme import STATUS_COLORS, GLASS_FILL, GLASS_FILL_HOVER, GLASS_BORDER, GLASS_BORDER_HOVER
from ui.styles import card_style, card_hover_style


class DeadlineCard(QWidget):
    clicked = Signal(Deadline)
    edit_requested = Signal(Deadline)
    delete_requested = Signal(str)

    def __init__(self, deadline: Deadline, parent=None):
        super().__init__(parent)
        self.deadline = deadline
        self.setObjectName("DeadlineCard")
        self.setFixedHeight(CARD_HEIGHT)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(card_style(deadline.status))

        # Shadow effect (subtle, shown on hover)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(0, 0, 0, 0))
        self.shadow.setOffset(0, 0)
        self.setGraphicsEffect(self.shadow)

        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 16, 0)
        layout.setSpacing(0)

        # Status rail
        self.rail = QWidget()
        self.rail.setFixedWidth(STATUS_RAIL_WIDTH)
        self.rail.setStyleSheet(
            f"background: {STATUS_COLORS.get(deadline.status, '#50D890')};"
            f"border-top-left-radius: {CARD_RADIUS}px;"
            f"border-bottom-left-radius: {CARD_RADIUS}px;"
        )
        layout.addWidget(self.rail)

        # Text content
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(14, 10, 0, 10)
        text_layout.setSpacing(2)

        # Top row: absolute date
        self.lbl_date = QLabel(format_absolute(deadline.due_date))
        self.lbl_date.setObjectName("CardDate")
        text_layout.addWidget(self.lbl_date)

        # Title
        self.lbl_title = QLabel(deadline.title)
        self.lbl_title.setObjectName("CardTitle")
        text_layout.addWidget(self.lbl_title)

        # Relative date
        self.lbl_relative = QLabel(relative_date(deadline.due_date))
        self.lbl_relative.setObjectName("CardRelative")
        text_layout.addWidget(self.lbl_relative)

        layout.addWidget(text_container, 1)

        # Completed indicator (if applicable)
        if deadline.completed:
            self.lbl_relative.setText("Completed")

    # --- interaction ---

    def enterEvent(self, event):
        self.setStyleSheet(card_hover_style(self.deadline.status))
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 40))
        self.shadow.setOffset(0, 4)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(card_style(self.deadline.status))
        self.shadow.setBlurRadius(0)
        self.shadow.setColor(QColor(0, 0, 0, 0))
        self.shadow.setOffset(0, 0)
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.deadline.url:
                webbrowser.open(self.deadline.url)
            else:
                self.clicked.emit(self.deadline)
        elif event.button() == Qt.RightButton:
            self._show_context_menu(event.globalPosition().toPoint())

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet(self.styleSheet())

        act_edit = menu.addAction("Edit")
        act_delete = menu.addAction("Delete")
        if self.deadline.url:
            act_copy = menu.addAction("Copy URL")

        action = menu.exec(QCursor.pos())
        if action == act_edit:
            self.edit_requested.emit(self.deadline)
        elif action == act_delete:
            self.delete_requested.emit(self.deadline.id)
        elif self.deadline.url and action == act_copy:
            from PySide6.QtWidgets import QApplication
            QApplication.clipboard().setText(self.deadline.url)