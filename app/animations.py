"""
DeadlineDock Animations
-----------------------
Subtle, restrained motion. Everything under 200 ms. No bounce.
"""

from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtWidgets import QWidget


class FadeAnimation:
    def __init__(self, widget: QWidget, duration_ms: int = 160):
        self.widget = widget
        self.anim = QPropertyAnimation(widget, b"windowOpacity")
        self.anim.setDuration(duration_ms)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    def fade_in(self, target: float = 1.0):
        self.widget.setWindowOpacity(0.0)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(target)
        self.anim.start()

    def fade_out(self, target: float = 0.0, on_finished=None):
        self.anim.setStartValue(self.widget.windowOpacity())
        self.anim.setEndValue(target)
        if on_finished:
            self.anim.finished.connect(on_finished)
        self.anim.start()


class SlideAnimation:
    def __init__(self, widget: QWidget, distance: int = 10, duration_ms: int = 160):
        self.widget = widget
        self.anim = QPropertyAnimation(widget, b"pos")
        self.anim.setDuration(duration_ms)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.distance = distance
        self._base_pos = widget.pos()

    def slide_in_from_top(self):
        start = QPoint(self._base_pos.x(), self._base_pos.y() - self.distance)
        self.widget.move(start)
        self.anim.setStartValue(start)
        self.anim.setEndValue(self._base_pos)
        self.anim.start()