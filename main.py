"""
DeadlineDock
main.py

Application entry point. Enforces single-instance.
"""

import sys
import tempfile
import atexit
from pathlib import Path

from PySide6.QtWidgets import QApplication

from ui.window import MainWindow
from app.theme import GLOBAL_QSS

LOCK_FILE = Path(tempfile.gettempdir()) / "DeadlineDock.lock"


def single_instance_check() -> bool:
    try:
        fd = Path(LOCK_FILE).open("x")
        fd.close()
        atexit.register(lambda: LOCK_FILE.unlink(missing_ok=True))
        return True
    except FileExistsError:
        return False


def main():
    if not single_instance_check():
        print("DeadlineDock is already running.")
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationName("DeadlineDock")
    app.setOrganizationName("DeadlineDock")
    app.setStyleSheet(GLOBAL_QSS)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()