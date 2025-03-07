from typing import Union, TYPE_CHECKING

from ...typedef import screen_unit, RGBAvalue, RGBvalue
from ...core.handler.fps_counter import FPSCounter
from ...widget.core.text import Text
from ...enum import corner
from ...core.utils.font import Font
from ...core.utils.cache.font_cache import fonts
from ...color import Color
from ...messenger import Messenger
from ...core.utils.coordinate import Coordinate

if TYPE_CHECKING:
    from ...core.window.window import Window


class FPScounterWidget:
    def __init__(self, window: 'Window', position: Union[corner, Coordinate], font_size: int = 12, color: Union[RGBvalue, RGBAvalue] = Color.GREEN) -> None:
        self.window = window
        self._font = Font(fonts.ARIAL, font_size)
        self._fps_counter = FPSCounter()
        self._color = Color._handle_rgb_rgba(color)
        self._text = Text(window, 0.0, self._font, self._color)
        self._position = position

        if isinstance(position, Coordinate):
            self._locked_corner_position = False
            self.x = position.x
            self.y = position.y
        else:
            self._locked_corner_position = True
            self._calculate_corner_position(position)

    def _calculate_corner_position(self, _corner) -> None:
        text_size = self._text.get_size()
        if _corner == corner.top_left:
            self.x = 0
            self.y = 0

        elif _corner == corner.top_right:
            self.x = self.window.width - text_size[0]
            self.y = 0

        elif _corner == corner.bottom_left:
            self.x = 0
            self.y = self.window.height - text_size[1]

        elif _corner == corner.bottom_right:
            self.x = self.window.width - text_size[0]
            self.y = self.window.height - text_size[1]

        else:
            Messenger.fatalError(TypeError(
                f"{_corner} with type {type(_corner)} is not a valid instance of 'Coordinate' or enum 'corner' while positioning an FPScounterWidget"))

    def set_color(self, color: Union[RGBvalue, RGBAvalue]) -> None:
        self._color = Color._handle_rgb_rgba(color)

    def draw(self) -> None:
        self._fps_counter.tick()
        self._text.change_text(f"{round(self._fps_counter.get_fps(), 2)} FPS")

        if self._locked_corner_position:
            self._calculate_corner_position(self._position)
            self._text.set_position(self.x, self.y)
        self._text.draw()
