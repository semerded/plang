from random import choice
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core.window.window import Window
    from .core.window.event import Event
    from .core.base.OID import OID

debugging: bool = True


_emoji_list: tuple[str] = ("(°O°)", ":{)", "O_o", "OwO", "UwU", "(>_<)", "(^_^)", "(T_T)",)
default_window_name: str = f"PLANG window {choice(_emoji_list)}"

window_tracker: dict[str, 'Window'] = {}
active_window_id: int = -1
event: 'Event' = None
