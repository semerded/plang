from ...widget.core.widget import Widget
from typing import TYPE_CHECKING, Union
from ...typedef import screen_unit, RGBAvalue, RGBvalue, percent
from ...core.utils.font import Font
from ...color import Color
from ...widget.core.text import Text
from ...enum import xPos, yPos

if TYPE_CHECKING:
    from ...core.window.window import Window

class TextBox(Widget):
    def __init__(self, window: 'Window', x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit, text: str, font: Font, text_color: Union[RGBvalue, RGBAvalue] = Color.WHITE, box_color: Union[RGBvalue, RGBAvalue] = Color.GRAY) -> None:
        super().__init__(window, x, y, width, height, color=box_color)
        self.text: Text = Text(self.window, text, font, text_color)
        
        
    def draw(self, text_x: Union[percent, xPos] = 50, text_y: Union[percent, yPos] = 50) -> None:
        
        self.window.draw.rectangle(self.x, self.y, self.w, self.h, self._color)
        self.text.draw_in_rect(self.pack(), text_x, text_y)