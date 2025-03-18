from cffi import FFI
import os
import sys
from .messenger import Messenger
from . import bridge
from .. import data
from ..core.window.event import Event

from ..core.cdef import cdef

SDL_INIT_VIDEO         = 0x00000020
SDL_WINDOW_SHOWN       = 0x00000004
SDL_RENDERER_ACCELERATED = 0x00000002

def init_SDL3_DLL(path):
    current_dir = os.path.dirname(path)
    dll_path = os.path.join(current_dir, "dll", "SDL3.dll")
    if not os.path.isfile(dll_path):
        sys.exit(f"SDL3.dll not found at {dll_path}. Please place SDL3.dll in the project folder.")

    bridge.sdl = bridge.ffi.dlopen(dll_path)
    
def init_video():
    if not bridge.sdl.SDL_Init(SDL_INIT_VIDEO):
        Messenger.sdl_error("failed to initialize SDL video")
        

def init_plang():
    data.event = Event()

