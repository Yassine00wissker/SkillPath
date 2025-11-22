from pydantic import BaseModel
from typing import Optional


class FormationBase(BaseModel):
    titre: str
    description: Optional[str] = None
    video: Optional[str] = None
    category_id: int


class FormationCreate(FormationBase):
    pass


class FormationUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    video: Optional[str] = None
    category_id: Optional[int] = None


class FormationResponse(FormationBase):
    id: int

    class Config:
        from_attributes = True
