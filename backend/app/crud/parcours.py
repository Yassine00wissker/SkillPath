from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.parcours import Parcours
from app.schemas.parcours import ParcoursCreate, ParcoursUpdate


async def create_parcours(db: AsyncSession, parcours: ParcoursCreate) -> Parcours:
    """Create a new parcours."""
    db_parcours = Parcours(
        titre=parcours.titre,
        description=parcours.description,
        listedeformations=parcours.listedeformations
    )
    db.add(db_parcours)
    await db.commit()
    await db.refresh(db_parcours)
    return db_parcours


async def get_parcours(db: AsyncSession, parcours_id: int) -> Optional[Parcours]:
    """Get a parcours by ID."""
    result = await db.execute(select(Parcours).where(Parcours.id == parcours_id))
    return result.scalar_one_or_none()


async def get_parcours_list(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Parcours]:
    """Get all parcours."""
    result = await db.execute(select(Parcours).offset(skip).limit(limit))
    return result.scalars().all()


async def update_parcours(db: AsyncSession, parcours_id: int, parcours_update: ParcoursUpdate) -> Optional[Parcours]:
    """Update a parcours."""
    db_parcours = await get_parcours(db, parcours_id)
    if not db_parcours:
        return None
    
    update_data = parcours_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_parcours, field, value)
    
    await db.commit()
    await db.refresh(db_parcours)
    return db_parcours


async def delete_parcours(db: AsyncSession, parcours_id: int) -> bool:
    """Delete a parcours."""
    db_parcours = await get_parcours(db, parcours_id)
    if not db_parcours:
        return False
    
    await db.delete(db_parcours)
    await db.commit()
    return True
