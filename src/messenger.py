from .typedef import *
from . import data

log_file_location: str = "" # TODO: set to a log dir

class Messenger:
    @staticmethod
    def configure(log_file_location: path = None):
        log_file_location = log_file_location
    
    
    
    @staticmethod
    def info(message: str):
        print(message)
       
    @staticmethod 
    def warning(message: str):
        print(message)
        
    @staticmethod    
    def error(error: str | Exception, terminate: bool = False):
        if terminate and not data.debugging:
            if isinstance(error) == Exception:
                raise error
            raise Exception(error)
        print(error)
        
    @staticmethod   
    def criticalError(error: Exception):
        if not data.debugging:
        # add log message
            raise error
        else: 
            print("Critical Error in debug mode!")
            print("The program may not function properly from this point forwards!")
            print(error)
            
    @staticmethod       
    def fatalError(error: Exception):
        # add log message
        raise error