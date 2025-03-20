from . import bridge
from .. import data
import sys
from .messenger import Messenger
from random import choice
from typing import Union, NoReturn

# we just want to spread kindness amongst the developers
_spread_kindness: list[str] = ("You did a good job!", "Good job developing.", "Very nice!", "Good job!", "Keep it up!")

def exit() -> NoReturn:
    """
    cleanup SDL and CFFI and exit with exit code 0
    """
    cleanup()
    sys.exit(0)
    
def exit_on_zero_windows() -> Union[None, NoReturn]:
    if len(data.window_tracker) == 0:
        Messenger.debug("no windows left, exiting...")
        bridge.sdl.SDL_Quit()
        bridge.ffi.dlclose(bridge.sdl)   
        Messenger.success("PLANG successfully cleaned up. " + choice(_spread_kindness))
        sys.exit(0)
        
def cleanup() -> None:
    """
    cleanup SDL and CFFI
    """
    for window in data.window_tracker.values():
        window.destroy(remove_from_tracker=False)
    bridge.sdl.SDL_Quit()
    bridge.ffi.dlclose(bridge.sdl)
    Messenger.success("PLANG successfully cleaned up. " + choice(_spread_kindness))
    
