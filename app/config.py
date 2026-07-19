"""
DeadlineDock Configuration
--------------------------
Global configuration, theme values and application constants.
"""

from pathlib import Path

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

ASSETS = ROOT / "assets"
ICONS = ASSETS / "icons"
FONTS = ASSETS / "fonts"

DATA = ROOT / "data"
DEADLINE_FILE = DATA / "deadlines.json"

# --------------------------------------------------
# Window
# --------------------------------------------------

APP_NAME = "DeadlineDock"

WINDOW_WIDTH = 430
WINDOW_HEIGHT = 620

MIN_WIDTH = 360
MIN_HEIGHT = 420

CORNER_RADIUS = 18

CONTENT_MARGIN = 18

# --------------------------------------------------
# Typography
# --------------------------------------------------

FONT_FAMILY = "Segoe UI Variable"
FONT_FALLBACK = "Segoe UI"

TITLE_SIZE = 20
HEADER_SIZE = 14
BODY_SIZE = 12
SMALL_SIZE = 10

# --------------------------------------------------
# Colors  (adaptive — content overlay handles readability)
# --------------------------------------------------

BACKGROUND = "#111111"

TEXT_PRIMARY = "#F5F5F7"
TEXT_SECONDARY = "#B8B8C2"
TEXT_MUTED = "#7D7D86"

ACCENT = "#5C8DFF"

SUCCESS = "#50D890"
WARNING = "#FFC857"
DANGER = "#FF5A5F"

# Glass surfaces
GLASS_FILL = "rgba(255,255,255,0.05)"
GLASS_FILL_HOVER = "rgba(255,255,255,0.09)"
GLASS_BORDER = "rgba(255,255,255,0.08)"
GLASS_BORDER_HOVER = "rgba(255,255,255,0.14)"

# Content overlay — dark enough for white text on any wallpaper
CONTENT_OVERLAY = "rgba(16,16,16,0.78)"
CONTENT_OVERLAY_SOLID = "#141414"

DIVIDER = "rgba(255,255,255,0.06)"

# --------------------------------------------------
# Card
# --------------------------------------------------

CARD_HEIGHT = 72
CARD_RADIUS = 12
CARD_SPACING = 8
STATUS_RAIL_WIDTH = 3

# --------------------------------------------------
# Title Bar
# --------------------------------------------------

TITLEBAR_HEIGHT = 44
ICON_SIZE = 18
BUTTON_SIZE = 32

# --------------------------------------------------
# Deadline Rules
# --------------------------------------------------

SOON_DAYS = 3

# --------------------------------------------------
# Animation
# --------------------------------------------------

CARD_FADE_MS = 160
CARD_SLIDE_DISTANCE = 10
BUTTON_HOVER_MS = 100
WINDOW_FADE_MS = 160
DIALOG_SLIDE_MS = 180

# --------------------------------------------------
# JSON
# --------------------------------------------------

DEFAULT_JSON = {"deadlines": []}