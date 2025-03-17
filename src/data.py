from random import choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core.window.window import Window
    from .core.window.event import Event

debugging: bool = True


_emoji_list: tuple[str] = ("(°O°)", ":{)", "O_o", "OwO", "UwU", "(>_<)", "(^_^)", "(T_T)",)
default_window_name: str = f"PLANG window {choice(_emoji_list)}"

window_tracker: dict[str, 'Window'] = {}
event: 'Event' = None