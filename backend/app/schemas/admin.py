from pydantic import BaseModel, EmailStr
from typing import Optional


class AdminBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class AdminResponse(AdminBase):
    id: int

    class Config:
        from_attributes = True
