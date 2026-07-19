"""
DeadlineDock MainWindow
-----------------------
Frameless, draggable, always-on-top, system tray.
Real Windows 11 Acrylic via DWM. Fallback for Win10.
"""

import sys
import ctypes
from ctypes import wintypes
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QScrollArea, QSystemTrayIcon,
    QMenu, QLabel, QApplication, QHBoxLayout
)
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QIcon, QAction, QMouseEvent, QPixmap, QPainter, QColor

from app.config import *
from app.storage import Storage
from app.theme import TOKENS, CONTENT_OVERLAY, CONTENT_OVERLAY_SOLID, GLASS_BORDER, GLOBAL_QSS
from app.animations import FadeAnimation
from ui.titlebar import TitleBar
from ui.deadline_card import DeadlineCard
from ui.add_dialog import AddDialog
from app.models import Deadline

# ------------------------------------------------------------------
# Windows DWM constants
# ------------------------------------------------------------------
if sys.platform == "win32":
    class MARGINS(ctypes.Structure):
        _fields_ = [
            ("cxLeftWidth", ctypes.c_int),
            ("cxRightWidth", ctypes.c_int),
            ("cyTopHeight", ctypes.c_int),
            ("cyBottomHeight", ctypes.c_int),
        ]

    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_SYSTEMBACKDROP_TYPE = 38

    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2      # Mica
    DWMSBT_TRANSIENTWINDOW = 3  # Acrylic
    DWMSBT_TABBEDWINDOW = 4

    DWMWCP_DEFAULT = 0
    DWMWCP_DONOTROUND = 1
    DWMWCP_ROUND = 2
    DWMWCP_ROUNDSMALL = 3


