from enum import Enum, auto
from sdl2 import SDL_GetNumVideoDisplays, SDL_Init, SDL_Quit, SDL_GetDisplayBounds, SDL_INIT_VIDEO, SDL_Rect, sdlttf, SDL_SetHint, SDL_HINT_RENDER_DRIVER

from .. import data, exceptions
from ..core.utils.font import Font

class AvailableFonts: ...

def _backend_init():
    global AvailableFonts
    print("welcome to Pla&g")

    SDL_Init(SDL_INIT_VIDEO)
    SDL_SetHint(SDL_HINT_RENDER_DRIVER, b"direct3d11")
    sdlttf.TTF_Init()


    num_displays = SDL_GetNumVideoDisplays()
    display_sizes = []

    for i in range(num_displays):
        bounds = SDL_Rect()
        SDL_GetDisplayBounds(i, bounds)
        display_sizes.append((bounds.w, bounds.h))

    data.display_width, data.display_height = display_sizes[data.primary_display]
    
    Font.cache_os_fonts()
