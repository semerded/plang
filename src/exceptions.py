#aspect ratio
class InvalidAspectRatioFormat(Exception): 
    """
    raises when an aspect ratio string is not set up like [ratio1]:[ratio2]
    """
class NegativeScreenUnitError(Exception): 
    """
    raises when a screenunit of any type is set to a negative value or 0
    """

# window
class NoWindowSizeError(Exception): ...
class MultipleWindowsInSingleWindowAppError(Exception): ... # TODO remove if not needed