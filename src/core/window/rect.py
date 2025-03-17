from typing import Annotated
from ...typedef import *
from ..utils.coordinate import Coordinate
from .. import bridge

class Rect():
    """
    A rect is a rectangle defined by x, y, width and height. It is used to define a region on the screen. 
    Rects can be used to detect collisions, either with the mouse or with other rects. 
    They can also be used to update certain parts of the screen
    """
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self._c_rect = bridge.ffi.new("SDL_Rect *", [x, y, width, height])
        
    @classmethod
    def from_circle(cls, center: coordinate, radius: int) -> 'Rect':
        """
        create a rect from a circle\n
        :param center: the center of the circle
        :param radius: the radius of the circle
        :return: a new rect instance
        """
        Coordinate.check_input(center)
        return cls(center[0] - radius, center[1] - radius, radius * 2, radius * 2)

    @classmethod
    def from_polygon(cls, points: tuple[coordinate] | list[coordinate]) -> "Rect":
        """
        create a rect from a list of points\n
        :param points: a list of points
        :return: a new rect instance
        """
        if not points:
            raise ValueError("Points list cannot be empty")
        for point in points:
            Coordinate.check_input(point)
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)
        return cls(min_x, min_y, max_x - min_x, max_y - min_y)

    def pack(self) -> 'Rect':
        """
        packs a rect instance into a new rect instance
        """
        return Rect(self.x, self.y, self.w, self.h)

    def unpack(self) -> Annotated[tuple[int, int, int, int], 4]:
        """
        unpacks a rect instance into a tuple (x, y, w, h)
        """
        return (self.x, self.y, self.w, self.h)

    def rw(self, percent: percent) -> screen_unit:
        """
        a rect's relative width\n
        :param percent: the percentage of the rect's width\n
        :return: the corresponding width\n
        ```
        rect = Rect(100, 200, 400, 150) # x, y, w, h
        print(rect.rw(50)) # = 200
        print(rect.rw(80)) # = 320
        ```
        """
        return self.w * percent / 100

    def rh(self, percent: percent) -> screen_unit:
        """
        a rect's relative height\n
        :param percent: the percentage of the rect's height\n
        :return: the corresponding height\n
        ```
        rect = Rect(100, 200, 400, 150) # x, y, w, h
        print(rect.rh(50)) # = 75
        print(rect.rh(80)) # = 120
        ```
        """
        return self.h * percent / 100

    def aw(self, percent: percent) -> screen_unit:
        """
        a rect's absolute width\n
        :param percent: the percentage of the rect's width\n
        :return: the corresponding width added to the rect's x value\n
        ```
        rect = Rect(100, 200, 400, 150) # x, y, w, h
        print(rect.aw(50)) # = 300
        print(rect.aw(80)) # = 420
        ```
        """
        return self.x + self.rw(percent)

    def ah(self, percent: percent) -> screen_unit:
        """
        a rect's absolute height\n
        :param percent: the percentage of the rect's height\n
        :return: the corresponding height added to the rect's y value\n
        ```
        rect = Rect(100, 200, 400, 150) # x, y, w, h
        print(rect.ah(50)) # = 275
        print(rect.ah(80)) # = 320
        ```
        """
        return self.y + self.rh(percent)

    def expand(self, expansion: screen_unit) -> None:
        """
        expand all sides of a rect\n
        an expansion of 10 will expand the rect by 5 on each side\n
        :param expansion: the amount to expand\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.expand(20) # x, y, w, h = 90, 190, 410, 160
        ```
        """
        self.x -= expansion // 2
        self.y -= expansion // 2
        self.w += expansion
        self.h += expansion

    def shrink(self, shrinkage: screen_unit) -> None:
        """
        shrink all sides of a rect\n
        a shrinkage of 10 will shrink the rect by 5 on each side\n
        :param shrinkage: the amount to shrink\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.shrink(20) # x, y, w, h = 110, 210, 380, 140
        ```
        """
        self.expand(-shrinkage)

    def expand_width(self, expansion: screen_unit) -> None:
        """
        expand the width of a rect\n
        an expansion of 10 will expand the rect by 5 on the left and right\n
        :param expansion: the amount to expand on the left and right\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.expand_width(20) # x, y, w, h = 80, 200, 420, 150
        ```
        """
        self.x -= expansion // 2
        self.w += expansion

    def shrink_width(self, shrinkage: screen_unit) -> None:
        """
        shrink the width of a rect\n
        a shrinkage of 10 will shrink the rect by 5 on the left and right\n
        :param shrinkage: the amount to shrink on the left and right\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.shrink_width(20) # x, y, w, h = 120, 200, 380, 150
        ```
        """
        self.expand_width(-shrinkage)

    def expand_height(self, expansion: screen_unit) -> None:
        """
        expand the height of a rect\n
        an expansion of 10 will expand the rect by 5 on the top and bottom\n
        :param expansion: the amount to expand on the top and bottom\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.expand_height(20) # x, y, w, h = 100, 180, 400, 170
        ```
        """
        self.y -= expansion // 2
        self.h += expansion

    def shrink_height(self, shrinkage: screen_unit) -> None:
        """
        shrink the height of a rect\n
        a shrinkage of 10 will shrink the rect by 5 on the top and bottom\n
        :param shrinkage: the amount to shrink on the top and bottom\n
        ```
        rect = Rect(100, 200, 400, 150)
        rect.shrink_height(20) # x, y, w, h = 100, 220, 400, 130
        ```
        """
        self.expand_height(-shrinkage)

    def resize(self, width: screen_unit, height: screen_unit) -> None:
        """
        resize a rect\n
        :param width: the new width
        :param height: the new height
        """
        self.w = width
        self.h = height

    def reposition(self, x: screen_unit, y: screen_unit) -> None:
        """
        reposition a rect\n
        :param x: the new x position
        :param y: the new y position
        """
        self.x = x
        self.y = y

    def union(self, rect: 'Rect') -> 'Rect':
        """
        Returns the union of two rects\n
        :param rect: the rect to union with the current rect
        :return: the union of the two rects as a new rect instance
        """
        x1 = min(self.x, rect.x)
        y1 = min(self.y, rect.y)
        x2 = max(self.x + self.w, rect.x + rect.w)
        y2 = max(self.y + self.h, rect.y + rect.h)
        return Rect(x1, y1, x2 - x1, y2 - y1)

    def collide_with_point(self, x: screen_unit, y: screen_unit) -> bool:
        """
        Checks if a point is within the rect\n
        :param x: the x position of the point
        :param y: the y position of the point
        :return: True if the point is within the rect, else False
        """
        return min(self.x, self.x + self.w) <= x <= max(self.x, self.x + self.w) and \
               min(self.y, self.y + self.h) <= y <= max(self.y, self.y + self.h)
    
    def collide_with_rect(self, rect: 'Rect') -> bool:
        """
        Checks if two rects collide\n
        :param rect: the rect to test collision with
        :return: True if the rects collide, else False
        """
        return SDL_HasIntersection(self, rect)

    def abs(self) -> None:
        """
        Correct negative width and height to a positive value
        """
        if self.w < 0:
            self.x += self.w
            self.w = -self.w
        if self.h < 0:
            self.y += self.h
            self.h = -self.h

    @staticmethod
    def place_holder() -> "Rect":
        """
        Return a rect at position (0, 0) with a width and height of 0.\n
        Can be used instead of assigning None to a none defined rect\n
        :return: a rect at position (0, 0) with a width and height of 0
        """
        return Rect(0, 0, 0, 0)
