from . import bridge

bridge.ffi.cdef("""//cpp
typedef unsigned int Uint32;
typedef unsigned char Uint8;

bool SDL_Init(Uint32 flags);
void SDL_Quit(void);

// window
typedef struct SDL_Window SDL_Window;
SDL_Window* SDL_CreateWindow(const char* title, int w, int h, Uint32 flags);
void SDL_DestroyWindow(SDL_Window* window);
bool SDL_SetWindowSize(SDL_Window* window, int w, int h);
bool SDL_ShowWindow(SDL_Window* window);
bool SDL_HideWindow(SDL_Window* window);
bool SDL_MinimizeWindow(SDL_Window* window);

// renderer
typedef struct SDL_Renderer SDL_Renderer;
SDL_Renderer * SDL_CreateRenderer(SDL_Window *window, const char *name);
void SDL_DestroyRenderer(SDL_Renderer* renderer);
bool SDL_SetRenderDrawColor(SDL_Renderer* renderer, Uint8 r, Uint8 g, Uint8 b, Uint8 a);
bool SDL_RenderClear(SDL_Renderer* renderer);
bool SDL_RenderPresent(SDL_Renderer* renderer);
bool SDL_RenderFillRect(SDL_Renderer* renderer, const void *rect);

const char* SDL_GetError(void);

/* For SDL3, you might also query display info.
   (Add additional SDL3-specific functions here as needed.) */
  
typedef struct SDL_Rect {
    int x;
    int y;
    int w;
    int h;
} SDL_Rect;
""")