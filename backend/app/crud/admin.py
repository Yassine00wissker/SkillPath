from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate
from app.core.security import get_password_hash


async def create_admin(db: AsyncSession, admin: AdminCreate) -> Admin:
    """Create a new admin."""
    hashed_password = get_password_hash(admin.password)
    db_admin = Admin(
        nom=admin.nom,
        prenom=admin.prenom,
        email=admin.email,
        password=hashed_password
    )
    db.add(db_admin)
    await db.commit()
    await db.refresh(db_admin)
    return db_admin


async def get_admin(db: AsyncSession, admin_id: int) -> Optional[Admin]:
    """Get an admin by ID."""
    result = await db.execute(select(Admin).where(Admin.id == admin_id))
    return result.scalar_one_or_none()


async def get_admin_by_email(db: AsyncSession, email: str) -> Optional[Admin]:
    """Get an admin by email."""
    result = await db.execute(select(Admin).where(Admin.email == email))
    return result.scalar_one_or_none()


async def get_admins(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Admin]:
    """Get all admins."""
    result = await db.execute(select(Admin).offset(skip).limit(limit))
    return result.scalars().all()


async def update_admin(db: AsyncSession, admin_id: int, admin_update: AdminUpdate) -> Optional[Admin]:
    """Update an admin."""
    db_admin = await get_admin(db, admin_id)
    if not db_admin:
        return None
    
    update_data = admin_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    for field, value in update_data.items():
        setattr(db_admin, field, value)
    
    await db.commit()
    await db.refresh(db_admin)
    return db_admin


async def delete_admin(db: AsyncSession, admin_id: int) -> bool:
    """Delete an admin."""
    db_admin = await get_admin(db, admin_id)
    if not db_admin:
        return False
    
    await db.delete(db_admin)
    await db.commit()
    return True
