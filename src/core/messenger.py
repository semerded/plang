from ..typedef import *
from .. import data
from typing import NoReturn, Callable
from . import bridge
from colorama import init as colorama_init, Fore, Style
from datetime import datetime
import os
import logging

colorama_init()
_log_file_location: None
_add_console_timestamp: bool = None
_logging_enabled: bool = True
logger: logging.Logger = None
logger_mapping: dict[int, Callable]
LEADING_LENGTH: int = 12
logging.CRITICAL

class SDL_Error(Exception):
    pass


def messenger_init():
    global _log_file_location, _add_console_timestamp
    _log_file_location = os.path.join(data.cwd, "log")
    _add_console_timestamp = data.debugging
    config_logger()
    

def config_logger():
    global logger, logger_mapping
    if _logging_enabled and logger == None:
        if not os.path.isdir(_log_file_location):
            os.mkdir(_log_file_location)
        
        file_name = f"log-runtime={datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
        
        logging.basicConfig(filename=os.path.join(_log_file_location, file_name),
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%H:%M:%S:%m',
                            filemode='w',
                            level=logging.DEBUG)
        logger = logging.getLogger()
        logger_mapping = {logging.DEBUG: logger.debug, logging.INFO: logger.info, logging.WARNING: logger.warning, logging.ERROR: logger.error, logging.CRITICAL: logger.critical}

        

def chaotic_cleanup():
    """
    Cleanup function called before termination to ensure proper cleanup of C instances.
    """
    Messenger.warning("Encountered an error with terminate request")
    for window in data.window_tracker.values():
        window.destroy(remove_from_tracker=False)
    bridge.sdl.SDL_Quit()
    bridge.ffi.dlclose(bridge.sdl)
    Messenger.success("Successful cleanup")


def get_log_path() -> path:
    return _log_file_location


class Messenger:
    @classmethod
    def configure(cls, log_file_location: str = None, add_console_timestamp: bool = None, logging_enabled: bool = None):
        """
        configure the messenger\n
        :param log_file_location: location of the log file [default is 'log' (in your current working directory)]\n
        :param add_console_timestamp: whether to add a timestamp to the console [default is True when in debug mode and False otherwise]\n
        """
        global _log_file_location, _add_console_timestamp, _logging_enabled
        if log_file_location is not None:
            _log_file_location = path.join(data.cwd, log_file_location)
        if add_console_timestamp is not None:
            _add_console_timestamp = add_console_timestamp
        if logging_enabled is not None:
            _logging_enabled = logging_enabled
            
        config_logger()

    @staticmethod
    def _print(leading: str, message: str, color: str):
        padding_length = max(0, LEADING_LENGTH - len(leading))
        leading = f"[{color}{' ' *(padding_length / 2).__floor__()}{leading.strip()}{' ' * (padding_length / 2).__ceil__()}{Style.RESET_ALL}]: "
        if _add_console_timestamp:
            now = datetime.now()
            timestamp = f"{now.hour:02}:{now.minute:02}:{now.second:02}.{now.microsecond // 1000:03} "
        else:
            timestamp = ""
        print(
            f"{timestamp}{leading}{message}")
        
    @staticmethod
    def _log(level, message: str):
        if _logging_enabled:
            logger_mapping[level](message)        

    @staticmethod
    def success(message: str) -> None:
        Messenger._print("success", message, Fore.GREEN)
        Messenger._log(logging.INFO, "SUCCES: " + message)

    @staticmethod
    def debug(message: str) -> None:
        if data.debugging:
            Messenger._print("debug", message, Fore.BLUE)
            Messenger._log(logging.DEBUG, message)

    @staticmethod
    def info(message: str) -> None:
        Messenger._print("info", message, Fore.WHITE)
        Messenger._log(logging.INFO, message)

    @staticmethod
    def warning(message: str) -> None:
        Messenger._print("warning", message, Fore.YELLOW)
        Messenger._log(logging.WARNING, message)

    @staticmethod
    def error(error: str | Exception, terminate: bool = False) -> NoReturn | None:
        if terminate and not data.debugging:
            chaotic_cleanup()
            Messenger._log(logging.CRITICAL, str(error))
            if isinstance(error, Exception):
                raise error
            raise Exception(error)
        Messenger._print("error", str(error), Fore.RED)
        Messenger._log(logging.ERROR, str(error))

    @staticmethod
    def critical_error(error: Exception, terminate_in_debug_mode: bool = False) -> NoReturn | None:
        if not data.debugging or terminate_in_debug_mode:
            Messenger._log(logging.CRITICAL, str(error))
            chaotic_cleanup()
            raise error
        else:
            print(
                "Critical Error in debug mode! The program may not function properly from this point onwards!")
            Messenger._log(logging.CRITICAL, str(error))
            Messenger._print("crit error", str(error), Fore.MAGENTA)

    @staticmethod
    def fatal_error(error: Exception) -> NoReturn:
        Messenger._log(logging.CRITICAL, str(error))
        chaotic_cleanup()
        raise error

    @staticmethod
    def sdl_error(info: str = "") -> NoReturn:
        error = bridge.ffi.string(bridge.sdl.SDL_GetError()).decode('utf-8')
        Messenger._log(logging.CRITICAL, str(error))
        chaotic_cleanup()
        raise SDL_Error(info + error)
