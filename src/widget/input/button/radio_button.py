from typing import TYPE_CHECKING, Union

from ....widget.core.widget import Widget
from ....color import Color
from ....typedef import screen_unit, RGBvalue, RGBAvalue
from ....enum import mouseButton

if TYPE_CHECKING:
    from ....core.window.window import Window


class RadioButton(Widget):
    def __init__(self, window, id: str, cx: screen_unit, cy: screen_unit, radius: screen_unit, color: Union[RGBvalue, RGBAvalue] = Color.WHITE, active_color: Union[RGBvalue, RGBAvalue] = Color.BLUE, default_activate: bool = False):
        """
        Draws a radio button that can be grouped together.\n
        :param window: The window to draw on.\n
        :param id: The id of the radio button. Radio buttons will be grouped together based on their id.\n
        :param cx: The x-coordinate of the center of the radio button.\n
        :param cy: The y-coordinate of the center of the radio button.\n
        :param radius: The radius of the radio button.\n
        :param color: The background color of the radio button in RGB/RGBA format.\n
        :param active_color: The color of the radio button when active in RGB/RGBA format.\n
        :param default_activate: If True, the radio button will be active when created. \n
        By default, the radio button is not active unless it is the first radio button with the given id.\n
        """

        self._radius: screen_unit = radius
        self.id: str = "radio:" + id
        self._active: bool = False
        self._active_color: Union[RGBvalue, RGBAvalue] = active_color

        super().__init__(window, cx - radius, cy - radius, radius * 2, radius * 2, color)
        self.set_border(1, Color.BLACK)

        if self.window.shared_data.get(self.id) is None or default_activate:
            self.window.shared_data[self.id] = self.oid()
            self._active = True
            
        self.window._widgets[self.oid()] = self

    def _cycle(self):
        super()._cycle()
        if self.window.shared_data[self.id] == None:
            self.window.shared_data[self.id] = self.oid()
            self._active = True
        elif self.window.shared_data[self.id] != self.oid() and self._is_clicked_in_rect:
            self.window._widgets[self.window.shared_data[self.id]
                                 ]._active = False
            self.window.shared_data[self.id] = self.oid()
            self._active = True
            
    def __del__(self):
        if self.window.shared_data[self.id] == self.oid():
            self.window.shared_data[self.id] = None
            
        self.window._widgets.pop(self.oid())

    def draw(self) -> None:
        self.window.draw.circle_with_border(
            self.x + self._radius, self.y + self._radius, self._radius, 1, self._color, self._border_color)

        if self.is_active():
            self.window.draw.circle(
                self.x + self._radius, self.y + self._radius, self._radius - 4, self._active_color)

    def is_active(self) -> bool:
        """
        Returns if the current radio button is active or not
        """
        return self._active


    # overwrite of mouse interactions for circle
    def is_mouse_over(self) -> bool:
        return self.window.mouse.is_mouse_in_circle((self.x + self._radius, self.y + self._radius), self._radius)
    
    def is_clicked(self, mouse_button = mouseButton.left, overwrite_widget_already_pressed = False, overwrite_deactivated = False):
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_clicked_in_circle((self.x + self._radius, self.y + self._radius), self._radius, mouse_button)
    
    def is_released(self, mouse_button = mouseButton.left, overwrite_widget_already_pressed = False, overwrite_deactivated = False):
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_released_in_circle((self.x + self._radius, self.y + self._radius), self._radius, mouse_button)

    def is_pressing(self, mouse_button = mouseButton.left, overwrite_widget_already_pressed = False, overwrite_deactivated = False):
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_pressing_in_circle((self.x + self._radius, self.y + self._radius), self._radius, mouse_button)
