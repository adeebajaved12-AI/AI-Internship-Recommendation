from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    required_skills = Column(String) 