def is_win11_22h2_or_later() -> bool:
    if sys.platform != "win32":
        return False
    ver = sys.getwindowsversion()
    return ver.major >= 10 and ver.build >= 22621


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.storage = Storage()
        self._drag_pos = None
        self._acrylic_enabled = False

        # Window flags: frameless, tool (no taskbar icon)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Attempt real DWM Acrylic
        self._setup_dwm()

        # Central widget
        self.central = QWidget()
        self.setCentralWidget(self.central)

        # If Acrylic worked, central is transparent so DWM shows through;
        # otherwise we use solid fallback.
        if self._acrylic_enabled:
            self.central.setStyleSheet("background: transparent;")
        else:
            self.central.setStyleSheet(f"background: {CONTENT_OVERLAY_SOLID};")

        layout = QVBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Content container (rounded, bordered, overlay for readability)
        self.content = QWidget()
        overlay = CONTENT_OVERLAY if self._acrylic_enabled else CONTENT_OVERLAY_SOLID
        self.content.setStyleSheet(
            f"""
            QWidget {{
                background: {overlay};
                border-radius: {CORNER_RADIUS}px;
                border: 1px solid {GLASS_BORDER};
            }}
            """
        )
        layout.addWidget(self.content)

        inner = QVBoxLayout(self.content)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(0)

        # Title bar
        self.titlebar = TitleBar(self)
        self.titlebar.add_clicked.connect(self._open_add)
        self.titlebar.pin_clicked.connect(self._toggle_topmost)
        inner.addWidget(self.titlebar)

        # Scroll area for deadlines
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setStyleSheet("background: transparent; border: none;")

        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(CONTENT_MARGIN, 12, CONTENT_MARGIN, CONTENT_MARGIN)
        self.scroll_layout.setSpacing(CARD_SPACING)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.scroll_widget)
        inner.addWidget(self.scroll, 1)

        # Empty state label
        self.empty_label = QLabel("No deadlines yet.\nClick + to add one.")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(f"color: {TEXT_MUTED}; font-size: {BODY_SIZE}px; border: none;")
        self.scroll_layout.addWidget(self.empty_label)

        # System tray
        self._setup_tray()

        # Load data
        self.refresh_deadlines()

        # Entry fade
        self.setWindowOpacity(0.0)
        QTimer.singleShot(50, lambda: FadeAnimation(self, WINDOW_FADE_MS).fade_in())

    # ------------------------------------------------------------------
    # DWM / Acrylic
    # ------------------------------------------------------------------

    def _setup_dwm(self):
        if not is_win11_22h2_or_later():
            return

        try:
            hwnd = self.winId().__int__()

            # Dark mode for caption / Mica tint
            dark = ctypes.c_int(1)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                ctypes.byref(dark), ctypes.sizeof(dark)
            )

            # Rounded corners
            corner = ctypes.c_int(DWMWCP_ROUND)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(corner), ctypes.sizeof(corner)
            )

            # Acrylic backdrop (more translucent than Mica — better for widgets)
            backdrop = ctypes.c_int(DWMSBT_TRANSIENTWINDOW)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_SYSTEMBACKDROP_TYPE,
                ctypes.byref(backdrop), ctypes.sizeof(backdrop)
            )

            # Extend frame so backdrop fills client area
            margins = MARGINS(-1, -1, -1, -1)
            ctypes.windll.dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(margins))

            self._acrylic_enabled = True
            self.setAttribute(Qt.WA_TranslucentBackground)
        except Exception:
            self._acrylic_enabled = False

    # ------------------------------------------------------------------
    # System Tray
    # ------------------------------------------------------------------

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self._generate_tray_icon())
        self.tray.setToolTip(APP_NAME)

        menu = QMenu()
        act_show = QAction("Show", self)
        act_show.triggered.connect(self.show_from_tray)
        act_quit = QAction("Quit", self)
        act_quit.triggered.connect(QApplication.quit)

        menu.addAction(act_show)
        menu.addSeparator()
        menu.addAction(act_quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self.tray.show()

    def _generate_tray_icon(self) -> QIcon:
        px = QPixmap(64, 64)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(ACCENT))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(px.rect(), 16, 16)
        p.setPen(QColor("#ffffff"))
        p.setBrush(QColor("#ffffff"))
        p.drawEllipse(28, 20, 8, 8)
        p.drawEllipse(28, 36, 8, 8)
        p.end()
        return QIcon(px)

    def _tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_from_tray()

    def show_from_tray(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        # Minimize to tray instead of quitting
        event.ignore()
        self.hide()

    # ------------------------------------------------------------------
    # Window controls
    # ------------------------------------------------------------------

    def _toggle_topmost(self):
        flags = self.windowFlags()
        if flags & Qt.WindowStaysOnTopHint:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        self.show()

    # ------------------------------------------------------------------
    # Drag (from empty areas)
    # ------------------------------------------------------------------

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._drag_pos = None

    # ------------------------------------------------------------------
    # Deadlines
    # ------------------------------------------------------------------

    def refresh_deadlines(self):
        # Clear existing cards
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        deadlines = self.storage.get_all()

        if not deadlines:
            self.empty_label.show()
            self.scroll_layout.addWidget(self.empty_label)
            return
        else:
            self.empty_label.hide()

        for dl in deadlines:
            card = DeadlineCard(dl)
            card.clicked.connect(self._on_card_clicked)
            card.edit_requested.connect(self._on_edit)
            card.delete_requested.connect(self._on_delete)
            self.scroll_layout.addWidget(card)

    def _open_add(self):
        dialog = AddDialog(self)
        dialog.deadline_saved.connect(self._on_deadline_added)
        dialog.exec()

    def _on_deadline_added(self, deadline: Deadline):
        self.storage.add(deadline)
        self.refresh_deadlines()

    def _on_card_clicked(self, deadline: Deadline):
        # If no URL, open edit
        if not deadline.url:
            self._on_edit(deadline)

    def _on_edit(self, deadline: Deadline):
        dialog = AddDialog(self, edit_deadline=deadline)
        dialog.deadline_saved.connect(self._on_deadline_updated)
        dialog.exec()

    def _on_deadline_updated(self, deadline: Deadline):
        self.storage.update(deadline)
        self.refresh_deadlines()

    def _on_delete(self, did: str):
        self.storage.delete(did)
        self.refresh_deadlines()