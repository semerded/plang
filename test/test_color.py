import pytest
from src.color import Color

def test_random_color():
    for i in range(255): # test 255 times to rule out the randomness
        color = Color.random()
        for c in color:
            assert c in range(0, 256)