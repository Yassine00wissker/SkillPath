from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional
from pydantic import BaseModel
from app.config.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.crud import formation as crud_formation
from app.crud import job as crud_job
from app.core.recommender import recommend_keyword
from app.core.gemini_client import build_gemini_prompt, send_skillpath_request

router = APIRouter(prefix="/api/recommend", tags=["recommendations"])


class RecommendSubmitRequest(BaseModel):
    goal: str
    competences: List[str] = []
    interests: List[str] = []
    mode: str = "keyword"  # "keyword" or "ai"
    top_n: Optional[int] = 5


@router.post("/submit")
async def recommend_submit(
    request: RecommendSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a recommendation request with user-provided form data.
    Returns a skillpath structure with steps, recommended jobs, and formations.
    Requires authentication (non-guest).
    """
    # Validate inputs
    if request.mode == "ai" and not request.goal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Goal is required for AI mode"
        )
    
    # Get all formations and jobs from database
    all_formations = await crud_formation.get_formations(db, skip=0, limit=1000)
    all_jobs = await crud_job.get_jobs(db, skip=0, limit=1000)
    
    if request.mode == "ai":
        try:
            # Prepare candidates for Gemini
            candidates = []
            for formation in all_formations[:30]:
                candidates.append({
                    "id": formation.id,
                    "type": "formation",
                    "title": formation.titre,
                    "titre": formation.titre,
                    "description": formation.description or "",
                    "skills": []  # Formations don't have skills in current schema
                })
            
            for job in all_jobs[:30]:
                candidates.append({
                    "id": job.id,
                    "type": "job",
                    "title": job.titre,
                    "titre": job.titre,
                    "description": job.description or "",
                    "requirements": job.requirements or [],
                    "skills": job.requirements or []
                })
            
            # Build prompt
            prompt = build_gemini_prompt(
                goal=request.goal,
                competences=request.competences,
                interests=request.interests,
                candidates=candidates
            )
            
            # Call Gemini
            skillpath = await send_skillpath_request(prompt)
            
            # Validate and ensure IDs exist
            # Verify formation IDs
            valid_formation_ids = {f.id for f in all_formations}
            valid_job_ids = {j.id for j in all_jobs}
            
            # Clean up steps resources
            if "steps" in skillpath:
                for step in skillpath["steps"]:
                    if "resources" in step:
                        valid_resources = []
                        for resource in step["resources"]:
                            if resource.get("type") == "formation" and resource.get("id"):
                                if resource["id"] in valid_formation_ids:
                                    valid_resources.append(resource)
                            elif resource.get("type") == "job" and resource.get("id"):
                                if resource["id"] in valid_job_ids:
                                    valid_resources.append(resource)
                            elif resource.get("type") == "external":
                                valid_resources.append(resource)
                        step["resources"] = valid_resources
            
            # Clean up recommended lists
            if "recommended_formations" in skillpath:
                skillpath["recommended_formations"] = [
                    f for f in skillpath["recommended_formations"]
                    if f.get("id") in valid_formation_ids
                ]
            
            if "recommended_jobs" in skillpath:
                skillpath["recommended_jobs"] = [
                    j for j in skillpath["recommended_jobs"]
                    if j.get("id") in valid_job_ids
                ]
            
            return {
                "source": "ai",
                "skillpath": skillpath
            }
        
        except Exception as e:
            # Fallback to keyword recommender
            skillpath = await recommend_keyword(
                formations=all_formations,
                jobs=all_jobs,
                competences=request.competences,
                interests=request.interests,
                goal=request.goal,
                top_n=request.top_n
            )
            
            return {
                "source": "keyword",
                "fallback_reason": f"AI service error: {str(e)}",
                "skillpath": skillpath
            }
    
    else:  # keyword mode
        skillpath = await recommend_keyword(
            formations=all_formations,
            jobs=all_jobs,
            competences=request.competences,
            interests=request.interests,
            goal=request.goal,
            top_n=request.top_n
        )
        
        return {
            "source": "keyword",
            "skillpath": skillpath
        }
