"""
DeadlineDock Models
-------------------
Deadline dataclass with automatic UUID, sorting helpers,
and relative date generation.
"""

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional
import uuid


@dataclass
class Deadline:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    due_date: str = ""          # ISO-8601  YYYY-MM-DD
    url: str = ""
    notes: str = ""
    completed: bool = False
    pinned: bool = False

    # --- derived ---

    @property
    def due_date_obj(self) -> Optional[date]:
        try:
            return date.fromisoformat(self.due_date)
        except Exception:
            return None

    @property
    def days_remaining(self) -> Optional[int]:
        d = self.due_date_obj
        if d is None:
            return None
        return (d - date.today()).days

    @property
    def status(self) -> str:
        if self.completed:
            return "completed"
        days = self.days_remaining
        if days is None:
            return "unknown"
        if days < 0:
            return "overdue"
        if days == 0:
            return "today"
        if days <= 3:
            return "soon"
        return "future"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Deadline":
        # Filter unknown keys for forward compatibility
        known = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in known}
        return cls(**filtered)