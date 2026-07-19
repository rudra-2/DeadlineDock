"""
DeadlineDock
ui/icon_button.py

Minimal glass icon button used throughout the app.
"""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from app.animations import press, restore
from app.theme import BUTTON_RADIUS


class IconButton(QPushButton):
    def __init__(self, icon_path:str="", tooltip:str="", parent=None):
        super().__init__(parent)

        self.setFixedSize(32, 32)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)

        if icon_path:
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(16,16))

        if tooltip:
            self.setToolTip(tooltip)

        self._original_geometry = None

        self.setStyleSheet(f"""
        QPushButton {{
            background: rgba(255,255,255,0.08);
            border:1px solid rgba(255,255,255,0.10);
            border-radius:{BUTTON_RADIUS}px;
        }}

        QPushButton:hover {{
            background: rgba(255,255,255,0.14);
            border:1px solid rgba(255,255,255,0.16);
        }}

        QPushButton:pressed {{
            background: rgba(255,255,255,0.18);
        }}

        QPushButton:focus {{
            border:1px solid #5C8DFF;
        }}
        """)

    def mousePressEvent(self, event):
        self._original_geometry = self.geometry()
        press(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self._original_geometry is not None:
            restore(self, self._original_geometry)
        super().mouseReleaseEvent(event)
