
from pydantic import BaseModel

class Client(BaseModel):
    """Client model representing a client in the system."""
    id: str

