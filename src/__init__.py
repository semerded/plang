from typing import TYPE_CHECKING
from src.core.messenger import Messenger, get_log_path

#? we don't want these vars/modules to show up in the typechecking
if not TYPE_CHECKING:
    import os
    from src.core import init
    from src.core.messenger import messenger_init
    SDL3_DLL_PATH = init.init_SDL3_DLL(os.path.abspath(__file__))
    init.init_video()
    init.init_plang()

    from src import data
    data.dll_path = SDL3_DLL_PATH
    data.cwd = os.getcwd()
    
    messenger_init()
    
    if data.debugging:
        Messenger.info("Debug mode enabled")
        Messenger.debug("DLL found in " + data.dll_path)
        Messenger.debug("Running script from " + data.cwd)
        Messenger.success("PLANG ready to run...")

    # cleanup init
    del os, init, data, messenger_init, TYPE_CHECKING

# start importing modules
from src.data import get_dll_path
from src.core.exit import exit, cleanup
from src.core.window.event import event_handler

from src.color import Color

from src.core.window.window import Window