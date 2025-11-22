from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.formation import Formation
from app.schemas.formation import FormationCreate, FormationUpdate


async def create_formation(db: AsyncSession, formation: FormationCreate) -> Formation:
    """Create a new formation."""
    db_formation = Formation(
        titre=formation.titre,
        description=formation.description,
        video=formation.video,
        category_id=formation.category_id
    )
    db.add(db_formation)
    await db.commit()
    await db.refresh(db_formation)
    return db_formation


async def get_formation(db: AsyncSession, formation_id: int) -> Optional[Formation]:
    """Get a formation by ID."""
    result = await db.execute(select(Formation).where(Formation.id == formation_id))
    return result.scalar_one_or_none()


async def get_formations(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Formation]:
    """Get all formations."""
    result = await db.execute(select(Formation).offset(skip).limit(limit))
    return result.scalars().all()


async def update_formation(db: AsyncSession, formation_id: int, formation_update: FormationUpdate) -> Optional[Formation]:
    """Update a formation."""
    db_formation = await get_formation(db, formation_id)
    if not db_formation:
        return None
    
    update_data = formation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_formation, field, value)
    
    await db.commit()
    await db.refresh(db_formation)
    return db_formation


async def delete_formation(db: AsyncSession, formation_id: int) -> bool:
    """Delete a formation."""
    db_formation = await get_formation(db, formation_id)
    if not db_formation:
        return False
    
    await db.delete(db_formation)
    await db.commit()
    return True
