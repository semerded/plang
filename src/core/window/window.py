import sdl2
import sdl2.ext
from ...typedef import screenUnit
from ...core.window.event import Event
from ...core.window.keyboard import Keyboard
from ...core.window.mouse import Mouse
from ...core.utils.screenunits import ScreenUnits
from ... import data
import sys

class Window:
    """
    Create a window to draw on and take events from. Multiple windows can be created
    """
    def __init__(self, width: screenUnit, height: screenUnit, show_on_creation: bool = True, title: str = data.default_window_name):
        self.title: str = title
        self.width: screenUnit = width
        self.height: screenUnit = height
        
        sdl2.ext.init()
        self._window = sdl2.ext.Window(self.title, size=(self.width, self.height))
        self._renderer = sdl2.ext.Renderer(self._window)
        
            
        data.window_count += 1
            
        self._event = Event()
        self.keyboard: Keyboard  = self._event.keyboard
        self.mouse: Mouse = self._event.mouse
        self.sc: ScreenUnits = ScreenUnits(width, height)
        
        if show_on_creation:
            self._window.show()
        
    def event_handler(self) -> None:
        """
        Handle keyboard, mouse, clock and window events
        """
        self._event.handle(self.close)
                    
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
        
    def update(self):
        self._renderer.present()

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
    
    def resize(self, width: screenUnit, height: screenUnit):
        self.width = width
        self.height = height
        self.sc.width = width
        self.sc.height = height
        self.update()