

from src.core.backend import _backend_init
_backend_init()
del _backend_init
from src.enum import mouseButton, mouseCursor, key, xPos, yPos, corner
from src.color import Color
from src.version import get_version
from src import exceptions, messenger, typedef

# core/handler
from src.core.handler.clock import Clock
from src.core.handler.OID import OID
from src.core.handler.fps_counter import FPSCounter

# core/utils
from src.core.utils.screenunits import dw, dh, screen_units
from src.core.utils.debugging import enable_debugging, DebugTimer
from src.core.utils.aspect_ratio import convert_aspect_ratio, get_height_from_aspect_ratio, get_width_from_aspect_ratio
from src.core.window.rect import Rect
from src.core.window.interactive_rect import InteractiveRect
from src.core.utils.coordinate import Coordinate
from src.core.utils.font import Font

# core/window
from src.core.window.window import Window
from src.core.window.draw import Draw

# widgets
#   core widgets
from src.widget.core.widget import Widget, dispose
from src.widget.core.text import Text
#   input widgets
from src.widget.input.button.button import Button
from src.widget.input.button.radio_button import RadioButton
from src.widget.input.button.checkbox import Checkbox
#   static widgets
from src.widget.static.text_box import TextBox
#   debug widgets
from src.widget.debug.fps_counter_widget import FPScounterWidget

# cache
from src.core.utils.cache.font_cache import fonts


