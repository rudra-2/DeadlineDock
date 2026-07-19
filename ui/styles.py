"""
DeadlineDock
ui/styles.py

Shared Qt stylesheet helpers.
"""

from app.theme import (
    GLOBAL_QSS,
    WINDOW_RADIUS,
    GLASS_FILL,
    GLASS_BORDER,
)

WINDOW_QSS = f"""
QWidget#WindowRoot {{
    background:{GLASS_FILL};
    border:1px solid {GLASS_BORDER};
    border-radius:{WINDOW_RADIUS}px;
}}
"""

CARD_QSS = """
QFrame#DeadlineCard{
    background:rgba(255,255,255,0.08);
    border:1px solid rgba(255,255,255,0.10);
    border-radius:14px;
}
QFrame#DeadlineCard:hover{
    background:rgba(255,255,255,0.12);
}
"""

TITLEBAR_QSS = """
QWidget#TitleBar{
    background:transparent;
}
"""

def build_stylesheet()->str:
    return "\n".join([
        GLOBAL_QSS,
        WINDOW_QSS,
        CARD_QSS,
        TITLEBAR_QSS,
    ])
