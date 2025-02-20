from ...enum import key

class Keyboard:
    def __init__(self) -> None:
        self.active_keys: list = []
        self.released_keys: list = []
        self.clicked_keys: list = []
        
    def _reset_keys(self) -> None:
        self.clicked_keys = []
        self.released_keys = []
    
    #TODO set type for key param
    def is_key_pressed(self, key: key) -> bool:
        return key.value in self.active_keys
    
    def is_key_clicked(self, key: key) -> bool:
        return key.value in self.clicked_keys
    
    def is_key_released(self, key: key) -> bool:
        return key.value in self.released_keys
