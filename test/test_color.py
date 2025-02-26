import pytest
from src.color import Color
from src.exceptions import ColorError

def test_random_color():
    for i in range(255): # test 255 times to rule out the randomness
        color = Color.random()
        for c in color:
            assert c in range(0, 256)
            
def test_color_handler(capsys):
    assert Color._handle_rgb_rgba((255, 0, 255)) == (255, 0, 255)
    assert Color._handle_rgb_rgba([200, 200, 200, 200]) == [200, 200, 200, 200]
    
    with pytest.raises(ColorError):
        Color._handle_rgb_rgba((255, 0))
        captured = capsys.readouterr()
        assert "shorter than 3" in captured.out

        Color._handle_rgb_rgba((255, 0, 0, 255, 0))
        captured = capsys.readouterr()
        assert "longer than 4" in captured.out
        
        Color._handle_rgb_rgba((-5, 0, 5))
        captured = capsys.readouterr()
        assert "out of range" in captured.out
        
        Color._handle_rgb_rgba((256, 0, 0))
        captured = capsys.readouterr()
        assert "out of range" in captured.out