from cffi import FFI
import os
import sys
from .messenger import Messenger
from . import bridge
from .. import data
from ..core.window.event import Event
from ..typedef import path
from ..core.exit import cleanup
import atexit

from .cdef import cdef_sld # runs cdef 

SDL_INIT_VIDEO         = 0x00000020
SDL_WINDOW_SHOWN       = 0x00000004
SDL_RENDERER_ACCELERATED = 0x00000002

DLL_NAMES = ["SDL3.dll",]

def init_dlls(lib_path) -> path:
    dll_folder = os.path.join(lib_path, "dll")
    if not os.path.isdir(dll_folder):
        sys.exit(f"Folder {dll_folder} not found. Please create this folder and place all the DLLs in it.")
    
    def get_dll(dll_folder, dll_name) -> object:
        dll_path = os.path.join(dll_folder, dll_name)
        if not os.path.isfile(dll_path):
            sys.exit(f"{dll_name} not found in folder {dll_folder}. Please place {dll_name} in the project folder.")
        return bridge.ffi.dlopen(dll_path)
        
    bridge.sdl = get_dll(dll_folder, DLL_NAMES[0])
    
    return dll_folder
    
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
    # atexit.register(cleanup)
    sys.excepthook = Messenger.unexpected_error

