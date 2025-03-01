from time import perf_counter
from typing import TYPE_CHECKING, Union, Annotated, Any
from ...object.screen_object import ScreenObject
from ...enum import mouse_button
from ...typedef import RGBAvalue, RGBvalue, screen_unit, percent
from ...core.window.window import Window
from ...color import Color
from ...enum import xPos, yPos
from ...object.text import Text
from ...core.utils.font import Font
from ...annotated_var import unchanged

class Button(ScreenObject):
    def __init__(self, window: Window, x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit, color: RGBvalue | RGBAvalue = Color.WHITE, radius: int = 0):
        super().__init__(window, x, y, width, height, color)
        
        self.text = None
        self.icon = None
        self._radius = radius
        self._click_time = 0
        self._double_click_timer = 0
        self._double_click_interval = 0.5 # default on windows os
        self._text_position = (50, 50)
        
    def set_text(self, text: Any, font: Font, color: Union[RGBvalue, RGBAvalue] = Color.WHITE, position: Union[tuple[xPos, yPos], tuple[Annotated[percent, 2]]] = unchanged) -> None:
        self.text = Text(self.window, text, font, color)
        if position != None:
            self.set_text_position(position)
            
    def set_text_position(self, position:  Union[tuple[xPos, yPos], tuple[Annotated[percent, 2]]]) -> None:
        if self._text_position != position:
            self._text_position = position
    
    def set_icon(self):
        raise NotImplementedError
    
    def set_radius(self, radius: screen_unit = 0):
        self._radius = radius
    
    def set_individual_radius(self, top_left: screen_unit = 0, top_right: screen_unit = 0, bottom_left: screen_unit = 0, bottom_right: screen_unit = 0):
        self._radius = (top_left, top_right, bottom_left, bottom_right)
    
    def is_double_clicked(self, mouse_button: mouse_button = mouse_button.left, overwrite_widget_already_pressed: bool = False, overwrite_deactivated: bool = False):
        if self.is_clicked(mouse_button, overwrite_widget_already_pressed, overwrite_deactivated):
            if perf_counter() - self._double_click_timer <= self._double_click_interval:
                self._double_click_timer = 0
                return True
            self._double_click_timer = perf_counter()
        if self.window.mouse.is_mouse_clicked_outside_rect(self.pack(), mouse_button):
            self._double_click_timer = 0
        return False

    def set_double_click_interval(self, double_click_interval: float):
        """
        set the double click interval in ms (positive floating point number)
        """
        if double_click_interval > 0:
            self._double_click_interval = double_click_interval
            
    def is_held_for(self, milliseconds: int,  mouse_button: mouse_button = mouse_button.left, overwrite_widget_already_pressed: bool = False, overwrite_deactivated: bool = False):
        if self.is_clicked(mouse_button, overwrite_widget_already_pressed, overwrite_deactivated):
            self._click_time = perf_counter()
            
        return self.is_pressing(mouse_button, overwrite_widget_already_pressed, overwrite_deactivated) and (perf_counter() - self._click_time >= milliseconds)
    
    def draw(self):
        self.window.draw.rectangle(*self.unpack(), self._color, self._radius)
        
        if self.text != None:
            self.text.draw_in_rect(self.pack(), *self._text_position)
            