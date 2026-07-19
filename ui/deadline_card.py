
"""
DeadlineDock
ui/deadline_card.py

A minimalist glassmorphism deadline card.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from app.models import Deadline
from app.utils import open_url


class DeadlineCard(QFrame):
    clicked = Signal(object)
    deleteRequested = Signal(str)
    editRequested = Signal(object)

    def __init__(self, deadline: Deadline, parent=None):
        super().__init__(parent)

        self.deadline = deadline

        self.setObjectName("DeadlineCard")
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(78)

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)

        self.status = QWidget()
        self.status.setFixedWidth(4)
        self.status.setObjectName("StatusBar")

        root.addWidget(self.status)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.dateLabel = QLabel()
        self.dateLabel.setObjectName("Date")

        self.titleLabel = QLabel()
        self.titleLabel.setObjectName("Title")

        self.relativeLabel = QLabel()
        self.relativeLabel.setObjectName("Relative")

        text_layout.addWidget(self.dateLabel)
        text_layout.addWidget(self.titleLabel)
        text_layout.addWidget(self.relativeLabel)

        root.addLayout(text_layout, 1)

        self.setStyleSheet("""
        QFrame#DeadlineCard{
            background:rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.10);
            border-radius:14px;
        }

        QWidget#StatusBar{
            border-radius:2px;
        }

        QLabel#Date{
            color:#B8B8C2;
            font-size:11px;
        }

        QLabel#Title{
            color:#F5F5F7;
            font-size:14px;
            font-weight:600;
        }

        QLabel#Relative{
            color:#7D7D86;
            font-size:10px;
        }
        """)

    def refresh(self):
        self.dateLabel.setText(self.deadline.formatted_date)
        self.titleLabel.setText(self.deadline.title)
        self.relativeLabel.setText(self.deadline.relative_text)
        self.status.setStyleSheet(
            f"background:{self.deadline.status_color};border-radius:2px;"
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.deadline)
            if self.deadline.url:
                open_url(self.deadline.url)
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        from PySide6.QtWidgets import QMenu

        menu = QMenu(self)

        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")

        chosen = menu.exec(event.globalPos())

        if chosen == edit_action:
            self.editRequested.emit(self.deadline)

        elif chosen == delete_action:
            self.deleteRequested.emit(self.deadline.id)
