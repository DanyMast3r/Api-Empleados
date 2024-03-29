from typing import Optional
from pydantic import BaseModel, Field

class Data(BaseModel):
    id: Optional[str] = Field(None)
    calname: str
    username: str
    comentario: Optional[str] = Field(None)
    calificacion: str