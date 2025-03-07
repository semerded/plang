from ....widget.core.widget import Widget
from ....color import Color
from ....typedef import screen_unit

class Checkbox(Widget):
    def __init__(self, window, x, y, width, height, color = Color.WHITE):
        super().__init__(window, x, y, width, height, color)