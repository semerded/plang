import pytest

from src.core.utils.screenunits import screen_units, dw, dh
import src.core.backend
from src import exceptions
from src import data

def test_dw():
    pass    
def test_dh():
    pass

def test_sc_error():
    with pytest.raises(exceptions.Negativescreen_unitError):
        screen_units(-200, 100)
    with pytest.raises(exceptions.Negativescreen_unitError):
        screen_units(100, -200)


def test_vw():
    sc = screen_units(800, 600)
    assert sc.vw(100) == 800
    assert sc.vw(50) == 400
    assert sc.vw(0) == 0
    
def test_vh():
    sc = screen_units(800, 600)
    assert sc.vh(100) == 600
    assert sc.vh(50) == 300
    assert sc.vh(0) == 0
    
def test_w_center():
    sc = screen_units(800, 600)
    assert sc.w_center() == 400
    assert sc.w_center(200) == 300
    assert sc.w_center(400) == 200
    
def test_h_center():
    sc = screen_units(800, 600)
    assert sc.h_center() == 300
    assert sc.h_center(200) == 200
    assert sc.h_center(400) == 100