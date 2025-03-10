import sdl2.ext
from typing import Callable, TYPE_CHECKING, Union

from ....core.window.window import Window
from ...core.widget import Widget
from ....enum import key
from ....color import Color
from ....typedef import RGBAvalue, RGBvalue, screen_unit
from ....widget.core.text import Text
from ....core.utils.font import Font
from ....core.utils.cache.font_cache import fonts
from ....core.handler.keyboard_input import KeyboardInput

if TYPE_CHECKING:
    from ....core.window.window import Window


class Form(Widget):
    # TODO change active on show var name
    def __init__(self, window: 'Window', x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit, bg_color: Union[RGBvalue, RGBAvalue] = Color.WHITE, text_color: Union[RGBvalue, RGBAvalue] = Color.BLACK, font: Font = Font(fonts.ARIAL, 14), active_on_show: bool = False, on_enter: Callable[[], None] | None = None) -> None:
        super().__init__(window, x, y, width, height, bg_color)
        self.input: str = ""
        self.on_enter: Callable[[], None] | None = on_enter
        
        self._keyboard_input = KeyboardInput(window)
        if active_on_show:
            self._keyboard_input.activate()
            
        self.text_widget = Text(window, self.input, font, text_color)

        self.window._widgets[self.oid()] = self

    def _cycle(self) -> None:
        super()._cycle()

        if self._keyboard_input._activated:
            # caret (text cursor) handler
            

            if self.window.mouse.is_mouse_clicked_outside_rect(self.pack()):
                self.deactivate()
                return  # skip input cycle

            elif self.on_enter != None and self.window.keyboard.is_key_released(key.RETURN):
                self.on_enter()
            else:
                # print(self.input)
                self.input = self._keyboard_input.get_input_string() # TODO fix caret being placed in the wrong place
                self.text_widget.set_text(self.input)
        else:
            if self.window.mouse.is_mouse_clicked_in_rect(self.pack()):
                self.activate()

    def __del__(self):
        self.window._widgets.pop(self.oid())

    def activate(self) -> None:
        """
        activate the text input
        """
        self._keyboard_input.activate()

    def deactivate(self) -> None:
        """
        deactivate the text input
        """
        self._keyboard_input.deactivate()

    def clear(self) -> str:
        """
        clear the input and return the value
        """
        input = self.input
        self.input = u""
        return input

    def draw(self):
        self.window.draw.rectangle(*self.unpack(), self._color)
        self.text_widget.draw_in_rect(self.pack(), 0)
