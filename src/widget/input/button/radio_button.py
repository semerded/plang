from typing import TYPE_CHECKING, Union

from ....widget.core.widget import Widget
from ....color import Color
from ....typedef import screen_unit, RGBvalue, RGBAvalue
from ....enum import mouseButton

if TYPE_CHECKING:
    from ....core.window.window import Window


class RadioButton(Widget):
    def __init__(self, window, id: str, x: screen_unit, y: screen_unit, radius: screen_unit, color: Union[RGBvalue, RGBAvalue] = Color.WHITE, active_color: Union[RGBvalue, RGBAvalue] = Color.BLUE):
        self._radius: screen_unit = radius
        self.id: str = "radio:" + id
        self._active: bool = False
        self._active_color: Union[RGBvalue, RGBAvalue] = active_color

        super().__init__(window, x, y, radius * 2, radius * 2, color)
        self.set_border(1, Color.BLACK)
        
        print(self.unpack())

        if self.window.shared_data.get(self.id) is None:
            self.window.shared_data[self.id] = self.oid()
            self._active = True
        self.window._widgets[self.oid()] = self

    def _cycle(self):
        super()._cycle()
        if self.window.shared_data[self.id] != self.oid() and self._is_clicked_in_rect:
            self.window._widgets[self.window.shared_data[self.id]
                                 ]._active = False
            self.window.shared_data[self.id] = self.oid()
            self._active = True
            print(False)

    def draw(self) -> None:
        self.window.draw.circle_with_border(
            self.x, self.y, self._radius, 1, self._color, self._border_color)

        if self.is_active():
            self.window.draw.circle(
                self.x, self.y, self._radius - 3, self._active_color)

    def is_active(self) -> bool:
        return self._active
