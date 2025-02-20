from random import choice
from .typedef import *

debugging: bool = False

single_window_app: bool = True


display_info = None
display_width: screenUnit = None
display_height: screenUnit = None

primary_display: int = 0    
window_count: int = 0

_emoji_list: tuple[str] = ("(°O°)", ":{)", "O_o", "OwO", "UwU", "(>_<)", "(^_^)", "(T_T)",)
default_window_name: str = f"PLANG window {choice(_emoji_list)}"


