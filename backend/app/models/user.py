from sqlalchemy import Column, Integer, String, JSON
from app.config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    competence = Column(JSON, default=list)
    interests = Column(JSON, default=list)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # user, content_creator, admin
