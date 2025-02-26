from ...enum import mouse_button
from ...typedef import coordinate
from .interactive_rect import InteractiveRect
from ...core.utils.coordinate import Coordinate
import sdl2
from typing import Union, Annotated


class Mouse:
    def __init__(self) -> None:
        self.mouse_buttons_status: list[bool] = [False, False, False, False, False, False, False]
        self.mouse_flank: list[bool] = [False, False, False, False, False, False, False]
  
    def _reset_mouse_button_status(self) -> None:
        for i in range(7):
            self.mouse_buttons_status[i] = False
            self.mouse_flank[i] = False
            
    def _pos_flank(self, mouse_button: mouse_button) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_flank[mouse_button] and self.mouse_buttons_status[mouse_button]
    
    def _neg_flank(self, mouse_button: mouse_button) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_flank[mouse_button] and not self.mouse_buttons_status[mouse_button]
    
    def _pressed(self, mouse_button: mouse_button) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_buttons_status[mouse_button]
    
    def _check_if_int(self, mouse_button: Union[int, mouse_button]) -> int:
        if type(mouse_button) == int:
            return mouse_button
        return mouse_button.value
    
    def get_position(self) -> Annotated[tuple, 2]:
        x = sdl2.Sint32()
        y = sdl2.Sint32()
        sdl2.mouse.SDL_GetMouseState(x, y)
        return x.value, y.value
        
    def get_absolute_position(self) -> Annotated[tuple, 2]:
        x_global = sdl2.Sint32()
        y_global = sdl2.Sint32()

        sdl2.mouse.SDL_GetGlobalMouseState(x_global, y_global)
        return x_global.value, y_global.value
    
    # area detection
    def is_mouse_over(self, rect: InteractiveRect) -> bool:
        return rect.point_collision(*self.get_position())
    
    def is_mouse_in_area(self, topCord: coordinate, bottomCord: coordinate) -> bool:
        size = (abs(bottomCord[0] - topCord[0]), abs(bottomCord[1] - topCord[1]))
        rect = InteractiveRect(*topCord, *size)
        return self.is_mouse_over(rect)
    
    def is_mouse_in_polygon(self, polygon: Union[list, tuple [coordinate]]) -> bool:
        raise NotImplementedError
    
    def is_mouse_in_circle(self, center: coordinate, radius: int) -> bool:
        if not isinstance(center, Coordinate):
            center = Coordinate(*center)
            
        return center.difference() < radius

    # click detection
    def is_mouse_clicked(self, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self._pos_flank(mouse_button)
    
    def is_mouse_clicked_in_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_in_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_clicked(mouse_button)
        
    #? not variations
    def is_mouse_clicked_outside_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_over(rect) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_outside_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_clicked(mouse_button)

    # release detection
    def is_mouse_released(self, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self._neg_flank(mouse_button)
    
    def is_mouse_released_in_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_in_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool: 
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_released(mouse_button)
    
    #? not variations
    def is_mouse_released_outside_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_over(rect) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_outside_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool: 
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_released(mouse_button)

    
    # hold detection
    def is_mouse_pressing(self, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self._pressed(mouse_button)
    
    def is_mouse_pressing_in_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_in_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool:
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_pressing(mouse_button)
    
    #? not variations
    def is_mouse_pressing_outside_rect(self, rect: InteractiveRect, mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_over(rect) and self._pressed(mouse_button)
    
    def is_mouse_pressing_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_outside_circle(self, center: coordinate, radius: int, mouse_button: mouse_button = mouse_button.left) -> bool:
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_pressing(mouse_button)
        
        
    # scrolling detection
    def isScrolledUp(self) -> bool:
        return self._pressed(mouse_button.scroll_up)
    
    def isScrolledDown(self) -> bool:
        return self._pressed(mouse_button.scroll_down)
    
    def isScrolled(self) -> bool:
        return self._pressed(mouse_button.scroll_up) or self._pressed(mouse_button.scroll_down)
