"""
DeadlineDock
app/storage.py

Handles loading/saving deadlines from JSON.

Features
--------
✔ Auto-create data folder
✔ Auto-create deadlines.json
✔ Atomic saving
✔ Validation
✔ Sorted loading
✔ CRUD helpers
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from app.models import Deadline
from app.config import (
    DATA,
    DEADLINE_FILE,
    DEFAULT_JSON,
)


class Storage:

    def __init__(self):

        self.file = Path(DEADLINE_FILE)

        self._ensure_data_directory()

        self._ensure_json_file()

    # ----------------------------------------------------
    # Setup
    # ----------------------------------------------------

    def _ensure_data_directory(self):

        DATA.mkdir(parents=True, exist_ok=True)

    def _ensure_json_file(self):

        if self.file.exists():
            return

        with open(self.file, "w", encoding="utf-8") as f:

            json.dump(
                DEFAULT_JSON,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # ----------------------------------------------------
    # Load
    # ----------------------------------------------------

    def load(self):

        with open(
            self.file,
            "r",
            encoding="utf-8",
        ) as f:

            raw = json.load(f)

        deadlines = []

        for item in raw.get("deadlines", []):

            try:

                deadlines.append(
                    Deadline.from_dict(item)
                )

            except Exception as e:

                print("Skipped invalid deadline:", e)

        deadlines.sort()

        return deadlines

    # ----------------------------------------------------
    # Save
    # ----------------------------------------------------

    def save(self, deadlines):

        deadlines = sorted(deadlines)

        payload = {
            "deadlines": [
                d.to_dict()
                for d in deadlines
            ]
        }

        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".json",
            mode="w",
            encoding="utf-8",
        )

        json.dump(
            payload,
            tmp,
            indent=4,
            ensure_ascii=False,
        )

        tmp.close()

        Path(tmp.name).replace(self.file)

    # ----------------------------------------------------
    # CRUD
    # ----------------------------------------------------

    def get_all(self):

        return self.load()

    def add(self, deadline):

        data = self.load()

        data.append(deadline)

        self.save(data)

    def delete(self, deadline_id):

        data = self.load()

        data = [
            d
            for d in data
            if d.id != deadline_id
        ]

        self.save(data)

    def update(self, deadline):

        data = self.load()

        for i, item in enumerate(data):

            if item.id == deadline.id:

                data[i] = deadline

                break

        self.save(data)

    # ----------------------------------------------------

    def clear(self):

        self.save([])

    def count(self):

        return len(self.load())

    def exists(self, deadline_id):

        for d in self.load():

            if d.id == deadline_id:
                return True

        return False

    def get(self, deadline_id):

        for d in self.load():

            if d.id == deadline_id:

                return d

        return None