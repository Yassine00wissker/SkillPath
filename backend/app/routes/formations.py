from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.config.database import get_db
from app.core.security import get_current_admin
from app.models.admin import Admin
from app.crud import formation as crud_formation
from app.crud import category as crud_category
from app.schemas.formation import FormationCreate, FormationUpdate, FormationResponse

router = APIRouter(prefix="/formations", tags=["formations"])


@router.post("/", response_model=FormationResponse, status_code=status.HTTP_201_CREATED)
async def create_formation(
    formation: FormationCreate, 
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new formation (Admin only)."""
    # Verify category exists
    category = await crud_category.get_category(db, formation.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return await crud_formation.create_formation(db, formation)


@router.get("/", response_model=List[FormationResponse])
async def get_formations(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    """Get all formations (Public - no authentication required)."""
    formations = await crud_formation.get_formations(db, skip=skip, limit=limit)
    return formations


@router.get("/{formation_id}", response_model=FormationResponse)
async def get_formation(
    formation_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """Get a formation by ID (Public - no authentication required)."""
    formation = await crud_formation.get_formation(db, formation_id)
    if not formation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation not found"
        )
    return formation


@router.put("/{formation_id}", response_model=FormationResponse)
async def update_formation(
    formation_id: int,
    formation_update: FormationUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update a formation (Admin only)."""
    # Verify category exists if category_id is being updated
    if formation_update.category_id:
        category = await crud_category.get_category(db, formation_update.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
    
    formation = await crud_formation.update_formation(db, formation_id, formation_update)
    if not formation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation not found"
        )
    return formation


@router.delete("/{formation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_formation(
    formation_id: int, 
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a formation (Admin only)."""
    success = await crud_formation.delete_formation(db, formation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Formation not found"
        )
    return None
