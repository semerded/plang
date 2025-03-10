from ...enum import mouseButton, mouseCursor
from ...typedef import screen_unit
from .rect import Rect
from ...core.utils.coordinate import Coordinate
from ...messenger import Messenger
import sdl2
from sdl2.ext import load_image
from typing import Union, Annotated
import math


class Mouse:
    def __init__(self) -> None:
        self.mouse_buttons_status: list[bool] = [False, False, False, False, False, False, False]
        self.mouse_flank: list[bool] = [False, False, False, False, False, False, False]
        self._cursor = None
  
    def _reset_mouse_button_status(self) -> None:
        for i in range(7):
            self.mouse_flank[i] = False
            
    def _pos_flank(self, mouse_button: mouseButton) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_flank[mouse_button] and self.mouse_buttons_status[mouse_button]
    
    def _neg_flank(self, mouse_button: mouseButton) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_flank[mouse_button] and not self.mouse_buttons_status[mouse_button]
    
    def _pressed(self, mouse_button: mouseButton) -> bool:
        mouse_button = self._check_if_int(mouse_button)
        return self.mouse_buttons_status[mouse_button]
    
    def _check_if_int(self, mouse_button: Union[int, mouseButton]) -> int:
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
    def is_mouse_over(self, rect: Rect) -> bool:
        return rect.point_collision(*self.get_position())
    
    def is_mouse_in_area(self, topCord: Coordinate, bottomCord: Coordinate) -> bool:
        size = (abs(bottomCord[0] - topCord[0]), abs(bottomCord[1] - topCord[1]))
        rect = Rect(*topCord, *size)
        return self.is_mouse_over(rect)
    
    def is_mouse_in_polygon(self, polygon: Union[list, tuple [Coordinate]]) -> bool:
        raise NotImplementedError
    
    def is_mouse_in_circle(self, center: Coordinate, radius: int) -> bool:
        if not isinstance(center, Coordinate):
            center = Coordinate(*center)
        dx, dy = center.difference(self.get_position())
        return math.hypot(dx, dy) <= radius







    # click detection
    def is_mouse_clicked(self, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self._pos_flank(mouse_button)
    
    def is_mouse_clicked_in_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_in_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_clicked(mouse_button)
        
    #? not variations
    def is_mouse_clicked_outside_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_over(rect) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_clicked(mouse_button)
    
    def is_mouse_clicked_outside_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_clicked(mouse_button)

    # release detection
    def is_mouse_released(self, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self._neg_flank(mouse_button)
    
    def is_mouse_released_in_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_in_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool: 
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_released(mouse_button)
    
    #? not variations
    def is_mouse_released_outside_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_over(rect) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_released(mouse_button)
    
    def is_mouse_released_outside_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool: 
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_released(mouse_button)

    
    # hold detection
    def is_mouse_pressing(self, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self._pressed(mouse_button)
    
    def is_mouse_pressing_in_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_over(rect) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_in_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_in_polygon(polygon) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_in_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool:
        return self.is_mouse_in_circle(center, radius) and self.is_mouse_pressing(mouse_button)
    
    #? not variations
    def is_mouse_pressing_outside_rect(self, rect: Rect, mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_over(rect) and self._pressed(mouse_button)
    
    def is_mouse_pressing_outside_polygon(self, polygon: Union[list[Union[list, tuple]], tuple[Union[list, tuple]]], mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_in_polygon(polygon) and self.is_mouse_pressing(mouse_button)
    
    def is_mouse_pressing_outside_circle(self, center: Coordinate, radius: int, mouse_button: mouseButton = mouseButton.left) -> bool:
        return not self.is_mouse_in_circle(center, radius) and self.is_mouse_pressing(mouse_button)
        
        
    # scrolling detection
    def isScrolledUp(self) -> bool:
        return self._pressed(mouseButton.scroll_up)
    
    def isScrolledDown(self) -> bool:
        return self._pressed(mouseButton.scroll_down)
    
    def isScrolled(self) -> bool:
        return self._pressed(mouseButton.scroll_up) or self._pressed(mouseButton.scroll_down)


    def set_position(self, x: int, y: int) -> None:
        sdl2.mouse.SDL_WarpMouseGlobal(x, y)
    
    def set_position_relative(self, x: int, y: int) -> None:
        sdl2.mouse.SDL_WarpMouseInWindow(None, x, y)
        
    def set_cursor(self, cursor_type: mouseCursor) -> None:
        """
        Sets the mouse cursor to a system cursor.
        :param cursor_type: Type of cursor fount in the mouseCursor enum.
        """
        cursor = sdl2.SDL_CreateSystemCursor(cursor_type.value)
        if cursor:
            sdl2.SDL_SetCursor(cursor)
            if self._cursor != None:
                sdl2.SDL_FreeCursor(self._cursor)
            self._cursor = cursor
            
        else:
            Messenger.warning("Failed to set system cursor.")

        
    def set_custom_cursor(self, image_path: str, hot_x: screen_unit, hot_y: screen_unit):
        """
        Sets a custom cursor using an image.
        :param image_path: Path to the cursor image (e.g., PNG file).
        :param hot_x: Hotspot X coordinate (focus point of the cursor).
        :param hot_y: Hotspot Y coordinate (focus point of the cursor).
        """
        surface = load_image(image_path)
        if not surface:
            Messenger.warning("Failed to load cursor image.")
            return

        cursor = sdl2.SDL_CreateColorCursor(surface, hot_x, hot_y)
        if cursor:
            # Set the custom cursor
            sdl2.SDL_SetCursor(cursor)
            if self._cursor != None:
                sdl2.SDL_FreeCursor(self._cursor)
            self._cursor = cursor
        else:
            Messenger.warning("Failed to set custom cursor.")

        # Clean up
        sdl2.SDL_FreeCursor(cursor)
        sdl2.SDL_FreeSurface(surface)