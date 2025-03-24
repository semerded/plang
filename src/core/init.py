from cffi import FFI
import os
import sys
from .messenger import Messenger
from . import bridge
from .. import data
from ..core.window.event import Event
from ..typedef import path

from ..core.cdef import cdef

SDL_INIT_VIDEO         = 0x00000020
SDL_WINDOW_SHOWN       = 0x00000004
SDL_RENDERER_ACCELERATED = 0x00000002

def init_SDL3_DLL(path) -> path:
    current_dir = os.path.dirname(path)
    dll_path = os.path.join(current_dir, "dll", "SDL3.dll")
    if not os.path.isfile(dll_path):
        sys.exit(f"SDL3.dll not found at {dll_path}. Please place SDL3.dll in the project folder.")

    bridge.sdl = bridge.ffi.dlopen(dll_path)
    return dll_path
    
def init_video():
    if not bridge.sdl.SDL_Init(SDL_INIT_VIDEO):
        Messenger.sdl_error("failed to initialize SDL video")
        
    # num_drivers = bridge.sdl.SDL_GetNumRenderDrivers()
    # if num_drivers <= 0:
    #     print("No render drivers available or failed to retrieve render driver count.")
    # else:
    #     print("Available renderer drivers:")
    #     for i in range(num_drivers):
    #         driver_name = bridge.ffi.string(bridge.sdl.SDL_GetRenderDriver(i)).decode("utf-8")
    #         print(f"{i + 1}. {driver_name}")
            

def init_plang():
    data.event = Event()

