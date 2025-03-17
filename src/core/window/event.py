from .. import bridge
from enum import IntEnum

class EventReturn(IntEnum):
    QUIT = 0
    HIDE = 1
    SHOW = 2

class Event:
    def __init__(self):
        self.event = bridge.ffi.new("SDL_Event *")
        
        
    def handle(self) -> EventReturn:
        while bridge.sdl.SDL_PollEvent(self.event):
            event_type = self.event.type
            
            if event_type == 0x100:  # SDL_QUIT
                print("Quit event received. Exiting...")
                return EventReturn.QUIT
                

            elif event_type == 0x300:  # SDL_KEYDOWN
                kb = self.event.key
                scancode = kb.scancode   # Should correspond to SDL_SCANCODE values.
                sym = kb.key             # Virtual key code; may be 0 if it wasn't mapped.
                mod = kb.mod             # Modifier bitmask.
                print(bridge.ffi.string(bridge.sdl.SDL_GetKeyName(bridge.sdl.SDL_GetKeyFromScancode(scancode, mod, False))).decode('utf-8'))
                # print(f"KeyDown event: scancode={scancode}, sym={sym}, mod={mod}")