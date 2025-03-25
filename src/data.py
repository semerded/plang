from random import choice
from typing import TYPE_CHECKING
from .typedef import path

if TYPE_CHECKING:
    from .core.window.window import Window
    from .core.window.event import Event
    from .core.base.OID import OID

debugging: bool = None


_emoji_list: tuple[str] = ("(°O°)", ":{)", "O_o", "OwO", "UwU", "(>_<)", "(^_^)", "(T_T)",)
def get_default_window_name() -> str:
    return f"PLANG window {choice(_emoji_list)}"

window_tracker: dict[str, 'Window'] = {}
active_window_id: int = -1
event: 'Event' = None

dll_path: path = None
cwd: path = None
lib_path: path = None

# config file vars
log_file_location: path = None
add_console_timestamp: bool = None
logging_enabled: bool = None
log_file_limit: int = None
logger_file_name: str = None
print_stacktrace: bool = None

def get_dll_path() -> path:
    return dll_path