from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate


async def create_job(db: AsyncSession, job: JobCreate) -> Job:
    """Create a new job."""
    db_job = Job(
        titre=job.titre,
        description=job.description,
        requirements=job.requirements,
        company=job.company,
        location=job.location
    )
    db.add(db_job)
    await db.commit()
    await db.refresh(db_job)
    return db_job


async def get_job(db: AsyncSession, job_id: int) -> Optional[Job]:
    """Get a job by ID."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    return result.scalar_one_or_none()


async def get_jobs(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Job]:
    """Get all jobs."""
    result = await db.execute(select(Job).offset(skip).limit(limit))
    return result.scalars().all()


async def update_job(db: AsyncSession, job_id: int, job_update: JobUpdate) -> Optional[Job]:
    """Update a job."""
    db_job = await get_job(db, job_id)
    if not db_job:
        return None
    
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    await db.commit()
    await db.refresh(db_job)
    return db_job


async def delete_job(db: AsyncSession, job_id: int) -> bool:
    """Delete a job."""
    db_job = await get_job(db, job_id)
    if not db_job:
        return False
    
    await db.delete(db_job)
    await db.commit()
    return True

