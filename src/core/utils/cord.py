from ...typedef import *

class Cord: 
    """
    
    """
    
    def __init__(self, x: screenUnit, y: screenUnit) -> None:
        self.x: screenUnit = x
        self.y: screenUnit = y
        
    def equals(self, cord: Cord):
        return self.x == cord.x and self.y == cord.y
    
    def difference(self, cord: Cord):
        raise NotImplementedError