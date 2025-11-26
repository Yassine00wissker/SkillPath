from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, List
from app.config.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.formation import Formation
from app.models.category import Category
from app.models.parcours import Parcours
from app.models.admin import Admin
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin"])


class AdvancedStatisticsResponse(BaseModel):
    total_users: int
    total_providers: int
    total_regular_users: int
    total_formations: int
    total_categories: int
    total_parcours: int
    total_admins: int
    users_by_role: Dict[str, int]
    recent_registrations: int  # Users registered in last 30 days (placeholder)


@router.get("/statistics", response_model=AdvancedStatisticsResponse)
async def get_admin_statistics(
    db: AsyncSession = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Get advanced platform statistics. Admin only."""
    try:
        # Count total users
        users_result = await db.execute(select(func.count(User.id)))
        total_users = users_result.scalar() or 0
        
        # Count users by role
        users_by_role_result = await db.execute(
            select(User.role, func.count(User.id)).group_by(User.role)
        )
        users_by_role = {}
        total_providers = 0
        total_regular_users = 0
        
        for row in users_by_role_result:
            role = row[0] or "user"
            count = row[1]
            users_by_role[role] = count
            if role == "provider":
                total_providers = count
            elif role == "user":
                total_regular_users = count
        
        # Count formations
        formations_result = await db.execute(select(func.count(Formation.id)))
        total_formations = formations_result.scalar() or 0
        
        # Count categories
        categories_result = await db.execute(select(func.count(Category.id)))
        total_categories = categories_result.scalar() or 0
        
        # Count parcours
        parcours_result = await db.execute(select(func.count(Parcours.id)))
        total_parcours = parcours_result.scalar() or 0
        
        # Count admins
        admins_result = await db.execute(select(func.count(Admin.id)))
        total_admins = admins_result.scalar() or 0
        
        return {
            "total_users": total_users,
            "total_providers": total_providers,
            "total_regular_users": total_regular_users,
            "total_formations": total_formations,
            "total_categories": total_categories,
            "total_parcours": total_parcours,
            "total_admins": total_admins,
            "users_by_role": users_by_role,
            "recent_registrations": 0  # Placeholder - can be enhanced with date filtering
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching admin statistics: {str(e)}"
        )

