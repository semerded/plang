from typing import TYPE_CHECKING
from src.core.messenger import Messenger, Logger

#? we don't want these vars/modules to show up in the typechecking
if not TYPE_CHECKING:
    import os
    from src.core import init
    from src.core.config.read_config import read_config_file, find_config_file
    from src import data
    data.lib_path = os.path.abspath(__file__)
    data.dll_folder = init.init_dlls(os.path.split(data.lib_path)[0])

    data.cwd = os.getcwd()
    print(data.lib_path)
    
    read_config_file(find_config_file(data.cwd))
    
    Logger._config_logger()
    if Logger._check_log_file_size():
        Logger._cleanup_oldest_log_file()
    Logger.log_system_specs()
    
    init.init_video()
    init.init_plang()
    
    if data.debugging:
        Messenger.info("Debug mode enabled")
        Messenger.debug("DLLs found in " + data.dll_folder)
        Messenger.debug("Running script from " + data.cwd)
        Messenger.success("PLANG ready to run...")

    # cleanup init
    del os, init, data
del TYPE_CHECKING

# start importing modules
from src.data import get_dll_path
from src.core.exit import exit, cleanup
from src.core.window.event import event_handler

from src.color import Color

from src.core.window.window import Window