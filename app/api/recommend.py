from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.student import StudentProfile

from app.services.vector_store import (
    semantic_search_internships,
    semantic_search_mentor,
    calculate_match_score
)

router = APIRouter(
    prefix="/recommend",
    tags=["AI Recommendation Engine"]
)


# -------------------------------------------------------
# Learning Roadmap Generator
# -------------------------------------------------------

def generate_learning_roadmap(missing_skills):

    roadmap = []

    for i, skill in enumerate(missing_skills):

        roadmap.append(
            {
                "week": i + 1,
                "focus": skill,
                "goal": f"Learn {skill} fundamentals and build one mini project."
            }
        )

    return roadmap


# -------------------------------------------------------
# Recommendation API
# -------------------------------------------------------

@router.get("/{student_id}")

def recommend(student_id: int, db: Session = Depends(get_db)):

    student = db.query(StudentProfile).filter(
        StudentProfile.id == student_id
    ).first()

    if student is None:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    student_skills = student.skills.split(",")

    # ---------------------------------------------
    # Internship Search
    # ---------------------------------------------

    internship_results = semantic_search_internships(
        student_skills,
        n_results=3
    )

    # ---------------------------------------------
    # Mentor Search
    # ---------------------------------------------

    mentor_results = semantic_search_mentor(
        student_skills
    )

    recommendations = []

    if internship_results["metadatas"]:

        metas = internship_results["metadatas"][0]

        distances = internship_results["distances"][0]

        for i, meta in enumerate(metas):

            required_skills = [

                s.strip()

                for s in meta["skills"].split(",")

            ]

            strengths = []

            missing = []

            for skill in required_skills:

                if skill.lower() in [
                    x.strip().lower()
                    for x in student_skills
                ]:

                    strengths.append(skill)

                else:

                    missing.append(skill)

            score = calculate_match_score(
                distances[i]
            )

            confidence = round(
                (score / 100) * 0.95,
                2
            )

            roadmap = generate_learning_roadmap(
                missing
            )

            reasoning = f"""
Student profile has strong similarity with the required
technical stack.

Matched Skills:
{', '.join(strengths)}

Missing Skills:
{', '.join(missing)}

Embedding-based semantic similarity indicates that
this internship is highly relevant.
"""

            recommendations.append(

                {

                    "internship": meta["title"],

                    "company": meta["company"],

                    "mentor": meta["mentor"],

                    "required_skills": required_skills,

                    "strengths": strengths,

                    "missing_skills": missing,

                    "match_score": score,

                    "confidence_score": confidence,

                    "learning_roadmap": roadmap,

                    "reasoning": reasoning

                }

            )

    recommendations.sort(

        key=lambda x: x["match_score"],

        reverse=True

    )

    best_mentor = None

    if mentor_results["metadatas"]:

        best_mentor = mentor_results["metadatas"][0][0]["mentor"]

    return {

        "student": {

            "id": student.id,

            "name": student.name,

            "email": student.email,

            "skills": student.skills

        },

        "recommended_mentor": best_mentor,

        "recommendations": recommendations

    }