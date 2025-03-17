import pytest
from src.core.window.rect import Rect

def test_rect():
    rect = Rect(100, 200, 300, 400)
    assert rect.unpack() == (100, 200, 300, 400)
    
def test_rect_from_circle():
    rect: Rect = Rect.from_circle((200, 150), 100)
    assert rect.unpack() == (100, 50, 200, 200)
    
    
def test_rect_from_polygon():
    rect: Rect = Rect.from_polygon(((50, 100), (75, 75), (200, 100), (100, 100), (150, 150)))
    assert rect.unpack() == (50, 75, 150, 75)
    
@pytest.mark.parametrize("screen_unit, expected", [(50, 50), (80, 80)])
def test_rw(screen_unit, expected):
    rect = Rect(0, 0, 100, 50)
    assert rect.rw(screen_unit) == expected

@pytest.mark.parametrize("screen_unit, expected", [(50, 25), (80, 40)])
def test_rh(screen_unit, expected):
    rect = Rect(0, 0, 100, 50)
    assert rect.rh(screen_unit) == expected

@pytest.mark.parametrize("screen_unit, expected", [(50, 150), (80, 180)])
def test_aw(screen_unit, expected):
    rect = Rect(100, 0, 100, 50)
    assert rect.aw(screen_unit) == expected

@pytest.mark.parametrize("screen_unit, expected", [(50, 75), (80, 90)])
def test_ah(screen_unit, expected):
    rect = Rect(0, 50, 100, 50)
    assert rect.ah(screen_unit) == expected

def test_expand_shrink_width():
    rect = Rect(50, 50, 100, 50)
    rect.expand_width(20)
    assert rect.w == 120 and rect.x == 40

    rect.shrink_width(20)
    assert rect.w == 100 and rect.x == 50

def test_expand_shrink_height():
    rect = Rect(50, 50, 100, 50)
    rect.expand_height(20)
    assert rect.h == 70 and rect.y == 40

    rect.shrink_height(20)
    assert rect.h == 50 and rect.y == 50

def test_place_holder():
    rect = Rect.place_holder()
    assert rect.unpack() == (0, 0, 0, 0)
    
@pytest.mark.parametrize("x, y, expected", [(100, 100, True), (99, 100, False), (300, 120, True), (301, 120, False), (200, 200, True), (200, 201, False)])
def test_point_in_rect(x, y, expected):
    rect = Rect(100, 100, 200, 100)
    assert expected == rect.point_in_rect(x, y)