"""
DeadlineDock
app/theme.py

Central design system for the application.
"""

from dataclasses import dataclass

# ---------- Color Tokens ----------

BACKGROUND = "#111111"
TEXT_PRIMARY = "#F5F5F7"
TEXT_SECONDARY = "#B8B8C2"
TEXT_MUTED = "#7D7D86"

ACCENT = "#5C8DFF"

SUCCESS = "#50D890"
WARNING = "#FFC857"
DANGER = "#FF5A5F"

GLASS_FILL = "rgba(255,255,255,0.08)"
GLASS_FILL_HOVER = "rgba(255,255,255,0.12)"
GLASS_BORDER = "rgba(255,255,255,0.10)"

DIVIDER = "rgba(255,255,255,0.08)"

# ---------- Typography ----------

FONT_FAMILY = "Segoe UI Variable"
FALLBACK_FONT = "Segoe UI"

TITLE_SIZE = 20
HEADER_SIZE = 14
BODY_SIZE = 12
CAPTION_SIZE = 10

# ---------- Spacing ----------

SPACE_2 = 2
SPACE_4 = 4
SPACE_8 = 8
SPACE_12 = 12
SPACE_16 = 16
SPACE_20 = 20
SPACE_24 = 24
SPACE_32 = 32

# ---------- Radius ----------

WINDOW_RADIUS = 18
CARD_RADIUS = 14
BUTTON_RADIUS = 10

# ---------- Animation ----------

FAST = 120
NORMAL = 180
SLOW = 260

# ---------- Shadows ----------

@dataclass(frozen=True)
class Shadow:
    blur: int
    x: int
    y: int
    alpha: int

CARD_SHADOW = Shadow(
    blur=24,
    x=0,
    y=8,
    alpha=28
)

HOVER_SHADOW = Shadow(
    blur=30,
    x=0,
    y=10,
    alpha=40
)

# ---------- QSS ----------

GLOBAL_QSS = f"""
QWidget {{
    color: {TEXT_PRIMARY};
    font-family: "{FONT_FAMILY}", "{FALLBACK_FONT}";
    font-size: {BODY_SIZE}px;
    background: transparent;
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 4px;
}}

QScrollBar::handle:vertical {{
    background: rgba(255,255,255,0.18);
    border-radius: 4px;
}}

QScrollBar::handle:vertical:hover {{
    background: rgba(255,255,255,0.28);
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QPushButton {{
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: {BUTTON_RADIUS}px;
    background: rgba(255,255,255,0.08);
    padding: 6px 10px;
}}

QPushButton:hover {{
    background: rgba(255,255,255,0.12);
}}

QPushButton:pressed {{
    background: rgba(255,255,255,0.16);
}}

QLineEdit,
QPlainTextEdit,
QTextEdit {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 8px;
}}

QLineEdit:focus,
QPlainTextEdit:focus,
QTextEdit:focus {{
    border: 1px solid {ACCENT};
}}
"""
