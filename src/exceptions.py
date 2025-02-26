#aspect ratio
class InvalidAspectRatioFormat(Exception): 
    """
    raises when an aspect ratio string is not set up like [ratio1]:[ratio2]
    """
class Negativescreen_unitError(Exception): 
    """
    raises when a screen_unit of any type is set to a negative value or 0
    """

# window
class NoWindowSizeError(Exception): ...
class MultipleWindowsInSingleWindowAppError(Exception): ... # TODO remove if not needed

class ExpectedLengthError(Exception):
    """
    raises when an expected length is exceded or not met
    """
    
class OutOfWindowBoundsError(Exception):
    """
    raises when an object/screenunit goes out of bound when it is not supposed to
    """
    
class ColorError(Exception):
    """
    raises when a color is not inputted correctly
    """