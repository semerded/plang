import sdl2
import sdl2.ext
from .mouse import Mouse
from .keyboard import Keyboard
from typing import Callable
from ...core.handler.clock import Clock
from ... import data


class Event:
    def __init__(self, fps: int) -> None:
        self.events: list = None
        self.mouse: Mouse = Mouse()
        self.keyboard: Keyboard = Keyboard()
        self.clock: Clock = Clock(fps)
        self._fps = fps
    
    def handle(self, fps: int, on_quit: Callable[[], None]) -> bool:
        if fps != self._fps:
            self._fps = fps
            self.clock.fps = fps
        
        if not self._fps == -1:
            self.clock.sleep()
        self.events = sdl2.ext.get_events()
        
        #* reset vars
        self.mouse._reset_mouse_button_status()
        self.keyboard._reset_keys()       
        data.widget_pressed = False
        
        #* handle events
        if not self.is_build_frame():
            for event in self.events:
                if event.type == sdl2.SDL_QUIT:
                    on_quit()
                elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    self.mouse.mouse_buttons_status[event.button.button] = True
                    self.mouse.mouse_flank[event.button.button] = True
                elif event.type == sdl2.SDL_MOUSEBUTTONUP:
                    self.mouse.mouse_buttons_status[event.button.button] = False
                    self.mouse.mouse_flank[event.button.button] = True
                elif event.type == sdl2.SDL_KEYDOWN:
                    self.keyboard.active_keys.append(event.key.keysym.sym)
                    self.keyboard.clicked_keys.append(event.key.keysym.sym)
                elif event.type == sdl2.SDL_KEYUP:
                    index = self.keyboard.active_keys.index(event.key.keysym.sym)
                    self.keyboard.released_keys.append(self.keyboard.active_keys.pop(index))
                    
        
        
    def is_build_frame(self) -> bool:
        
        pass
            