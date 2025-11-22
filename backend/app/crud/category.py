from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def create_category(db: AsyncSession, category: CategoryCreate) -> Category:
    """Create a new category."""
    db_category = Category(nom=category.nom)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def get_category(db: AsyncSession, category_id: int) -> Optional[Category]:
    """Get a category by ID."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    """Get all categories."""
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


async def update_category(db: AsyncSession, category_id: int, category_update: CategoryUpdate) -> Optional[Category]:
    """Update a category."""
    db_category = await get_category(db, category_id)
    if not db_category:
        return None
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    """Delete a category."""
    db_category = await get_category(db, category_id)
    if not db_category:
        return False
    
    await db.delete(db_category)
    await db.commit()
    return True
