import pytest

from src.core.utils import aspect_ratio
from src import exceptions

def test_get_width_from_aspect_ratio():
    assert 500 == aspect_ratio.get_width_from_aspect_ratio("5:10", 1000) == 500
    
def test_get_height_from_aspect_ratio():
    assert 1000 == aspect_ratio.get_height_from_aspect_ratio("5:10", 500)

def test_convert_aspect_ratio():
    assert 0.5 == aspect_ratio.convert_aspect_ratio("5:10")
    assert 2 == aspect_ratio.convert_aspect_ratio("2:1")
    assert 1 == aspect_ratio.convert_aspect_ratio("1:1")
    
    with pytest.raises(exceptions.InvalidAspectRatioFormat):
        aspect_ratio.convert_aspect_ratio("1")
    with pytest.raises(exceptions.InvalidAspectRatioFormat):
        aspect_ratio.convert_aspect_ratio("nmb")
    with pytest.raises(exceptions.NegativeAspectRatioError):
        aspect_ratio.convert_aspect_ratio("bub:1")
    with pytest.raises(exceptions.NegativeAspectRatioError):
        aspect_ratio.convert_aspect_ratio("6:rub")
    with pytest.raises(exceptions.NegativeAspectRatioError):
        aspect_ratio.convert_aspect_ratio("-1:6")
    with pytest.raises(exceptions.NegativeAspectRatioError):
        aspect_ratio.convert_aspect_ratio("600:-2000")
    with pytest.raises(exceptions.NegativeAspectRatioError):
        aspect_ratio.convert_aspect_ratio("0:0")

