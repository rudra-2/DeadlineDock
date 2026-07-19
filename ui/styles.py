"""
DeadlineDock Styles
-------------------
Centralized widget-specific QSS generators.
"""

from app.config import *
from app.theme import TOKENS, STATUS_COLORS


def titlebar_style() -> str:
    return f"""
    QWidget {{
        background: transparent;
        border: none;
    }}
    QLabel {{
        color: {TEXT_PRIMARY};
        font-size: {HEADER_SIZE}px;
        font-weight: 600;
    }}
    """


def card_style(status: str = "future") -> str:
    color = STATUS_COLORS.get(status, SUCCESS)
    return f"""
    QWidget#DeadlineCard {{
        background: {GLASS_FILL};
        border: 1px solid {GLASS_BORDER};
        border-radius: {CARD_RADIUS}px;
    }}
    QLabel#CardDate {{
        color: {TEXT_MUTED};
        font-size: {SMALL_SIZE}px;
    }}
    QLabel#CardTitle {{
        color: {TEXT_PRIMARY};
        font-size: {BODY_SIZE}px;
        font-weight: 600;
    }}
    QLabel#CardRelative {{
        color: {color};
        font-size: {SMALL_SIZE}px;
        font-weight: 500;
    }}
    """


def card_hover_style(status: str = "future") -> str:
    color = STATUS_COLORS.get(status, SUCCESS)
    return f"""
    QWidget#DeadlineCard {{
        background: {GLASS_FILL_HOVER};
        border: 1px solid {GLASS_BORDER_HOVER};
        border-radius: {CARD_RADIUS}px;
    }}
    QLabel#CardDate {{
        color: {TEXT_SECONDARY};
        font-size: {SMALL_SIZE}px;
    }}
    QLabel#CardTitle {{
        color: {TEXT_PRIMARY};
        font-size: {BODY_SIZE}px;
        font-weight: 600;
    }}
    QLabel#CardRelative {{
        color: {color};
        font-size: {SMALL_SIZE}px;
        font-weight: 500;
    }}
    """


def dialog_style() -> str:
    return f"""
    QWidget#AddDialog {{
        background: {CONTENT_OVERLAY_SOLID};
        border: 1px solid {GLASS_BORDER};
        border-radius: 16px;
    }}
    QLabel#DialogTitle {{
        color: {TEXT_PRIMARY};
        font-size: {HEADER_SIZE}px;
        font-weight: 600;
    }}
    QLabel#FieldLabel {{
        color: {TEXT_SECONDARY};
        font-size: {SMALL_SIZE}px;
        font-weight: 500;
        margin-bottom: 4px;
    }}
    QPushButton#SaveButton {{
        background: {ACCENT};
        color: #ffffff;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: {BODY_SIZE}px;
        font-weight: 600;
    }}
    QPushButton#SaveButton:hover {{
        background: #4a7de0;
    }}
    QPushButton#CancelButton {{
        background: transparent;
        color: {TEXT_SECONDARY};
        border: 1px solid {GLASS_BORDER};
        border-radius: 10px;
        padding: 10px 20px;
        font-size: {BODY_SIZE}px;
        font-weight: 500;
    }}
    QPushButton#CancelButton:hover {{
        background: {GLASS_FILL_HOVER};
        color: {TEXT_PRIMARY};
    }}
    """