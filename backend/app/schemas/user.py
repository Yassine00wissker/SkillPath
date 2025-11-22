from pydantic import BaseModel, EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    nom: str
    prenom: str
    email: EmailStr
    competence: List[str] = []
    interests: List[str] = []


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    nom: Optional[str] = None
    prenom: Optional[str] = None
    email: Optional[EmailStr] = None
    competence: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
