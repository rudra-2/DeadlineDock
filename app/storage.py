"""
DeadlineDock Storage
--------------------
Local JSON persistence with atomic writes, CRUD, sorting,
and basic validation.
"""

import json
import os
from pathlib import Path
from typing import List, Optional    # <-- added Optional
from datetime import date

from app.config import DEADLINE_FILE, DEFAULT_JSON
from app.models import Deadline


class Storage:
    def __init__(self):
        self.path: Path = DEADLINE_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: dict = DEFAULT_JSON.copy()
        self.load()

    # --- core ---

    def load(self) -> None:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = DEFAULT_JSON.copy()
                self.save()
        else:
            self.save()

    def save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, self.path)
        except Exception:
            if tmp.exists():
                tmp.unlink(missing_ok=True)
            raise

    # --- CRUD ---

    def get_all(self) -> List[Deadline]:
        return [Deadline.from_dict(d) for d in self._data.get("deadlines", [])]

    def get_by_id(self, did: str) -> Optional[Deadline]:
        for d in self.get_all():
            if d.id == did:
                return d
        return None

    def add(self, deadline: Deadline) -> None:
        self._data["deadlines"].append(deadline.to_dict())
        self._sort_and_save()

    def update(self, deadline: Deadline) -> None:
        for i, d in enumerate(self._data["deadlines"]):
            if d["id"] == deadline.id:
                self._data["deadlines"][i] = deadline.to_dict()
                self._sort_and_save()
                return

    def delete(self, did: str) -> None:
        self._data["deadlines"] = [d for d in self._data["deadlines"] if d["id"] != did]
        self._sort_and_save()

    # --- sorting ---

    def _sort_and_save(self) -> None:
        deadlines = self.get_all()
        deadlines.sort(
            key=lambda d: (
                0 if d.pinned else 1,
                d.due_date_obj or date.max,
                d.title.lower(),
            )
        )
        self._data["deadlines"] = [d.to_dict() for d in deadlines]
        self.save()