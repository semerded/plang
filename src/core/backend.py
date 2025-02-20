from sdl2 import SDL_GetNumVideoDisplays, SDL_Init, SDL_Quit, SDL_GetDisplayBounds, SDL_INIT_VIDEO, SDL_Rect

from .. import data, exceptions

def _backend_init():
    print("welcome to Pla&g")

    SDL_Init(SDL_INIT_VIDEO)

    num_displays = SDL_GetNumVideoDisplays()
    display_sizes = []

    for i in range(num_displays):
        bounds = SDL_Rect()
        SDL_GetDisplayBounds(i, bounds)
        display_sizes.append((bounds.w, bounds.h))

    data.display_width, data.display_height = display_sizes[data.primary_display]
