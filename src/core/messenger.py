import sys
from ..typedef import *
from .. import data
from typing import NoReturn, Callable
from . import bridge
from colorama import init as colorama_init, Fore, Style, Back
from datetime import datetime
import logging
import platform
import os

colorama_init()

logger: logging.Logger = None
logger_mapping: dict[int, Callable] = {}
LEADING_LENGTH: int = 12


class SDL_Error(Exception):
    pass


class Logger:
    @staticmethod
    def _config_logger():
        global logger, logger_mapping
        if data.logging_enabled and logger == None:
            if not os.path.isdir(data.log_file_location):
                os.mkdir(data.log_file_location)

            data.logger_file_name = f"log-runtime={datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

            logging.basicConfig(filename=os.path.join(data.log_file_location, data.logger_file_name),
                                format='%(asctime)s %(levelname)-8s %(message)s',
                                datefmt='%H:%M:%S:%m',
                                filemode='w',
                                level=logging.DEBUG)
            logger = logging.getLogger()
            logger_mapping = {logging.DEBUG: logger.debug, logging.INFO: logger.info,
                              logging.WARNING: logger.warning, logging.ERROR: logger.error, logging.CRITICAL: logger.critical}

    @staticmethod
    def get_log_path() -> path:
        return data.log_file_location

    @staticmethod
    def log(level: Callable, message: str, exc_info: tuple = None, descriptor: str = "") -> None:
        if data.logging_enabled:
            if descriptor == None:
                descriptor = ""
            logger_mapping[level](descriptor + message, exc_info=exc_info)

    @staticmethod
    def log_system_specs():
        system_info = {
            "Date and Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Python Version": sys.version,
            "Python Implementation": platform.python_implementation(),
            "Operating System": platform.system(),
            "OS Version": platform.version(),
            "OS Release": platform.release(),
            "Machine Type": platform.machine(),
            "Processor": platform.processor(),
            "Hostname": platform.node(),
            "CPU Architecture": platform.architecture()[0]
        }

        try:
            statvfs = os.statvfs('/')
            system_info["Disk Space (Total GB)"] = round(
                (statvfs.f_frsize * statvfs.f_blocks) / (1024 ** 3), 2)
            system_info["Disk Space (Free GB)"] = round(
                (statvfs.f_frsize * statvfs.f_bfree) / (1024 ** 3), 2)
        except AttributeError:
            system_info["Disk Space"] = "Not available natively on this platform"

        with open(os.path.join(data.log_file_location, data.logger_file_name), "w") as log_file:
            log_file.write("Log file started\n")
            for key, value in system_info.items():
                log_file.write(f"{key}: {value}\n")

    def _check_log_file_size() -> bool:
        num_files = len([f for f in os.listdir(data.log_file_location) if os.path.isfile(
            os.path.join(data.log_file_location, f))])
        return num_files >= data.log_file_limit

    def _cleanup_oldest_log_file():
        dates = []
        for file in os.listdir(data.log_file_location):
            date = os.path.splitext(file)[0].split("=")[1]
            dates.append(datetime.strptime(date, "%Y-%m-%d_%H-%M-%S"))

        os.remove(os.path.join(data.log_file_location,
                  f'log-runtime={min(dates).strftime("%Y-%m-%d_%H-%M-%S.log")}'))


def chaotic_cleanup():
    """
    Cleanup function called before termination to ensure proper cleanup of C instances.
    """
    Messenger.warning(
        "Encountered an error with terminate request, attempting cleanup...")
    for window in data.window_tracker.values():
        window.destroy(remove_from_tracker=False)
    bridge.sdl.SDL_Quit()
    bridge.ffi.dlclose(bridge.sdl)
    Messenger.success("Successful cleanup")
    if data.print_stacktrace:
        Messenger.info("Stacktrace will be printed below and in the log file")
        Messenger.divider(Fore.RED)


