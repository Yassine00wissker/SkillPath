from pydantic import BaseModel
from typing import Optional


class CategoryBase(BaseModel):
    nom: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    nom: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
