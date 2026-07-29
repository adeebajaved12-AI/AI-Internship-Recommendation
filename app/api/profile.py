from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.student import StudentProfile
from pydantic import BaseModel
from app.services.resume_parser import parse_resume_pdf

router = APIRouter()

class ProfileCreate(BaseModel):
    name: str
    university: str
    skills: str
    cv_link: str = None
    user_id: int

@router.post("/create-profile")
def create_profile(profile_data: ProfileCreate, db: Session = Depends(get_db)):
    new_profile = StudentProfile(
        name=profile_data.name,
        degree=profile_data.university,
        skills=profile_data.skills,
        user_id=profile_data.user_id
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"message": "Profile created successfully", "profile_id": new_profile.id}