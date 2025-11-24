from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional
from pydantic import BaseModel
from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.crud import user as crud_user
from app.crud import formation as crud_formation
from app.crud import job as crud_job
from app.core.recommender import recommend_keyword
from app.core.gemini_client import build_gemini_prompt, send_to_gemini

router = APIRouter(prefix="/api/recommend", tags=["recommendations"])


class KeywordRecommendRequest(BaseModel):
    user_id: int
    top_n: Optional[int] = 5


class AIRecommendRequest(BaseModel):
    user_id: int
    mode: str = "enhance"  # "enhance" or "generate"
    top_n: Optional[int] = 5


@router.post("/keyword")
async def recommend_keyword_endpoint(
    request: KeywordRecommendRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get keyword-based recommendations for a user.
    Requires authentication.
    """
    # Fetch user
    user = await crud_user.get_user(db, request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get all formations and jobs
    all_formations = await crud_formation.get_formations(db, skip=0, limit=1000)
    all_jobs = await crud_job.get_jobs(db, skip=0, limit=1000)
    
    # Get user competences and interests
    competences = user.competence or []
    interests = user.interests or []
    
    # Get recommendations
    recommendations = await recommend_keyword(
        all_formations,
        all_jobs,
        competences,
        interests,
        top_n=request.top_n
    )
    
    return {
        "source": "keyword",
        **recommendations
    }


@router.post("/ai")
async def recommend_ai_endpoint(
    request: AIRecommendRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get AI-enhanced recommendations using Gemini.
    Requires authentication.
    Falls back to keyword recommender if Gemini fails.
    """
    # Fetch user
    user = await crud_user.get_user(db, request.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user data as dict
    user_dict = {
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "competence": user.competence or [],
        "interests": user.interests or []
    }
    
    try:
        if request.mode == "enhance":
            # Get all formations and jobs
            all_formations = await crud_formation.get_formations(db, skip=0, limit=1000)
            
            # Prepare candidates
            candidates = []
            for formation in all_formations[:50]:  # Limit to 50
                candidates.append({
                    "id": formation.id,
                    "type": "formation",
                    "title": formation.titre,
                    "description": formation.description or ""
                })
            
            all_jobs = await crud_job.get_jobs(db, skip=0, limit=1000)
            for job in all_jobs[:50]:
                candidates.append({
                    "id": job.id,
                    "type": "job",
                    "title": job.title,
                    "description": job.description or "",
                    "requirements": job.requirements or []
                })
            
            # Build prompt
            prompt = build_gemini_prompt(user_dict, candidates, task="enhance")
            
            # Call Gemini
            gemini_response = await send_to_gemini(prompt)
            
            # Format response
            return {
                "source": "gemini",
                "jobs": gemini_response.get("jobs", []),
                "formations": gemini_response.get("formations", [])
            }
        
        else:  # generate
            # Build prompt for generation
            prompt = build_gemini_prompt(user_dict, [], task="generate")
            
            # Call Gemini
            gemini_response = await send_to_gemini(prompt)
            
            # Format response
            return {
                "source": "gemini",
                "jobs": gemini_response.get("jobs", []),
                "formations": gemini_response.get("formations", [])
            }
    
    except HTTPException as e:
        # If Gemini fails, fallback to keyword recommender
        all_formations = await crud_formation.get_formations(db, skip=0, limit=1000)
        all_jobs = await crud_job.get_jobs(db, skip=0, limit=1000)
        competences = user.competence or []
        interests = user.interests or []
        
        recommendations = await recommend_keyword(
            all_formations,
            all_jobs,
            competences,
            interests,
            top_n=request.top_n
        )
        
        return {
            "source": "keyword",
            "fallback_reason": str(e.detail),
            **recommendations
        }
    except Exception as e:
        # Fallback to keyword recommender on any error
        all_formations = await crud_formation.get_formations(db, skip=0, limit=1000)
        all_jobs = await crud_job.get_jobs(db, skip=0, limit=1000)
        competences = user.competence or []
        interests = user.interests or []
        
        recommendations = await recommend_keyword(
            all_formations,
            all_jobs,
            competences,
            interests,
            top_n=request.top_n
        )
        
        return {
            "source": "keyword",
            "fallback_reason": f"AI service error: {str(e)}",
            **recommendations
        }

