from ...typedef import *

class Cord: 
    """
    
    """
    
    def __init__(self, x: screen_unit, y: screen_unit) -> None:
        self.x: screen_unit = x
        self.y: screen_unit = y
        
    def equals(self, cord: Cord):
        return self.x == cord.x and self.y == cord.y
    
    def difference(self, cord: Cord):
        raise NotImplementedError