"""
DeadlineDock Utils
------------------
Relative date formatting and status helpers.
"""

from datetime import date


def relative_date(due_date_str: str) -> str:
    """Human-friendly relative date string."""
    try:
        due = date.fromisoformat(due_date_str)
    except Exception:
        return "Invalid date"

    today = date.today()
    delta = (due - today).days

    if delta < -1:
        return f"Overdue by {abs(delta)} days"
    if delta == -1:
        return "Yesterday"
    if delta == 0:
        return "Today"
    if delta == 1:
        return "Tomorrow"
    if delta < 7:
        return f"In {delta} days"
    if delta < 30:
        weeks = delta // 7
        return f"In {weeks} week{'s' if weeks > 1 else ''}"
    return due.strftime("%d %b")


def format_absolute(due_date_str: str) -> str:
    """e.g. '21 Jul'"""
    try:
        return date.fromisoformat(due_date_str).strftime("%d %b")
    except Exception:
        return ""