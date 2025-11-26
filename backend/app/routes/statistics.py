from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict
from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.formation import Formation
from app.models.category import Category
from app.models.parcours import Parcours
from pydantic import BaseModel

router = APIRouter(prefix="/api/statistics", tags=["statistics"])


class StatisticsResponse(BaseModel):
    total_users: int
    total_formations: int
    total_categories: int
    total_parcours: int
    user_stats: Dict


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get platform statistics. Available to all authenticated users."""
    try:
        # Count users
        users_result = await db.execute(select(func.count(User.id)))
        total_users = users_result.scalar() or 0
        
        # Count formations
        formations_result = await db.execute(select(func.count(Formation.id)))
        total_formations = formations_result.scalar() or 0
        
        # Count categories
        categories_result = await db.execute(select(func.count(Category.id)))
        total_categories = categories_result.scalar() or 0
        
        # Count parcours
        parcours_result = await db.execute(select(func.count(Parcours.id)))
        total_parcours = parcours_result.scalar() or 0
        
        # User-specific stats
        user_stats = {
            "competence_count": len(current_user.competence or []),
            "interests_count": len(current_user.interests or []),
            "role": current_user.role or "user"
        }
        
        # Get saved items count from localStorage (frontend will handle this)
        # For now, we'll just return the structure
        
        return {
            "total_users": total_users,
            "total_formations": total_formations,
            "total_categories": total_categories,
            "total_parcours": total_parcours,
            "user_stats": user_stats
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching statistics: {str(e)}"
        )

