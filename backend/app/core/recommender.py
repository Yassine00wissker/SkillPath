from typing import List, Dict, Tuple
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
    top_n: int = 5
) -> Dict[str, List]:
    """Recommend formations and jobs based on keyword matching."""
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
            "title": f.titre,
            "description": f.description,
            "score": round(score, 2)
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
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements or [],
            "company": job.company,
            "location": job.location,
            "score": round(score, 2)
        }
        for job, score in scored_jobs[:top_n] if score > 0
    ]
    
    return {
        "formations": top_formations,
        "jobs": top_jobs
    }

