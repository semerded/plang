from .window.window import Window
from ..typedef import *
from .. import data
from .. import data, exceptions
from ..messenger import Messenger
from ..core.utils import aspect_ratio as ar
import pygame


def setup(window_width: screen_unit | None = None,
          window_height: screen_unit | None = None,
          aspect_ratio: str | None = None,
          single_window_app: bool = True,
          window_name: str = data.default_window_name,
          max_fps: int = 60) -> None:

    if window_width == None and window_height == None:
        Messenger.fatalError(exceptions.NoWindowSizeError(
            "Both window width and window height are defined as 'None'\n\t-> give 2 dimensions or 1 dimension with an aspect ratio"))

    if aspect_ratio != None:
        if window_width != None:
            window_height = ar.get_height_from_aspect_ratio(
                aspect_ratio, window_width)
            window_width = window_width
        else:
            window_width = ar.get_width_from_aspect_ratio(
                aspect_ratio, window_height)
            window_height = window_height

    data.display_info = pygame.display.Info()
    data.display_width = data.display_info.current_w
    data.display_height = data.display_info.current_h

    data.main_window = Window(window_width, window_height, window_name, )

    # args setup
    data.max_fps = max_fps

    data.single_window_app = single_window_app
