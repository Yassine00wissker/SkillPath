from sqlalchemy import Column, Integer, String, Text, JSON
from app.config.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    # Keep attribute name `titre` for API compatibility, map to existing `title` column
    titre = Column("title", String(255), nullable=False)
    description = Column(Text, nullable=True)
    requirements = Column(JSON, default=list)  # List of required skills
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)

