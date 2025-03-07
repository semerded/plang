from ...core.window.interactive_rect import InteractiveRect

class TextBox(InteractiveRect):
    def __init__(self, window, x, y, width, height):
        super().__init__(window, x, y, width, height)