class Messenger:
    @classmethod
    def configure(cls, log_file_location: str = None, add_console_timestamp: bool = None, logging_enabled: bool = None):
        """
        configure the messenger\n
        :param log_file_location: location of the log file [default is 'log' (in your current working directory)]\n
        :param add_console_timestamp: whether to add a timestamp to the console [default is True when in debug mode and False otherwise]\n
        """
        if log_file_location is not None:
            data.log_file_location = path.join(data.cwd, log_file_location)
        if add_console_timestamp is not None:
            data.add_console_timestamp = add_console_timestamp
        if logging_enabled is not None:
            data.logging_enabled = logging_enabled

        Logger._config_logger()

    @staticmethod
    def _print(leading: str, message: str, color: str, descriptor: str = None, descriptor_color=None):
        padding_length = max(0, LEADING_LENGTH - len(leading))
        leading = f"[{color}{' ' *(padding_length / 2).__floor__()}{leading.strip()}{' ' * (padding_length / 2).__ceil__()}{Style.RESET_ALL}]: "
        if data.add_console_timestamp:
            now = datetime.now()
            timestamp = f"{Fore.WHITE}{now.hour:02}:{now.minute:02}:{now.second:02}.{now.microsecond // 1000:03}{Style.RESET_ALL} "
        else:
            timestamp = ""
        if descriptor_color == None:
            descriptor_color = Style.RESET_ALL
        print(
            f"{timestamp}{leading}{descriptor_color}{descriptor}{Style.RESET_ALL}{message}")

    @staticmethod
    def _crash(error_type, error_value, error_traceback):
        Logger.log(logging.CRITICAL, str(error_type), exc_info=(
            error_type, error_value, error_traceback))
        chaotic_cleanup()
        if data.print_stacktrace:
            sys.__excepthook__(error_type, error_value, error_traceback)

    @staticmethod
    def divider(color=None):
        if color == None:
            color = Style.RESET_ALL
        print(color + "\n" + "=" * 80, Style.RESET_ALL, "\n")

    @staticmethod
    def success(message: str, descriptor: str = "", descriptor_color=None) -> None:
        Messenger._print("success", message, Fore.GREEN,
                         descriptor=descriptor, descriptor_color=descriptor_color)
        Logger.log(logging.INFO, "SUCCES: " + message, descriptor=descriptor)

    @staticmethod
    def debug(message: str, descriptor: str = "", descriptor_color=None) -> None:
        if data.debugging:
            Messenger._print("debug", message, Fore.BLUE,
                             descriptor=descriptor, descriptor_color=descriptor_color)
            Logger.log(logging.DEBUG, message, descriptor=descriptor)

    @staticmethod
    def info(message: str, descriptor: str = "", descriptor_color=None) -> None:
        Messenger._print("info", message, Fore.WHITE,
                         descriptor=descriptor, descriptor_color=descriptor_color)
        Logger.log(logging.INFO, message, descriptor=descriptor)

    @staticmethod
    def warning(message: str, descriptor: str = "", descriptor_color=None) -> None:
        Messenger._print("warning", message, Fore.YELLOW,
                         descriptor=descriptor, descriptor_color=descriptor_color)
        Logger.log(logging.WARNING, message, descriptor=descriptor)

    @staticmethod
    def error(error: str | Exception, terminate: bool = False, descriptor: str = "", descriptor_color=None) -> NoReturn | None:
        if terminate and not data.debugging:
            chaotic_cleanup()
            Messenger._print("error", str(
                error), Fore.RED, descriptor=descriptor, descriptor_color=descriptor_color)
            Logger.log(logging.CRITICAL, str(error), descriptor=descriptor)

            if isinstance(error, Exception):
                raise error
            raise Exception(error)
        Messenger._print("error", str(error), Fore.RED)
        Logger.log(logging.ERROR, str(error), descriptor=descriptor)

    @staticmethod
    def critical_error(error: Exception, terminate_in_debug_mode: bool = False, descriptor: str = "", descriptor_color=None) -> NoReturn | None:
        if not data.debugging or terminate_in_debug_mode:
            Messenger._print("crit error", str(error), Fore.MAGENTA,
                             descriptor=descriptor, descriptor_color=descriptor_color)
            Logger.log(logging.CRITICAL, str(error), descriptor=descriptor)
            chaotic_cleanup()
            raise error
        else:
            Messenger.warning(
                "Critical Error in debug mode! The program may not function properly from this point onwards!")
            Messenger._print("crit error", str(error), Fore.MAGENTA)
            Logger.log(logging.CRITICAL, str(error), descriptor=descriptor)

    @staticmethod
    def fatal_error(error: Exception, descriptor: str = "", descriptor_color=None) -> NoReturn:
        Messenger._print("crit error", str(error), Back.MAGENTA,
                         descriptor=descriptor, descriptor_color=descriptor_color)
        Logger.log(logging.CRITICAL, str(error), descriptor=descriptor)
        chaotic_cleanup()
        raise error

    def unexpected_error(error_type, error_value, error_traceback):
        Messenger._print("crit error", str(error_value), Back.MAGENTA)
        Logger.log(logging.CRITICAL, str(error_value))
        Messenger._crash(error_type, error_value, error_traceback)

    @staticmethod
    def sdl_error(info: str = "", descriptor: str = "", descriptor_color=None) -> NoReturn:
        error = bridge.ffi.string(bridge.sdl.SDL_GetError()).decode('utf-8')
        Messenger._print("SDL error", str(error), Back.RED,
                         descriptor=descriptor, descriptor_color=descriptor_color)
        Logger.log(logging.CRITICAL, str(error), descriptor=descriptor)
        chaotic_cleanup()
        raise SDL_Error(info + error)
