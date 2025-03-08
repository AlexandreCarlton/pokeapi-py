
from pydantic import BaseModel

class PokeApiBaseType(BaseModel):
    """An light abstraction around a BaseModel to facilitate switching out of
    JSON deserialisation libraries."""
    pass
