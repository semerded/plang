import uuid

class OID:
    """
    creates an object ID
    """
    def __init__(self) -> None:
        self.OID: str = uuid.uuid4()