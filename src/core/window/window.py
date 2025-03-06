import sdl2
import sdl2.ext
from ...typedef import screen_unit, RGBAvalue, RGBvalue
from ...core.window.event import Event
from ...core.window.keyboard import Keyboard
from ...core.window.mouse import Mouse
from ...core.utils.screenunits import screen_units
from ...core.window.draw import Draw
from ... import data, Color
from ...messenger import Messenger
import sys

class Window:
    """
    Create a window to draw on and take events from. Multiple windows can be created
    """
    def __init__(self, width: screen_unit, height: screen_unit, fps: int = 60, show_on_creation: bool = True, title: str = data.default_window_name):
        self.title: str = title
        self.width: screen_unit = width
        self.height: screen_unit = height
        if fps < -1 or fps == 0:
            Messenger.fatalError(ValueError("fps can't be negative or 0 (-1 can be used for unlimited fps)"))
        self._fps = fps
        
        sdl2.ext.init()
        self._window = sdl2.ext.Window(self.title, size=(self.width, self.height))
        self._renderer = sdl2.ext.Renderer(self._window, flags=sdl2.SDL_RENDERER_ACCELERATED)
        
            
        data.window_count += 1
            
        self._event = Event(self._fps)
        self.keyboard: Keyboard  = self._event.keyboard
        self.mouse: Mouse = self._event.mouse
        self.sc: screen_units = screen_units(width, height)
        self.draw: Draw = Draw(self._window, self._renderer)
        self.frame_counter = 0

        if show_on_creation:
            self._window.show()
        
    def event_handler(self, background_color: (RGBvalue | RGBAvalue) = Color.BLACK, fps: int = None) -> None:
        """
        Handle keyboard, mouse, clock and window events\n
        Fps can be changed dynamically
        """
        if fps == None:
            fps = self._fps
        elif fps < -1 or fps == 0:
            Messenger.fatalError(ValueError("fps can't be negative or 0 (-1 can be used for unlimited fps)"))
        self.frame_counter += 1

        sdl2.SDL_RenderPresent(self._renderer.sdlrenderer)   
        sdl2.SDL_SetRenderDrawColor(self._renderer.sdlrenderer, *Color._handle_rgb_rgba(background_color))
     
        sdl2.SDL_RenderClear(self._renderer.sdlrenderer)
        
        self._event.handle(fps, self.close)
                            
    def hide(self) -> None:
        """
        Hide the window
        """ 
        self._window.hide()
        
    def minimize(self) -> None:
        """
        Minimize the window\nThe window will go in a slow state
        """
        self._window.minimize()

    def show(self) -> None:
        self._window.show()

    def clear(self, color = (0, 0, 0)) -> None:
        """
        Repaint the full window with a specified color
        """
        self._renderer.clear(color)

    def close(self, quit_program: bool = False) -> None:
        """
        close the window
        """
        self._window.close()
        data.window_count -= 1
        if quit_program or data.window_count == 0:
            sdl2.ext.quit()
            if data.debugging and data.window_count == 0:
                print("PLANG exited because there are 0 windows left")
            sys.exit(0) # using sys library to be able to compile to EXE
    
    def resize(self, width: screen_unit, height: screen_unit):
        self.width = width
        self.height = height
        self.sc.width = width
        self.sc.height = height
        self.update()