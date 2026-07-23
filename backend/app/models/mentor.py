from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Mentor(Base):
    __tablename__ = "mentors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    expertise_skills = Column(String) # e.g., "python, machine learning, ai"