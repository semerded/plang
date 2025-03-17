from . import bridge
from .. import data

def cleanup():
    for window in data.window_tracker.values():
        window.destroy()
    bridge.sdl.SDL_Quit()