from sqlalchemy import Column, Integer, String, Float, Text
from app.database.connection import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    name = Column(String, default="Student")
    email = Column(String, default="Not found")
    degree = Column(String, nullable=True)
    cgpa = Column(Float, nullable=True)
    skills = Column(Text, default="")
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    resume_path = Column(String, nullable=True)