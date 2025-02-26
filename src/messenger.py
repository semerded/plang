from .typedef import *
from . import data
from typing import NoReturn

log_file_location: str = "" # TODO: set to a log dir

class Messenger:
    @staticmethod
    def configure(log_file_location: path = None):
        log_file_location = log_file_location
    
    
    
    @staticmethod
    def info(message: str) -> None:
        """
        send info to the terminal when in not in production mode
        """
        print(message)
       
    @staticmethod 
    def warning(message: str) -> None:
        """
        send a yellow colored warning to stdout when in not in production mode\n
        message will be send in yellow
        """
        print(message)
        
    @staticmethod    
    def error(error: str | Exception, terminate: bool = False) -> (NoReturn | None):
        """
        a non critical error\n
        send a red colored error message to stdout when not in production mode\n
        error can cause a termination when selected and not in debug mode
        """
        if terminate and not data.debugging:
            if isinstance(error) == Exception:
                raise error
            raise Exception(error)
        print(error)
        
    @staticmethod   
    def criticalError(error: Exception, terminate_in_debug_mode: bool = False) -> (NoReturn | None):
        """
        a critcal error\n
        send a purple colored error message to stdout when not in production mode\n
        error will not terminate when in debug mode (can be overwritten with 'terminate_in_debug_mode')
        """
        if not data.debugging or terminate_in_debug_mode:
        # add log message
            raise error
        else: 
            print("Critical Error in debug mode!")
            print("The program may not function properly from this point forwards!")
            print(error)
            
    @staticmethod       
    def fatalError(error: Exception) -> NoReturn:
        """
        a fatal error (program will always terminate)\n
        send a purple background error message to stdout when not in production mode
        """
        # add log message
        raise error