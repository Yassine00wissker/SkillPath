from sqlalchemy import Column, Integer, String, JSON, Text
from app.config.database import Base


class Parcours(Base):
    __tablename__ = "parcours"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    listedeformations = Column(JSON, default=list)
