from ..core.handler.OID import OID
from ..core.window.window import Window

class ScreenObject:
    def __init__(self, window: Window) -> None:
        self.oid = OID()
        self.window = window
        
    def _cycle(self):
        pass
