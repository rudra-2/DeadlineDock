"""
DeadlineDock AddDialog
----------------------
Compact floating sheet. Enter saves, Esc closes.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QKeyEvent

from app.config import WINDOW_WIDTH, CONTENT_MARGIN, DIALOG_SLIDE_MS
from app.models import Deadline
from app.animations import SlideAnimation
from ui.styles import dialog_style


class AddDialog(QDialog):
    deadline_saved = Signal(Deadline)

    def __init__(self, parent=None, edit_deadline: Deadline = None):
        super().__init__(parent)
        self.edit_mode = edit_deadline is not None
        self.deadline = edit_deadline or Deadline()

        self.setObjectName("AddDialog")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(WINDOW_WIDTH - 40, 420)

        # Position centered over parent
        if parent:
            geo = self.geometry()
            parent_geo = parent.geometry()
            x = parent_geo.x() + (parent_geo.width() - geo.width()) // 2
            y = parent_geo.y() + (parent_geo.height() - geo.height()) // 2
            self.move(x, y)

        self.setStyleSheet(dialog_style())

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(CONTENT_MARGIN, 20, CONTENT_MARGIN, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel("Edit Deadline" if self.edit_mode else "New Deadline")
        title.setObjectName("DialogTitle")
        layout.addWidget(title)

        # Title field
        layout.addWidget(self._label("Title"))
        self.inp_title = QLineEdit()
        self.inp_title.setText(self.deadline.title)
        self.inp_title.setPlaceholderText("e.g. Honors Project Form")
        layout.addWidget(self.inp_title)

        # Date field
        layout.addWidget(self._label("Due Date"))
        self.inp_date = QLineEdit()
        self.inp_date.setText(self.deadline.due_date)
        self.inp_date.setPlaceholderText("YYYY-MM-DD")
        layout.addWidget(self.inp_date)

        # URL field
        layout.addWidget(self._label("URL (optional)"))
        self.inp_url = QLineEdit()
        self.inp_url.setText(self.deadline.url)
        self.inp_url.setPlaceholderText("https://...")
        layout.addWidget(self.inp_url)

        # Notes field
        layout.addWidget(self._label("Notes (optional)"))
        self.inp_notes = QTextEdit()
        self.inp_notes.setText(self.deadline.notes)
        self.inp_notes.setPlaceholderText("Any extra details...")
        self.inp_notes.setMaximumHeight(80)
        layout.addWidget(self.inp_notes)

        layout.addStretch()

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("CancelButton")
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("SaveButton")
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self._save)

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_save)
        layout.addLayout(btn_row)

        # Focus title
        QTimer.singleShot(50, self.inp_title.setFocus)

        # Entry animation
        self.slide = SlideAnimation(self, distance=12, duration_ms=DIALOG_SLIDE_MS)
        QTimer.singleShot(10, self.slide.slide_in_from_top)

    def _label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")
        return lbl

    def _save(self):
        title = self.inp_title.text().strip()
        date_str = self.inp_date.text().strip()
        if not title or not date_str:
            return

        self.deadline.title = title
        self.deadline.due_date = date_str
        self.deadline.url = self.inp_url.text().strip()
        self.deadline.notes = self.inp_notes.toPlainText().strip()

        self.deadline_saved.emit(self.deadline)
        self.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)