from ...typedef import *
from ... import data, exceptions


def dw(screenUnit: float) -> float:
    """
    display width
    """
    return data.display_width / 100 * screenUnit


def dh(screenUnit: float) -> float:
    """
    display height
    """
    return data.display_height / 100 * screenUnit


class ScreenUnits:
    def __init__(self, width: screenUnit, height: screenUnit) -> None:
        if width <= 0:
            raise exceptions.NegativeScreenUnitError("givin width is smaller or equal to 0")
        elif height <= 0:
            raise exceptions.NegativeScreenUnitError("givin height is smaller or equal to 0")

        self.width = width
        self.height = height

    def vw(self, screenUnit: float) -> float:
        """
        view width 
        """
        return self.width / 100 * screenUnit

    def vh(self, screenUnit: float) -> float:
        """
        view height
        """
        return self.height / 100 * screenUnit

    def w_center(self, offset: screenUnit = 0) -> float:
        """
        width (horizontal) center
        """
        return (self.width - offset) / 2

    def h_center(self, offset: screenUnit = 0) -> float:
        """
        height (vertical) center
        """
        return (self.height - offset) / 2

    def resize(self, width: screenUnit, height: screenUnit) -> None:
        self.width = width
        self.height = height
