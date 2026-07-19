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

ANIMATION_DURATION = 220

FPS = 60

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
# Glass Surface
# --------------------------------------------------

SURFACE_OPACITY = 0.62

CARD_OPACITY = 0.16

CARD_HOVER_OPACITY = 0.22

BORDER_OPACITY = 0.12

SHADOW_BLUR = 30

# --------------------------------------------------
# Colors
# --------------------------------------------------

BACKGROUND = "#111111"

TEXT_PRIMARY = "#F5F5F7"
TEXT_SECONDARY = "#B8B8C2"
TEXT_MUTED = "#7D7D86"

ACCENT = "#5C8DFF"

SUCCESS = "#50D890"

WARNING = "#FFB84D"

DANGER = "#FF5A5F"

CARD_BORDER = "rgba(255,255,255,0.10)"

CARD_FILL = "rgba(255,255,255,0.08)"

CARD_FILL_HOVER = "rgba(255,255,255,0.12)"

DIVIDER = "rgba(255,255,255,0.08)"

# --------------------------------------------------
# Card
# --------------------------------------------------

CARD_HEIGHT = 78

CARD_RADIUS = 14

CARD_SPACING = 10

STATUS_DOT = 10

# --------------------------------------------------
# Title Bar
# --------------------------------------------------

TITLEBAR_HEIGHT = 46

ICON_SIZE = 18

BUTTON_SIZE = 32

# --------------------------------------------------
# Deadline Rules
# --------------------------------------------------

OVERDUE_DAYS = 0

SOON_DAYS = 3

# --------------------------------------------------
# Startup Defaults
# --------------------------------------------------

START_ALWAYS_ON_TOP = True

START_CLICK_THROUGH = False

START_WITH_WINDOWS = False

MINIMIZE_TO_TRAY = True

# --------------------------------------------------
# Animation
# --------------------------------------------------

CARD_FADE_MS = 180

CARD_SLIDE_DISTANCE = 12

BUTTON_HOVER_MS = 120

WINDOW_FADE_MS = 180

# --------------------------------------------------
# JSON
# --------------------------------------------------

DEFAULT_JSON = {
    "deadlines": []
}