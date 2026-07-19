"""
DeadlineDock TitleBar
---------------------
Draggable. App name left, controls right.
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent

from app.config import APP_NAME, TITLEBAR_HEIGHT, CONTENT_MARGIN
from ui.icon_button import IconButton, ICON_SETTINGS, ICON_PIN, ICON_PLUS
from ui.styles import titlebar_style


class TitleBar(QWidget):
    add_clicked = Signal()
    pin_clicked = Signal()
    settings_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(TITLEBAR_HEIGHT)
        self.setStyleSheet(titlebar_style())
        self._drag_pos = None
        self._pinned = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(CONTENT_MARGIN, 0, CONTENT_MARGIN, 0)
        layout.setSpacing(6)

        # App name
        self.title = QLabel(APP_NAME)
        self.title.setStyleSheet("font-weight: 600; font-size: 14px;")
        layout.addWidget(self.title)

        layout.addStretch()

        # Settings
        self.btn_settings = IconButton(ICON_SETTINGS)
        self.btn_settings.setToolTip("Settings")
        self.btn_settings.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(self.btn_settings)

        # Pin
        self.btn_pin = IconButton(ICON_PIN)
        self.btn_pin.setToolTip("Always on top")
        self.btn_pin.clicked.connect(self._toggle_pin)
        layout.addWidget(self.btn_pin)

        # Add
        self.btn_add = IconButton(ICON_PLUS)
        self.btn_add.setToolTip("Add deadline")
        self.btn_add.clicked.connect(self.add_clicked.emit)
        layout.addWidget(self.btn_add)

    def _toggle_pin(self):
        self._pinned = not self._pinned
        self.btn_pin.setStyleSheet(
            f"""
            QPushButton {{
                background: {'rgba(92,141,255,0.15)' if self._pinned else 'transparent'};
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: {'rgba(92,141,255,0.25)' if self._pinned else 'rgba(255,255,255,0.06)'};
            }}
            """
        )
        self.pin_clicked.emit()

    # --- drag support ---

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = None