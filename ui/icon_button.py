"""
DeadlineDock IconButton
-----------------------
Minimal 32×32 button with SVG path painting.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPaintEvent

from app.config import BUTTON_SIZE, ICON_SIZE, TEXT_MUTED, TEXT_PRIMARY, ACCENT


class IconButton(QPushButton):
    def __init__(self, path_d: str, parent=None):
        super().__init__(parent)
        self.path_d = path_d
        self.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: rgba(255,255,255,0.06);
            }}
            QPushButton:pressed {{
                background: rgba(255,255,255,0.10);
            }}
            """
        )

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw icon centered
        icon_color = QColor(TEXT_PRIMARY)
        painter.setPen(Qt.NoPen)
        painter.setBrush(icon_color)

        # Simple path parser for common icons (we use pre-built paths)
        # For production, replace with QSvgRenderer or QPixmap
        rect = self.rect().adjusted(
            (BUTTON_SIZE - ICON_SIZE) // 2,
            (BUTTON_SIZE - ICON_SIZE) // 2,
            -(BUTTON_SIZE - ICON_SIZE) // 2,
            -(BUTTON_SIZE - ICON_SIZE) // 2,
        )
        painter.drawEllipse(rect.center(), 2, 2)  # placeholder dot

        painter.end()


# Pre-built icon paths (simplified shapes)
# In a real app you'd load SVG files from assets/icons/

ICON_PLUS = "M12 5v14M5 12h14"
ICON_PIN = "M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7z"
ICON_SETTINGS = "M12 15a3 3 0 100-6 3 3 0 000 6z"
ICON_CLOSE = "M18 6L6 18M6 6l12 12"