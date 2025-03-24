from .. import bridge
from ... import data
from ..messenger import Messenger
from ..base.OID import OID
from .. import exit
from .event import Event, EventReturn

SDL_WINDOW_FULLSCREEN         = 0x00000001
SDL_WINDOW_OPENGL             = 0x00000002
SDL_WINDOW_OCCLUDED           = 0x00000004
SDL_WINDOW_HIDDEN             = 0x00000008
SDL_WINDOW_BORDERLESS         = 0x00000010
SDL_WINDOW_RESIZABLE          = 0x00000020
SDL_WINDOW_MINIMIZED          = 0x00000040
SDL_WINDOW_MAXIMIZED          = 0x00000080
SDL_WINDOW_MOUSE_GRABBED      = 0x00000100
SDL_WINDOW_INPUT_FOCUS        = 0x00000200
SDL_WINDOW_MOUSE_FOCUS        = 0x00000400
SDL_WINDOW_EXTERNAL           = 0x00000800
SDL_WINDOW_MODAL              = 0x00001000
SDL_WINDOW_HIGH_PIXEL_DENSITY = 0x00002000
SDL_WINDOW_MOUSE_CAPTURE      = 0x00004000
SDL_WINDOW_ALWAYS_ON_TOP      = 0x00008000
SDL_WINDOW_UTILITY            = 0x00010000
SDL_WINDOW_TOOLTIP            = 0x00020000
SDL_WINDOW_POPUP_MENU         = 0x00040000
SDL_WINDOW_KEYBOARD_GRABBED   = 0x00080000
SDL_WINDOW_VULKAN             = 0x00100000
SDL_WINDOW_METAL              = 0x00200000
SDL_WINDOW_TRANSPARENT        = 0x00400000
SDL_WINDOW_NOT_FOCUSABLE      = 0x00800000


class Window:
    def __init__(self, width, height, window_name: str = None, fill_color=None, vsync: bool = False, resizable: bool = False, fullscreen: bool = False, minimized: bool = False, maximized: bool = False):
        self.width = width
        self.height = height
        if window_name == None:
            self._window_name = str.encode(data.get_default_window_name())
        else:
            self._window_name = str.encode(window_name)
        flags = 0x0
        if resizable:
            flags |= SDL_WINDOW_RESIZABLE
        if fullscreen:
            flags |= SDL_WINDOW_FULLSCREEN
        # if windowed_fullscreen:
        #     if fullscreen:
        #         Messenger.warning("fullscreen and windowed fullscreen flags are mutually exclusive, windowed fullscreen flag will be ignored.")
        #     else:
        #         if not resizable:
        #             Messenger.warning("windowed fullscreen requires resizable flag to be set.")
        #         flags |= SDL_WINDOW_FULLSCREEN_DESKTOP
        

        self._window = bridge.sdl.SDL_CreateWindow(
            self._window_name, width, height, flags)
        if self._window == bridge.ffi.NULL:
            Messenger.sdl_error("failed to create SDL window")
        self.id = bridge.sdl.SDL_GetWindowID(self._window)
        self.set_window_name(
            "[" + str(self.id) + "] " + self.get_window_name())
        Messenger.debug(
            f"Created a SDL window with size ({self.width}, {self.height}) | ID: {self.id}")
        self._renderer = bridge.sdl.SDL_CreateRenderer(
            self._window, bridge.ffi.NULL)

        if self._renderer == bridge.ffi.NULL:
            Messenger.sdl_error("failed to create SDL renderer")

        if vsync:
            self.set_vsync(True)

        self._fill_color = fill_color

        self._event = data.event

        data.window_tracker[self.id] = self

    def destroy(self, remove_from_tracker: bool = True):
        bridge.sdl.SDL_DestroyRenderer(self._renderer)
        bridge.sdl.SDL_DestroyWindow(self._window)
        if remove_from_tracker and self.id in data.window_tracker.keys():
            data.window_tracker.pop(self.id)

        Messenger.debug(
            f"Window with name '{self.get_window_name()}' successfully destroyed.")

    def __del__(self):
        self.destroy()  # force destroy when garbage collected

    def set_size(self, width, height):
        bridge.sdl.SDL_SetWindowSize(self._window, width, height)
        self.width = width
        self.height = height
        Messenger.debug(
            f"Window with name '{self.get_window_name()}' successfully resized to ({width}, {height}).")

    def fill(self):
        if self._fill_color != None:
            if not bridge.sdl.SDL_SetRenderDrawColor(self._renderer, *self._fill_color):
                Messenger.sdl_error("failed to set SDL renderer draw color")

    def set_fill_color(self, color) -> None:
        self._fill_color = color

    def set_vsync(self, vsync: bool, adaptive: bool = False) -> None:
        """
        turn vsync on or off. Vsync is used to limit the refresh rate of the window to the monitors refresh rate. It can be used to prevent screen tearing at the cost of a higher input latency.\n
        :param vsync: True to enable vsync, False to disable\n
        :param adaptive: True to enable adaptive vsync, False to disable, vsync must also be enabled for adaptive to work. Adaptive VSync synchronizes frame presentation with the display refresh rate when the frame rate is sufficient, and allows tearing when the frame rate drops to minimize stuttering and input lag.
        """
        if adaptive and vsync:
            value = -1
        elif vsync:
            value = 1
        else:
            value = 0
        if not bridge.sdl.SDL_SetRenderVSync(self._renderer, value):
            Messenger.sdl_error("failed to set SDL renderer vsync")

    def set_icon(self, surface):
        if not bridge.sdl.SDL_SetWindowIcon(self._window, surface):
            Messenger.sdl_error("failed to set SDL window icon")

    def set_min_size(self, width, height):
        if not bridge.sdl.SDL_SetWindowMinimumSize(self._window, width, height):
            Messenger.sdl_error("failed to set SDL window minimum size")

    def set_max_size(self, width, height):
        if not bridge.sdl.SDL_SetWindowMaximumSize(self._window, width, height):
            Messenger.sdl_error("failed to set SDL window maximum size")

    def show(self):
        bridge.sdl.SDL_ShowWindow(self._window)
        Messenger.debug(
            f"Window with name '{self.get_window_name()}' successfully shown.")

    def hide(self):
        bridge.sdl.SDL_HideWindow(self._window)
        Messenger.debug(
            f"Window with name '{self.get_window_name()}' successfully hidden.")

    def minimize(self):
        bridge.sdl.SDL_MinimizeWindow(self._window)
        Messenger.debug(
            f"Window with name '{self.get_window_name()}' successfully minimized.")

    def update(self):
        bridge.sdl.SDL_RenderPresent(self._renderer)

    def get_window_name(self):
        return self._window_name.decode('utf-8')

    def set_window_name(self, window_name: str):
        self._window_name = str.encode(window_name)
        if not bridge.sdl.SDL_SetWindowTitle(self._window, self._window_name):
            Messenger.sdl_error("failed to set SDL window name")

    @staticmethod
    def is_active(window) -> bool:
        return isinstance(window, Window)
