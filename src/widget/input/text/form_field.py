from ....widget.input.text.form import Form
from ....color import Color
from ....typedef import screen_unit, RGBAvalue, RGBvalue
from typing import Callable, TYPE_CHECKING, Union
from ....core.utils.font import Font
from ....core.utils.cache.font_cache import fonts
from ....core.handler.multiline_keyboard_input import MultilineKeyboardInput

if TYPE_CHECKING:
    from ....core.window.window import Window

class FormField(Form):
    def __init__(self, window: 'Window', x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit, bg_color: Union[RGBvalue, RGBAvalue] = Color.WHITE, text_color: Union[RGBvalue, RGBAvalue] = Color.BLACK, font: Font = Font(fonts.ARIAL, 14), active_on_show: bool = False, on_enter: Callable[[], None] | None = None) -> None:
        super().__init__(window, x, y, width, height, bg_color, text_color, font, active_on_show, on_enter)
        self._keyboard_input = MultilineKeyboardInput(window)
        
        if active_on_show:
            self._keyboard_input.activate()
            
    def draw(self):
        self.window.draw.rectangle(*self.unpack(), self._color)
        self.text_widget.draw_in_rect(self.pack(), 0, 0)