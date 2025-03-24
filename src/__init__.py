from typing import TYPE_CHECKING
from src.core.messenger import Messenger, Logger

#? we don't want these vars/modules to show up in the typechecking
if not TYPE_CHECKING:
    import os
    from src.core import init
    from src.core.config.read_config import read_config_file, find_config_file
    lib_path = os.path.abspath(__file__)
    SDL3_DLL_PATH = init.init_SDL3_DLL(lib_path)
    init.init_video()
    init.init_plang()

    from src import data
    data.dll_path = SDL3_DLL_PATH
    data.cwd = os.getcwd()
    data.lib_path = lib_path
    
    read_config_file(find_config_file(data.cwd))
    
    Logger._config_logger()
    if Logger._check_log_file_size():
        Logger._cleanup_oldest_log_file()
    Logger.log_system_specs()
    
    if data.debugging:
        Messenger.info("Debug mode enabled")
        Messenger.debug("DLL found in " + data.dll_path)
        Messenger.debug("Running script from " + data.cwd)
        Messenger.success("PLANG ready to run...")

    # cleanup init
    del os, init, data, TYPE_CHECKING

# start importing modules
from src.data import get_dll_path
from src.core.exit import exit, cleanup
from src.core.window.event import event_handler

from src.color import Color

from src.core.window.window import Window