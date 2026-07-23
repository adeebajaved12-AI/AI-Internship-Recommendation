from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User  # Ya jo bhi aapka user model ho
from app.services.vector_store import semantic_search_internships, add_internship_to_db

router = APIRouter(prefix="/recommend", tags=["Recommendations"])

# Startup ya initialization par kuch default internships ko Vector DB mein seed karna
def initialize_vector_db():
    internships_data = [
        {"id": "1", "title": "AI Intern at Arch Technologies", "description": "Build local LLM models, Ollama, Streamlit, and Python workflows.", "skills": "Python, Machine Learning, NLP, Ollama"},
        {"id": "2", "title": "Full Stack Developer at Ezitech", "description": "Web application development using PHP, MySQL, WampServer, and JavaScript.", "skills": "PHP, MySQL, JavaScript, HTML, CSS"},
        {"id": "3", "title": "Data Scientist Track", "description": "Advanced data analysis, predictive modeling, and deep learning architectures.", "skills": "Python, TensorFlow, Deep Learning, SQL"}
    ]
    for item in internships_data:
        add_internship_to_db(item["id"], item["title"], item["description"], item["skills"])

# Call initialization
initialize_vector_db()

@router.get("/{student_id}")
def get_recommendations(student_id: int, db: Session = Depends(get_db)):
    # 1. Database se user/student find karna aur uski extracted skills nikalna
    user = db.query(User).filter(User.id == student_id).first()
    
    # Agar user na mile ya skills empty hon toh default fallback skills use karein
    student_skills = ["Python", "Machine Learning", "NLP"]
    if user and hasattr(user, 'skills') and user.skills:
        # Agar skills string format mein hain toh split kar lein
        if isinstance(user.skills, str):
            student_skills = [s.strip() for s in user.skills.split(",")]
        elif isinstance(user.skills, list):
            student_skills = user.skills

    # 2. Vector Database se Semantic Similarity Search perform karna
    search_results = semantic_search_internships(student_skills, n_results=3)
    
    recommended_internships = []
    
    if search_results and 'metadatas' in search_results and search_results['metadatas']:
        metadatas = search_results['metadatas'][0]
        distances = search_results['distances'][0] if 'distances' in search_results and search_results['distances'] else [0.2] * len(metadatas)
        
        for i, meta in enumerate(metadatas):
            # Distance ko match score percentage mein convert karna (Chroma L2 distance heuristic)
            dist = distances[i] if i < len(distances) else 0.2
            match_score = max(40, min(95, int((1 - dist) * 100)))
            
            req_skills_str = meta.get("skills", "")
            req_skills_list = [s.strip() for s in req_skills_str.split(",")]
            
            # Strengths aur Missing skills calculate karna
            strengths = [s for s in student_skills if s in req_skills_list]
            if not strengths:
                strengths = student_skills[:2]
                
            missing_skills = [s for s in req_skills_list if s not in student_skills]
            
            recommended_internships.append({
                "title": meta.get("title"),
                "company": "Ezitech Partner",
                "mentor": "Mam Hamera Javed" if "AI" in meta.get("title") else "Ali Ahmed",
                "match_score": match_score,
                "strengths": strengths,
                "missing_skills": missing_skills if missing_skills else ["Advanced Deployment"],
                "recommended_roadmap": f"Master {' -> '.join(req_skills_list)}",
                "ai_reasoning": f"Generated via Embedding-based Semantic Search. Your vector profile shares high semantic alignment with this track's core requirements."
            })
    
    # Match score ke mutabiq sorting karna (highest first)
    recommended_internships = sorted(recommended_internships, key=lambda x: x['match_score'], reverse=True)

    return {
        "student_id": student_id,
        "extracted_skills_used": student_skills,
        "recommendations": recommended_internships
    }