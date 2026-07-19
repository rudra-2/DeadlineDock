"""
DeadlineDock
app/utils.py

General helper functions used across the project.
"""

from __future__ import annotations

from datetime import date
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl


# -----------------------------------------
# Date Formatting
# -----------------------------------------

def pretty_date(d: date) -> str:
    return d.strftime("%d %b")


def long_date(d: date) -> str:
    return d.strftime("%d %B %Y")


# -----------------------------------------
# URL
# -----------------------------------------

def open_url(url: str):

    if not url:
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    QDesktopServices.openUrl(QUrl(url))


# -----------------------------------------
# Clamp
# -----------------------------------------

def clamp(value, minimum, maximum):

    return max(minimum, min(maximum, value))


# -----------------------------------------
# Status Dot
# -----------------------------------------

def status_color(days_remaining):

    if days_remaining < 0:
        return "#FF5A5F"

    if days_remaining == 0:
        return "#FF8C42"

    if days_remaining <= 3:
        return "#FFC857"

    return "#50D890"


# -----------------------------------------
# Relative Time
# -----------------------------------------

def relative_time(target: date):

    delta = (target - date.today()).days

    if delta == 0:
        return "Today"

    if delta == 1:
        return "Tomorrow"

    if delta == -1:
        return "Yesterday"

    if delta > 1:
        return f"In {delta} days"

    return f"{abs(delta)} days ago"


# -----------------------------------------
# Text
# -----------------------------------------

def ellipsis(text: str, length=38):

    if len(text) <= length:
        return text

    return text[:length - 1] + "…"


# -----------------------------------------
# Shadow Strength
# -----------------------------------------

def shadow_alpha(hover=False):

    return 40 if hover else 22