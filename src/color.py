import random
from .typedef import RGBAvalue, RGBvalue
from .messenger import Messenger
from .exceptions import ColorError

class Color:
    # TODO add argb

    # red
    RED = (255, 0, 0, 255)
    LESS_RED = (200, 0, 0, 255)
    LAVA_RED = (255, 40, 0, 255)
    ORANGE = (255, 80, 0, 255)
    YELLOW = (255, 255, 0, 255)
    SAFFRON = (244, 201, 93, 255)
    LESS_YELLOW = (200, 200, 0, 255)
    PINK = (255, 192, 203, 255)
    REDWOOD = (175, 93, 99, 255)
    ECRU = (193, 174, 124, 255)
    BITTERSWEET = (254, 95, 85, 255)

    # green
    GREEN = (0, 255, 0, 255)
    LESS_GREEN = (0, 200, 0, 255)
    OLIVE_GREEN = (0, 150, 0, 255)
    DARK_GREEN = (0, 100, 0, 255)
    BRUNSWICK_GREEN = (41, 73, 54, 255)
    TURQUISE = (0, 255, 255, 255)
    LESS_TURQUISE = (0, 200, 200, 255)
    AQUAMARINE = (80, 255, 177, 255)
    TEA_GREEN = (199, 239, 207, 255)
    SPRING_GREEN = (89, 255, 160, 255)
    LIGHT_GREEN = (171, 250, 169, 255)

    # blue
    BLUE = (0, 0, 255, 255)
    LESS_BLUE = (0, 0, 200, 255)
    LIGHT_BLUE = (0, 120, 255, 255)
    MOONSTONE = (70, 177, 201, 255)
    PURPLE = (255, 0, 255, 255)
    RUSSIAN_VIOLET = (50, 14, 59, 255)
    STEEL_PINK = (204, 75, 194, 255)
    NAVY_BLUE = (21, 5, 120, 255)
    VIOLET_BLUE = (57, 67, 183, 255)
    SKY_BLUE = (120, 192, 224, 255)
    CELESTIAL_BLUE = (68, 157, 209, 255)
    DARK_PURPLE = (34, 3, 31, 255)

    # rest
    BLACK = (0, 0, 0, 255)
    WHITE = (255, 255, 255, 255)
    BEIGE = (238, 245, 219, 255)
    GHOST_WHITE = (233, 236, 245, 255)
    LESS_WHITE = (200, 200, 200, 255)
    GRAY = GREY = (100, 100, 100, 255)
    BLACK_OLIVE = (67, 74, 66, 255)
    LIGHT_GRAY = LIGHT_GREY = (150, 150, 150, 255)
    DARK_GRAY = DARK_GREY = (50, 50, 50, 255)
    DARKMODE = (30, 30, 30, 255)
    LICORICE = (17, 11, 17, 255)
    CREAM = (242, 244, 203, 255)
    COFFEE = (100, 69, 54, 255)
    CAFE_NOIR = (86, 63, 27, 255)
    EERIE_BLACK = (25, 23, 22, 255)
    BROWN = (150, 75, 0, 255)
    GOLD = (212, 175, 55, 255)

    @staticmethod
    def random():
        return tuple([random.randint(0, 255) for c in range(3)])

    @staticmethod
    def _handle_rgb_rgba(color: (RGBvalue | RGBAvalue)) -> (RGBvalue | RGBAvalue):
        if len(color) < 3:
            Messenger.fatalError(ColorError(f"Length of color tuple|list is shorter than 3 -> {color}\ncorrect notation: (R, G, B, [optional] A)"))
        elif len(color) > 4:
            Messenger.fatalError(ColorError(f"Length of color tuple|list is longer than 4 -> {color}\ncorrect notation: (R, G, B, [optional] A)"))
        for _color in color:
            if _color not in range(0, 256):
                Messenger.fatalError(ColorError(f"{_color} is out of range 0-255 in {color}"))
        return color
