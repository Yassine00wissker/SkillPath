from pydantic import BaseModel
from typing import List, Optional


class ParcoursBase(BaseModel):
    titre: str
    description: Optional[str] = None
    listedeformations: List[int] = []


class ParcoursCreate(ParcoursBase):
    pass


class ParcoursUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    listedeformations: Optional[List[int]] = None


class ParcoursResponse(ParcoursBase):
    id: int

    class Config:
        from_attributes = True
