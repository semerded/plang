from ..handler.OID import OID
from .rect import Rect
from ...typedef import *
from ...enum import mouseButton
from ... import data
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .window import Window


class InteractiveRect(Rect):
    """
    adds interactions to a rect
    """

    def __init__(self, window: 'Window', x: screen_unit, y: screen_unit, width: screen_unit, height: screen_unit) -> None:
        super().__init__(x, y, width, height)
        self.oid: OID = OID()
        self.window: 'Window' = window
        self._is_clicked_in_rect = False
        self._enabled = True        

    def _cycle(self):
        if self.is_clicked():
            self._is_clicked_in_rect = True
        
        if self.window.mouse.is_mouse_released():
            self._is_clicked_in_rect = False

    def is_mouse_over(self) -> bool:
        return self.window.mouse.is_mouse_over(self.pack())

    def is_clicked(self, mouse_button: mouseButton = mouseButton.left, overwrite_widget_already_pressed: bool = False, overwrite_deactivated: bool = False) -> bool:
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_clicked_in_rect(self.pack(), mouse_button)

    def is_released(self, mouse_button: mouseButton = mouseButton.left, overwrite_widget_already_pressed: bool = False, overwrite_deactivated: bool = False) -> bool:
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_released_in_rect(self.pack(), mouse_button)

    def is_pressing(self, mouse_button: mouseButton = mouseButton.left, overwrite_widget_already_pressed: bool = False, overwrite_deactivated: bool = False) -> bool:
        return self._eligible_for_click(overwrite_widget_already_pressed, overwrite_deactivated) and self.window.mouse.is_mouse_pressing_in_rect(self.pack(), mouse_button) and self._is_clicked_in_rect

    def _eligible_for_click(self, overwrite_widget_already_pressed, overwrite_deactivated):
        if not overwrite_widget_already_pressed and data.widget_pressed:
            return False
        if not overwrite_deactivated and not self._enabled:
            return False
        return True
    
    def enable(self):
        self._enabled = True
        
    def disable(self):
        self._enabled = False 
        
    def pack_interactive_rect(self) -> 'InteractiveRect':
        """
        returns a new rect instance from a rect instance
        """
        return self

    def rect_collision(self, rect: Rect) -> bool:
        raise NotImplementedError

    def point_collision(self, x: screen_unit, y: screen_unit) -> bool:
        return x in range(self.x, self.x + self.w + 1) and y in range(self.y, self.y + self.h + 1)
        
