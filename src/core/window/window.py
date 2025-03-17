from .. import bridge
from ... import data
from ..messenger import Messenger
from ..base.OID import OID
import time

SDL_WINDOW_SHOWN       = 0x00000004
SDL_RENDERER_ACCELERATED = 0x00000002


class Window:
    def __init__(self, width, height, window_name: str = data.default_window_name):
        self.width = width
        self.height = height
        self._window_name = str.encode(window_name)
        self.id = OID()
        
        self._window = bridge.sdl.SDL_CreateWindow(self._window_name, width, height, SDL_WINDOW_SHOWN)
        if self._window == bridge.ffi.NULL:
            Messenger.sdl_error("failed to create SDL window")
        elif data.debugging:
            Messenger.info(f"Created a SDL window with size ({self.width}, {self.height})")
        self._renderer = bridge.sdl.SDL_CreateRenderer(self._window, bridge.ffi.NULL)
        
        if self._renderer == bridge.ffi.NULL:
            Messenger.sdl_error("failed to create SDL renderer")
            
        data.window_tracker[self.id()] = self
        
    def event_handeler(self):
        pass
    
    def fill(self, color):
        if not bridge.sdl.SDL_SetRenderDrawColor(self._renderer, *color):
            Messenger.sdl_error("failed to set SDL renderer draw color")
        if not bridge.sdl.SDL_RenderClear(self._renderer):
            Messenger.sdl_error("failed to clear SDL renderer")
            
    def destroy(self):
        bridge.sdl.SDL_DestroyRenderer(self._renderer)
        bridge.sdl.SDL_DestroyWindow(self._window)
        if self.id() in data.window_tracker.keys():
            data.window_tracker.pop(self.id())
        
        if data.debugging:
            Messenger.info(f"Window with name '{self.window_name}' succesfully destroyed.")
            
    def __del__(self):
        self.destroy() # force destroy when garbage collected
            
    def set_size(self, width, height):
        bridge.sdl.SDL_SetWindowSize(self._window, width, height)
        self.width = width
        self.height = height
        if data.debugging:
            Messenger.info(f"Window with name '{self.window_name}' successfully resized to ({width}, {height}).")
    
    def show(self):
        bridge.sdl.SDL_ShowWindow(self._window)
        if data.debugging:
            Messenger.info(f"Window with name '{self.window_name}' successfully shown.")
            
    def hide(self):
        bridge.sdl.SDL_HideWindow(self._window)
        if data.debugging:
            Messenger.info(f"Window with name '{self.window_name}' successfully hidden.")
    
    def minimize(self):
        bridge.sdl.SDL_MinimizeWindow(self._window)
        if data.debugging:
            Messenger.info(f"Window with name '{self.window_name}' successfully minimized.")
            
    def update(self):
        bridge.sdl.SDL_RenderPresent(self._renderer)
      
    @property
    def window_name(self):
        return self._window_name.decode('utf-8')
    
    @window_name.setter        
    def set_window_name(self, window_name: str):
            self._window_name = str.encode(window_name)