from ...core.window.interactive_rect import InteractiveRect
from ...color import Color
from ...typedef import RGBAvalue, RGBvalue, screen_unit
from ...core.window.window import Window
from typing import Union


class Widget(InteractiveRect):
    def __init__(self, window: Window, x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit, color: Union[RGBvalue, RGBAvalue] = Color.WHITE):
        super().__init__(window, x, y, width, height)
        self._border_width = None
        self._border_color = Color.BLACK
        self._color = Color._handle_rgb_rgba(color)

    def set_color(self, color: RGBAvalue | RGBvalue):
        self._color = Color._handle_rgb_rgba(color)

    def set_border(self, width: screen_unit, color: Union[RGBvalue, RGBAvalue] = Color.BLACK) -> None:
        self._border_width = width
        self._border_color = color

