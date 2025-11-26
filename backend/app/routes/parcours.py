from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.core.security import get_current_user, get_current_admin, get_current_content_creator
from app.models.user import User
from app.models.admin import Admin
from app.crud import parcours as crud_parcours
from app.schemas.parcours import ParcoursCreate, ParcoursUpdate, ParcoursResponse

router = APIRouter(prefix="/parcours", tags=["parcours"])


@router.post("/", response_model=ParcoursResponse, status_code=status.HTTP_201_CREATED)
async def create_parcours(
    parcours: ParcoursCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_content_creator)
):
    """Create a new parcours (Content Creator only)."""
    return await crud_parcours.create_parcours(db, parcours)


@router.get("/", response_model=List[ParcoursResponse])
async def get_parcours_list(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all parcours (Authenticated users only)."""
    parcours_list = await crud_parcours.get_parcours_list(db, skip=skip, limit=limit)
    return parcours_list


@router.get("/{parcours_id}", response_model=ParcoursResponse)
async def get_parcours(
    parcours_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a parcours by ID (Authenticated users only)."""
    parcours = await crud_parcours.get_parcours(db, parcours_id)
    if not parcours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours not found"
        )
    return parcours


@router.put("/{parcours_id}", response_model=ParcoursResponse)
async def update_parcours(
    parcours_id: int,
    parcours_update: ParcoursUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_content_creator)
):
    """Update a parcours (Content Creator only)."""
    parcours = await crud_parcours.update_parcours(db, parcours_id, parcours_update)
    if not parcours:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours not found"
        )
    return parcours


@router.delete("/{parcours_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_parcours(
    parcours_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_content_creator)
):
    """Delete a parcours (Content Creator only)."""
    success = await crud_parcours.delete_parcours(db, parcours_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parcours not found"
        )
    return None
