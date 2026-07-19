
"""
DeadlineDock
ui/titlebar.py

Custom title bar for the frameless window.
"""

from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QSizePolicy,
)

from ui.icon_button import IconButton
from app.config import TITLEBAR_HEIGHT, APP_NAME


class TitleBar(QWidget):
    """
    Custom title bar.

    Signals
    -------
    addClicked
    settingsClicked
    pinClicked
    """

    addClicked = Signal()
    settingsClicked = Signal()
    pinClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._window = parent
        self._drag_pos = QPoint()
        self._dragging = False

        self.setFixedHeight(TITLEBAR_HEIGHT)
        self.setObjectName("TitleBar")

        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(8)

        self.title = QLabel(APP_NAME)
        font = QFont("Segoe UI Variable", 11)
        font.setBold(True)
        self.title.setFont(font)

        self.title.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        # Icons should be placed in assets/icons
        self.pin_btn = IconButton(
            "assets/icons/pin.svg",
            "Pin on top"
        )

        self.settings_btn = IconButton(
            "assets/icons/settings.svg",
            "Settings"
        )

        self.add_btn = IconButton(
            "assets/icons/plus.svg",
            "Add deadline"
        )

        self.pin_btn.clicked.connect(self.pinClicked.emit)
        self.settings_btn.clicked.connect(
            self.settingsClicked.emit
        )
        self.add_btn.clicked.connect(
            self.addClicked.emit
        )

        layout.addWidget(self.title)
        layout.addWidget(self.pin_btn)
        layout.addWidget(self.settings_btn)
        layout.addWidget(self.add_btn)

    def _apply_style(self):
        self.setStyleSheet("""
        QWidget#TitleBar{
            background: transparent;
        }

        QLabel{
            color:#F5F5F7;
            background:transparent;
        }
        """)

    # -------------------------
    # Drag window
    # -------------------------

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_pos = (
                event.globalPosition().toPoint()
                - self.window().frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.window().move(
                event.globalPosition().toPoint()
                - self._drag_pos
            )
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        # Reserved for compact mode in future
        event.accept()
