from .. import bridge
from enum import IntEnum
from ...core.cdef.cdef_bridge import eventType
from ... import data
from ..messenger import Messenger
from ...core import exit

class EventReturn(IntEnum):
    QUIT = 0
    DESTROY = 1
    SHOW = 2

class Event:
    def __init__(self):
        self.event = bridge.ffi.new("SDL_Event *")
        
        
    def handle(self) -> EventReturn:
        while bridge.sdl.SDL_PollEvent(self.event):
            print(eventType(self.event.type).name)
            event_type = self.event.type
            
            match event_type:
                case eventType.EVENT_QUIT.value: 
                    print("Quit event received. Exiting...")
                    # data.window_tracker[data.active_window_id].destroy()
                    exit.exit()
                    
                
                case eventType.EVENT_WINDOW_CLOSE_REQUESTED.value:
                    data.window_tracker[data.active_window_id].destroy()
                
                case eventType.EVENT_WINDOW_FOCUS_GAINED.value:
                    data.active_window_id = self.event.window.windowID
                    
                case eventType.EVENT_WINDOW_FOCUS_LOST.value:
                    data.active_window_id = -1
            
                case eventType.EVENT_KEY_DOWN.value:
                    kb = self.event.key
                    scancode = kb.scancode   # Should correspond to SDL_SCANCODE values.
                    sym = kb.key             # Virtual key code; may be 0 if it wasn't mapped.
                    mod = kb.mod             # Modifier bitmask.
                    print(bridge.ffi.string(bridge.sdl.SDL_GetKeyName(bridge.sdl.SDL_GetKeyFromScancode(scancode, mod, False))).decode('utf-8'))
                    # print(f"KeyDown event: scancode={scancode}, sym={sym}, mod={mod}")
            
                case eventType.EVENT_KEY_UP.value:
                    kb = self.event.key
                    scancode = kb.scancode   # Should correspond to SDL_SCANCODE values.
                    sym = kb.key             # Virtual key code; may be 0 if it wasn't mapped.
                    mod = kb.mod             # Modifier bitmask.
                    # print(f"KeyUp event: scancode={scancode}, sym={sym}, mod={mod}")
            
                case eventType.EVENT_MOUSE_BUTTON_DOWN.value:
                    print("Mouse button down event")
            
                case eventType.EVENT_MOUSE_BUTTON_UP.value:
                    print("Mouse button up event")
            
                case eventType.EVENT_MOUSE_MOTION.value:
                    print("Mouse motion event")
            
                case eventType.EVENT_MOUSE_WHEEL.value:
                    print("Mouse wheel event")


def event_handler():
    return_value = data.event.handle()
    if bridge.ffi.string(bridge.sdl.SDL_GetError()).decode('utf-8'):
        Messenger.sdl_error("failed to poll SDL events")
    
