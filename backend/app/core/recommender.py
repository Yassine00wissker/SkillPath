from typing import List, Dict, Tuple, Optional
from app.models.formation import Formation
from app.models.job import Job


def score_formation(formation: Formation, competences: List[str], interests: List[str]) -> Tuple[Formation, float]:
    """Score a formation based on keyword matches."""
    score = 0
    max_score = 0
    
    # Combine title and description
    search_text = f"{formation.titre} {formation.description or ''}".lower()
    
    # All user keywords
    user_keywords = [comp.lower() for comp in competences] + [interest.lower() for interest in interests]
    max_score = len(user_keywords) * 2  # Max possible score
    
    # Check competence matches (weight: 2)
    for comp in competences:
        if comp.lower() in search_text:
            score += 2
    
    # Check interest matches (weight: 1)
    for interest in interests:
        if interest.lower() in search_text:
            score += 1
    
    # Normalize score (0-1)
    normalized_score = score / max_score if max_score > 0 else 0.0
    
    return formation, normalized_score


def score_job(job: Job, competences: List[str], interests: List[str]) -> Tuple[Job, float]:
    """Score a job based on skill matches."""
    score = 0
    job_requirements = [req.lower() for req in (job.requirements or [])]
    user_skills = [skill.lower() for skill in competences + interests]
    
    max_score = len(job_requirements) if job_requirements else 1
    
    # Count matches
    for skill in user_skills:
        if skill in job_requirements:
            score += 1
    
    # Normalize score (0-1)
    normalized_score = score / max_score if max_score > 0 else 0.0
    
    return job, normalized_score


async def recommend_keyword(
    formations: List[Formation],
    jobs: List[Job],
    competences: List[str],
    interests: List[str],
    goal: Optional[str] = None,
    top_n: int = 5
) -> Dict:
    """Recommend formations and jobs based on keyword matching. Returns skillpath structure."""
    # Score formations
    scored_formations = [
        score_formation(formation, competences, interests)
        for formation in formations
    ]
    
    # Sort by score (descending) and filter out zero scores
    scored_formations.sort(key=lambda x: x[1], reverse=True)
    top_formations = [
        {
            "id": f.id,
            "titre": f.titre,
            "score": round(score, 2),
            "match_reason": f"Matches your skills: {', '.join([c for c in competences if c.lower() in (f.titre + ' ' + (f.description or '')).lower()][:2])}"
        }
        for f, score in scored_formations[:top_n] if score > 0
    ]
    
    # Score jobs
    scored_jobs = [
        score_job(job, competences, interests)
        for job in jobs
    ]
    
    # Sort by score (descending) and filter out zero scores
    scored_jobs.sort(key=lambda x: x[1], reverse=True)
    top_jobs = [
        {
            "id": job.id,
            "titre": job.titre,
            "score": round(score, 2),
            "match_reason": f"Matches your skills: {', '.join([c for c in competences if c.lower() in (job.titre + ' ' + (job.description or '')).lower()][:2])}"
        }
        for job, score in scored_jobs[:top_n] if score > 0
    ]
    
    # Build simple skillpath structure
    goal_text = goal or "Achieve your career goals"
    steps = []
    if top_formations:
        steps.append({
            "id": "step-1",
            "title": "Start with recommended formations",
            "duration_weeks": 4,
            "progress_estimate": "beginner->intermediate",
            "resources": [
                {"type": "formation", "id": f["id"], "titre": f["titre"], "url": None, "score": f["score"]}
                for f in top_formations[:3]
            ],
            "explanation": "Build foundation with these courses"
        })
    if top_jobs:
        steps.append({
            "id": "step-2",
            "title": "Explore career opportunities",
            "duration_weeks": 2,
            "progress_estimate": "exploration",
            "resources": [
                {"type": "job", "id": j["id"], "titre": j["titre"], "url": None, "score": j["score"]}
                for j in top_jobs[:3]
            ],
            "explanation": "Review jobs matching your profile"
        })
    
    return {
        "title": goal_text[:50] if goal else "Your Learning Path",
        "summary": f"Personalized recommendations based on your {len(competences)} skills and {len(interests)} interests.",
        "steps": steps[:5],  # Limit to 5 steps
        "recommended_jobs": top_jobs,
        "recommended_formations": top_formations
    }

