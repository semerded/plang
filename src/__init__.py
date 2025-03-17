from src.core import init, bridge
import os

init.init_SDL3_DLL(os.path.abspath(__file__))
init.init_video()

del os, init

from src.core.window.window import Window