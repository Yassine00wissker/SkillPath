from pydantic import BaseModel
from typing import List, Optional


class JobBase(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: List[str] = []
    company: Optional[str] = None
    location: Optional[str] = None


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    company: Optional[str] = None
    location: Optional[str] = None


class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True

