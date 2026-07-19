"""
DeadlineDock
app/models.py

Data models used throughout the application.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid


DATE_FORMAT = "%Y-%m-%d"


def parse_date(value):
    """
    Accepts either:
        datetime.date
        datetime.datetime
        'YYYY-MM-DD'
    """

    if isinstance(value, date):
        return value

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, str):
        return datetime.strptime(value, DATE_FORMAT).date()

    raise TypeError(f"Unsupported date type: {type(value)}")


@dataclass(order=True)
class Deadline:

    sort_index: date = field(init=False, repr=False)

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    title: str = ""

    due_date: date = field(default_factory=date.today)

    url: str = ""

    notes: str = ""

    completed: bool = False

    def __post_init__(self):

        self.due_date = parse_date(self.due_date)

        self.title = self.title.strip()

        self.url = self.url.strip()

        self.notes = self.notes.strip()

        self.sort_index = self.due_date

    # -----------------------------------------------------
    # Date Helpers
    # -----------------------------------------------------

    @property
    def days_remaining(self):

        return (self.due_date - date.today()).days

    @property
    def is_overdue(self):

        return self.days_remaining < 0

    @property
    def is_today(self):

        return self.days_remaining == 0

    @property
    def is_due_soon(self):

        return 0 < self.days_remaining <= 3

    # -----------------------------------------------------
    # UI Helpers
    # -----------------------------------------------------

    @property
    def status(self):

        if self.completed:
            return "completed"

        if self.is_overdue:
            return "overdue"

        if self.is_today:
            return "today"

        if self.is_due_soon:
            return "soon"

        return "future"

    @property
    def status_color(self):

        mapping = {
            "completed": "#808080",
            "overdue": "#FF5A5F",
            "today": "#FF8C42",
            "soon": "#FFC857",
            "future": "#50D890",
        }

        return mapping[self.status]

    @property
    def relative_text(self):

        d = self.days_remaining

        if d < 0:
            if d == -1:
                return "Yesterday"

            return f"{abs(d)} days ago"

        if d == 0:
            return "Today"

        if d == 1:
            return "Tomorrow"

        return f"In {d} days"

    @property
    def formatted_date(self):

        return self.due_date.strftime("%d %b")

    @property
    def full_date(self):

        return self.due_date.strftime("%d %B %Y")

    # -----------------------------------------------------
    # JSON
    # -----------------------------------------------------

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "due_date": self.due_date.strftime(DATE_FORMAT),
            "url": self.url,
            "notes": self.notes,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            title=data.get("title", ""),
            due_date=data.get("due_date", date.today()),
            url=data.get("url", ""),
            notes=data.get("notes", ""),
            completed=data.get("completed", False),
        )

    # -----------------------------------------------------

    def __str__(self):

        return f"{self.formatted_date} - {self.title}"

    def __repr__(self):

        return (
            f"Deadline("
            f"title={self.title!r}, "
            f"date={self.full_date!r})"
        )