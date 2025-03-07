from ....core.window.window import Window
from ...core.widget import ScreenObject
import sdl2.ext
from ....enum import key
from typing import Callable

class Form(ScreenObject): 
    def __init__(self, active_on_show: bool = False, on_enter: Callable[[], None] | None = None) -> None: #TODO change active on show var name
        super().__init__()
        self.input: str = u""
        self.active: bool = active_on_show
        self.on_enter: Callable[[], None] | None = on_enter
        if self.active:
            sdl2.ext.start_text_input()
        
    def _cycle(self) -> None:
        super()
    
        if self.active:
            if self.window.mouse.is_mouse_clicked_outside_rect():
                self.deactivate()
                return # skip input cycle
            
            if self.on_enter != None and self.window.keyboard.is_key_released(key.RETURN):
                self.on_enter()
            else:
                self.input += sdl2.ext.get_text_input()
                
        else:
            if self.window.mouse.is_mouse_clicked_in_rect():
                self.activate()

     
    def activate(self) -> None:
        """
        activate the text input
        """
        self.active = True
        sdl2.ext.start_text_input()
         
    def deactivate(self) -> None:
        """
        deactivate the text input
        """
        self.active = False
        sdl2.ext.stop_text_input()
        
    def clear(self) -> str:
        """
        clear the input and return the value
        """
        input = self.input
        self.input = u""
        return input
    
    def draw(self):
        pass