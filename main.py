
"""
DeadlineDock
main.py

Application entry point.
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.window import MainWindow
from app.theme import GLOBAL_QSS


def main():
    app = QApplication(sys.argv)

    app.setApplicationName("DeadlineDock")
    app.setOrganizationName("DeadlineDock")

    app.setStyleSheet(GLOBAL_QSS)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
