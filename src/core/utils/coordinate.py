from ...typedef import *
from ...messenger import Messenger
from ...exceptions import ExpectedLengthError, OutOfWindowBoundsError
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ...core.window.window import Window

class Coordinate:
    def __init__(self, x: screen_unit, y: screen_unit):
        self.x = x
        self.y = y
        
    
    @staticmethod
    def check_input(input: 'Coordinate', strict_positive: bool = False, strict_in_window_bounds: bool = False, window: Optional['Window'] = None) -> 'Coordinate':
        if len(input) == 2:
            if strict_positive:
                if input[0] < 0:
                    Messenger.error(ValueError(f"expected a positive value for x coordinate -> {input[1]}"))
                if input[1] < 0:
                    Messenger.error(ValueError(f"expected a positive value for y coordinate -> {input[0]}"))
            
            if strict_in_window_bounds:
                if window == None:
                    Messenger.warning("coordinate check 'strict_in_window_bounds' set to True but no window given")
                if input[0] not in range(0, window.width):
                    Messenger.error(OutOfWindowBoundsError(f"x coordinate out of window bound found when checking for coordinate out of window bounds -> x:{input[0]} | window width range: 0 - {window.width}"))
                if input[1] not in range(0, window.height):
                    Messenger.error(OutOfWindowBoundsError(f"y coordinate out of window bound found when checking for coordinate out of window bounds: -> y:{input[1]} | window height range: 0 - {window.height}"))                    
                
        else:
            if len(input) < 2:
                Messenger.fatalError(ExpectedLengthError(f"Coordinate length of [2] is not met: actual length = {len(input)}"))
            else:
                Messenger.fatalError(ExpectedLengthError(f"Coordinate length of [2] exceeded: actual length = {len(input)}"))
        return input
    
    def equals(self, cord: 'Coordinate'):
        Coordinate.check_input(cord)
        return self.x == cord.x and self.y == cord.y
    
    def difference(self, cord: 'Coordinate'):
        Coordinate.check_input(cord)
        return (abs(self.x - cord[0]), abs(self.y - cord[1]))