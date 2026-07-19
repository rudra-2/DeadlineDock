
"""
DeadlineDock
ui/add_dialog.py

Dialog used for creating and editing deadlines.
"""

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPlainTextEdit,
    QVBoxLayout,
)

from app.models import Deadline


class AddDialog(QDialog):
    def __init__(self, deadline: Deadline | None = None, parent=None):
        super().__init__(parent)

        self.deadline = deadline

        self.setWindowTitle("New Deadline" if deadline is None else "Edit Deadline")
        self.setModal(True)
        self.resize(420, 330)

        self._build_ui()
        self._apply_style()

        if deadline:
            self._load(deadline)

    def _build_ui(self):
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Honors Project Form")

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.today())

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://...")

        self.notes_edit = QPlainTextEdit()
        self.notes_edit.setPlaceholderText("Optional notes")
        self.notes_edit.setFixedHeight(90)

        form.addRow("Title", self.title_edit)
        form.addRow("Due Date", self.date_edit)
        form.addRow("URL", self.url_edit)
        form.addRow("Notes", self.notes_edit)

        layout.addLayout(form)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout.addWidget(self.buttons)

    def _apply_style(self):
        self.setStyleSheet("""
        QDialog{
            background:rgba(24,24,24,235);
            border:1px solid rgba(255,255,255,0.10);
            border-radius:18px;
        }

        QLabel{
            color:#F5F5F7;
        }

        QLineEdit,QPlainTextEdit,QDateEdit{
            background:rgba(255,255,255,0.06);
            border:1px solid rgba(255,255,255,0.10);
            border-radius:10px;
            padding:8px;
            color:white;
        }

        QPushButton{
            min-width:90px;
        }
        """)

    def _load(self, d: Deadline):
        self.title_edit.setText(d.title)
        self.date_edit.setDate(d.due_date)
        self.url_edit.setText(d.url)
        self.notes_edit.setPlainText(d.notes)

    def accept(self):
        if not self.title_edit.text().strip():
            QMessageBox.warning(
                self,
                "Missing Title",
                "Please enter a deadline title."
            )
            return

        super().accept()

    def get_deadline(self) -> Deadline:
        if self.deadline:
            d = self.deadline
        else:
            d = Deadline()

        d.title = self.title_edit.text().strip()
        d.url = self.url_edit.text().strip()
        d.notes = self.notes_edit.toPlainText().strip()
        d.due_date = self.date_edit.date().toPython()

        return d
