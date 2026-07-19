
"""
DeadlineDock
ui/window.py

Main application window.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QMessageBox,
)

from app.storage import Storage
from ui.titlebar import TitleBar
from ui.deadline_card import DeadlineCard
from ui.add_dialog import AddDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.storage = Storage()

        self.setWindowTitle("DeadlineDock")
        self.resize(430, 620)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self._build_ui()
        self.load_deadlines()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.titlebar = TitleBar(self)
        self.titlebar.addClicked.connect(self.add_deadline)

        layout.addWidget(self.titlebar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0,0,0,0)
        self.list_layout.setSpacing(10)
        self.list_layout.addStretch()

        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

    def clear_cards(self):
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def load_deadlines(self):
        self.clear_cards()

        deadlines = self.storage.get_all()

        for deadline in deadlines:
            card = DeadlineCard(deadline)

            card.deleteRequested.connect(self.delete_deadline)
            card.editRequested.connect(self.edit_deadline)

            self.list_layout.insertWidget(
                self.list_layout.count()-1,
                card
            )

    def add_deadline(self):
        dialog = AddDialog(parent=self)

        if dialog.exec():
            self.storage.add(dialog.get_deadline())
            self.load_deadlines()

    def edit_deadline(self, deadline):
        dialog = AddDialog(deadline, self)

        if dialog.exec():
            self.storage.update(dialog.get_deadline())
            self.load_deadlines()

    def delete_deadline(self, deadline_id):
        ans = QMessageBox.question(
            self,
            "Delete",
            "Delete this deadline?"
        )

        if ans == QMessageBox.StandardButton.Yes:
            self.storage.delete(deadline_id)
            self.load_deadlines()
