"""
DeadlineDock Theme
------------------
Color tokens and global QSS. Kept minimal and typography-first.
"""

from app.config import *

# ------------------------------------------------------------------
# Token palette
# ------------------------------------------------------------------

TOKENS = {
    "bg": BACKGROUND,
    "text": TEXT_PRIMARY,
    "text_secondary": TEXT_SECONDARY,
    "text_muted": TEXT_MUTED,
    "accent": ACCENT,
    "danger": DANGER,
    "warning": WARNING,
    "success": SUCCESS,
    "glass": GLASS_FILL,
    "glass_hover": GLASS_FILL_HOVER,
    "border": GLASS_BORDER,
    "border_hover": GLASS_BORDER_HOVER,
    "overlay": CONTENT_OVERLAY,
    "overlay_solid": CONTENT_OVERLAY_SOLID,
    "divider": DIVIDER,
}

STATUS_COLORS = {
    "overdue": DANGER,
    "today": "#FFB84D",
    "soon": WARNING,
    "future": SUCCESS,
    "completed": TEXT_MUTED,
    "unknown": TEXT_MUTED,
}

# ------------------------------------------------------------------
# Global QSS
# ------------------------------------------------------------------

GLOBAL_QSS = f"""
QWidget {{
    font-family: "{FONT_FAMILY}", "{FONT_FALLBACK}", sans-serif;
    color: {TEXT_PRIMARY};
    outline: none;
}}

QLineEdit, QTextEdit {{
    background: rgba(255,255,255,0.05);
    border: 1px solid {GLASS_BORDER};
    border-radius: 10px;
    padding: 10px 12px;
    font-size: {BODY_SIZE}px;
    color: {TEXT_PRIMARY};
    selection-background-color: {ACCENT};
}}

QLineEdit:focus, QTextEdit:focus {{
    border: 1px solid {ACCENT};
}}

QLineEdit::placeholder,
QTextEdit::placeholder {{
    color: {TEXT_MUTED};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 5px;
    border-radius: 2px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.12);
    border-radius: 2px;
    min-height: 40px;
}}

QScrollBar::handle:vertical:hover {{
    background: rgba(255,255,255,0.22);
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QMenu {{
    background: {CONTENT_OVERLAY_SOLID};
    border: 1px solid {GLASS_BORDER};
    border-radius: 10px;
    padding: 6px;
}}

QMenu::item {{
    padding: 8px 18px;
    border-radius: 6px;
    font-size: {BODY_SIZE}px;
}}

QMenu::item:selected {{
    background: {GLASS_FILL_HOVER};
}}

QMenu::separator {{
    height: 1px;
    background: {DIVIDER};
    margin: 4px 10px;
}}
"""