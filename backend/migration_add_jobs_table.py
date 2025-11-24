"""
Migration script to create the jobs table.
Run this script to add the jobs table to your database.
"""
import asyncio
import sys
from sqlalchemy import text
from app.config.database import AsyncSessionLocal, engine
from app.models.job import Job
from app.config.database import Base


async def migrate():
    """Create the jobs table if it doesn't exist."""
    try:
        async with engine.begin() as conn:
            # Check if table exists
            result = await conn.execute(
                text("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE() 
                    AND table_name = 'jobs'
                """)
            )
            table_exists = result.scalar() > 0

            if not table_exists:
                print("Creating jobs table...")
                # Create the table
                await conn.run_sync(Base.metadata.create_all)
                print("Jobs table created successfully!")
            else:
                print("Jobs table already exists.")
        
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(migrate())

