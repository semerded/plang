import random
class Color:
    # TODO add argb
    
    # red 
    RED = (255, 0, 0)
    LESS_RED = (200, 0, 0)
    LAVA_RED = (255, 40, 0)
    ORANGE = (255, 80, 0)
    YELLOW = (255, 255, 0)
    SAFFRON = (244, 201, 93)
    LESS_YELLOW = (200, 200, 0)
    PINK = (255, 192, 203)
    REDWOOD = (175, 93, 99)
    ECRU = (193, 174, 124)
    BITTERSWEET = (254, 95, 85)
    
    # green
    GREEN = (0, 255, 0)
    LESS_GREEN = (0, 200, 0)
    OLIVE_GREEN = (0, 150, 0)
    DARK_GREEN = (0, 100, 0)
    BRUNSWICK_GREEN = (41, 73, 54)
    TURQUISE = (0, 255, 255)
    LESS_TURQUISE = (0, 200, 200)
    AQUAMARINE = (80, 255, 177)
    TEA_GREEN = (199, 239, 207)
    SPRING_GREEN = (89, 255, 160)
    LIGHT_GREEN = (171, 250, 169)
    
    # blue
    BLUE = (0, 0, 255)
    LESS_BLUE = (0, 0, 200)
    LIGHT_BLUE = (0, 120, 255)
    MOONSTONE = (70, 177, 201)
    PURPLE = (255, 0, 255)
    RUSSIAN_VIOLET = (50, 14, 59)
    STEEL_PINK = (204, 75, 194)
    NAVY_BLUE = (21, 5, 120)
    VIOLET_BLUE = (57, 67, 183)
    SKY_BLUE = (120, 192, 224)
    CELESTIAL_BLUE = (68, 157, 209)
    DARK_PURPLE = (34, 3, 31)
    
    # rest
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BEIGE = (238, 245, 219)
    GHOST_WHITE = (233, 236, 245)
    LESS_WHITE = (200, 200, 200)
    GRAY = GREY = (100, 100, 100)
    BLACK_OLIVE = (67, 74, 66)
    LIGHT_GRAY = LIGHT_GREY = (150, 150, 150)
    DARK_GRAY = DARK_GREY = (50, 50, 50)
    DARKMODE = (30, 30, 30)   
    LICORICE = (17, 11, 17)
    CREAM = (242, 244, 203)
    COFFEE = (100, 69, 54)
    CAFE_NOIR = (86, 63, 27) 
    EERIE_BLACK = (25, 23, 22)
    BROWN = (150, 75, 0)
    GOLD = (212, 175, 55)

    @staticmethod
    def random():
        return tuple([random.randint(0, 255) for c in range(3)])
