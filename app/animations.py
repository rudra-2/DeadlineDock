"""
DeadlineDock
app/animations.py

Reusable animation helpers.
"""

from PySide6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QParallelAnimationGroup,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect


FAST = 120
NORMAL = 180
SLOW = 260


def ensure_opacity_effect(widget):
    effect = widget.graphicsEffect()
    if not isinstance(effect, QGraphicsOpacityEffect):
        effect = QGraphicsOpacityEffect(widget)
        effect.setOpacity(1.0)
        widget.setGraphicsEffect(effect)
    return effect


def fade_in(widget, duration=NORMAL, start=0.0, end=1.0):
    effect = ensure_opacity_effect(widget)
    anim = QPropertyAnimation(effect, b"opacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
    widget._fade_anim = anim
    return anim


def fade_out(widget, duration=NORMAL, start=1.0, end=0.0):
    effect = ensure_opacity_effect(widget)
    anim = QPropertyAnimation(effect, b"opacity", widget)
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(QEasingCurve.OutCubic)
    anim.start()
    widget._fade_anim = anim
    return anim


def slide_from_y(widget, offset=18, duration=NORMAL):
    start = widget.pos() + QPoint(0, offset)
    end = widget.pos()

    widget.move(start)

    move = QPropertyAnimation(widget, b"pos", widget)
    move.setDuration(duration)
    move.setStartValue(start)
    move.setEndValue(end)
    move.setEasingCurve(QEasingCurve.OutCubic)

    effect = ensure_opacity_effect(widget)
    fade = QPropertyAnimation(effect, b"opacity", widget)
    fade.setDuration(duration)
    fade.setStartValue(0.0)
    fade.setEndValue(1.0)
    fade.setEasingCurve(QEasingCurve.OutCubic)

    group = QParallelAnimationGroup(widget)
    group.addAnimation(move)
    group.addAnimation(fade)
    group.start()

    widget._intro_anim = group
    return group


def press(widget, scale_down_px=1, duration=FAST):
    start = widget.geometry()
    end = start.adjusted(scale_down_px, scale_down_px,
                         -scale_down_px, -scale_down_px)

    anim = QPropertyAnimation(widget, b"geometry", widget)
    anim.setDuration(duration)
    anim.setStartValue(start)
    anim.setEndValue(end)
    anim.setEasingCurve(QEasingCurve.OutQuad)
    anim.start()
    widget._press_anim = anim
    return anim


def restore(widget, original_geometry, duration=FAST):
    anim = QPropertyAnimation(widget, b"geometry", widget)
    anim.setDuration(duration)
    anim.setStartValue(widget.geometry())
    anim.setEndValue(original_geometry)
    anim.setEasingCurve(QEasingCurve.OutBack)
    anim.start()
    widget._restore_anim = anim
    return anim
