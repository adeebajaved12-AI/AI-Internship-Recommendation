import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.student import StudentProfile

from app.services.parser import parse_resume
from app.services.vector_store import add_candidate_to_vector_db

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_resume(

        student_id: int = Form(...),

        file: UploadFile = File(...),

        db: Session = Depends(get_db)

):

    # ------------------------
    # PDF Validation
    # ------------------------

    if not file.filename.endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF Resume Allowed."
        )

    # ------------------------
    # Save PDF
    # ------------------------

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        f"{student_id}_{file.filename}"
    )

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ------------------------
    # Parse Resume
    # ------------------------

    parsed = parse_resume(pdf_path)

    # ------------------------
    # Skills
    # ------------------------

    skills = ", ".join(parsed["skills"])

    # ------------------------
    # Existing Student?
    # ------------------------

    student = db.query(StudentProfile).filter(

        StudentProfile.id == student_id

    ).first()

    # ------------------------
    # Create New
    # ------------------------

    if student is None:

        student = StudentProfile(

            id=student_id,

            name=parsed["name"],

            email=parsed["email"],

            phone=parsed["phone"],

            github=parsed["github"],

            linkedin=parsed["linkedin"],

            skills=skills,

            resume_path=pdf_path

        )

        db.add(student)

    # ------------------------
    # Update Existing
    # ------------------------

    else:

        student.name = parsed["name"]

        student.email = parsed["email"]

        student.phone = parsed["phone"]

        student.github = parsed["github"]

        student.linkedin = parsed["linkedin"]

        student.skills = skills

        student.resume_path = pdf_path

    db.commit()

    db.refresh(student)

    # ------------------------
    # Add Candidate To ChromaDB
    # ------------------------

    add_candidate_to_vector_db(

        candidate_id=str(student.id),

        candidate_name=student.name,

        skills=skills,

        resume_text=parsed["raw_text"]

    )

    # ------------------------
    # Response
    # ------------------------

    return {

        "status": "success",

        "message": "Resume Uploaded Successfully",

        "candidate": {

            "id": student.id,

            "name": student.name,

            "email": student.email,

            "phone": student.phone,

            "github": student.github,

            "linkedin": student.linkedin,

            "skills": parsed["skills"],

            "education": parsed["education"],

            "projects": parsed["projects"],

            "certifications": parsed["certifications"]

        }

    }