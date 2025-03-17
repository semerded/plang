from src.core import init, bridge
import os

init.init_SDL3_DLL(os.path.abspath(__file__))
init.init_video()
init.init_plang()

del os, init

from src.color import Color
from src.core.messenger import Messenger

from src.core.window.window import Window