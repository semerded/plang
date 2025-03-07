import uuid

class OID:
    """
    creates an object ID
    """
    def __init__(self) -> None:
        self.OID: uuid.UUID = uuid.uuid4()
        
    def __call__(self) -> str:
        return self.OID.__str__()
    
    def __str__(self) -> str:
        return self.OID.__str__()