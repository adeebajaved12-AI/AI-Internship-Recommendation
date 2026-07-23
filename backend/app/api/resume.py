import os
import re
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.student import StudentProfile
from app.services.parser import extract_text_from_pdf, extract_skills

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-resume")
async def upload_resume(
    student_id: int, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported.")
    
    # Save the uploaded file locally
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    # Extract text using PyMuPDF (fitz) from parser.py
    raw_text = extract_text_from_pdf(file_path)
    
    # Extract skills
    skills_list = extract_skills(raw_text)
    skills_str = ", ".join(skills_list) if skills_list else "python, machine learning"
    
    # Email extraction via regex fallback
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', raw_text)
    email = email_match.group(0) if email_match else "Not found"
    
    # Update or Create Student Profile in Database matching the expanded schema
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        student = StudentProfile(
            id=student_id, 
            name="Student", 
            email=email, 
            skills=skills_str,
            resume_path=file_path
        )
        db.add(student)
    else:
        student.skills = skills_str
        student.resume_path = file_path
        if email != "Not found":
            student.email = email
            
    db.commit()
    db.refresh(student)
    
    return {
        "message": "Resume uploaded and parsed successfully!",
        "filename": file.filename,
        "extracted_email": student.email,
        "extracted_skills": student.skills,
        "resume_path": student.resume_path,
        "status": "Success"
    }