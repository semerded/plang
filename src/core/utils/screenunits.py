from ...typedef import *
from ... import data, exceptions


def dw(screen_unit: float) -> float:
    """
    display width
    """
    return data.display_width / 100 * screen_unit


def dh(screen_unit: float) -> float:
    """
    display height
    """
    return data.display_height / 100 * screen_unit


class screen_units:
    def __init__(self, width: screen_unit, height: screen_unit) -> None:
        if width <= 0:
            raise exceptions.Negativescreen_unitError("givin width is smaller or equal to 0")
        elif height <= 0:
            raise exceptions.Negativescreen_unitError("givin height is smaller or equal to 0")

        self.width = width
        self.height = height

    def vw(self, screen_unit: float) -> float:
        """
        view width 
        """
        return self.width / 100 * screen_unit

    def vh(self, screen_unit: float) -> float:
        """
        view height
        """
        return self.height / 100 * screen_unit

    def w_center(self, offset: screen_unit = 0) -> float:
        """
        width (horizontal) center
        """
        return (self.width - offset) / 2

    def h_center(self, offset: screen_unit = 0) -> float:
        """
        height (vertical) center
        """
        return (self.height - offset) / 2

    def resize(self, width: screen_unit, height: screen_unit) -> None:
        self.width = width
        self.height = height
