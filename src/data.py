from random import choice
from .typedef import *

debugging: bool = False

single_window_app: bool = True


display_info = None
display_width: screen_unit = None
display_height: screen_unit = None

primary_display: int = 0    
window_count: int = 0
widget_pressed: bool = False

_emoji_list: tuple[str] = ("(°O°)", ":{)", "O_o", "OwO", "UwU", "(>_<)", "(^_^)", "(T_T)",)
default_window_name: str = f"PLANG window {choice(_emoji_list)}"


