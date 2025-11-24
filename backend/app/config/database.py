import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Database URL - Update with your MySQL credentials
# Can be overridden with DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://root:@localhost/skillpath")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
