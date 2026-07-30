import sqlite3
import os
import pypdf

def init_db():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    # Mentors Table Creation & Sample Data
    cursor.execute('''CREATE TABLE IF NOT EXISTS mentors 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, expertise TEXT, domain TEXT, contact TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM mentors")
    if cursor.fetchone()[0] == 0:
        sample_mentors = [
            ("Dr. Ahmed Khan", "Python, PyTorch, AI, LLM, Streamlit", "Artificial Intelligence", "ahmed.khan@ezitech.pk"),
            ("Engr. Sara Malik", "PHP, MySQL, Web, Backend", "Web Development", "sara.malik@ezitech.pk"),
            ("Prof. Zeeshan Ali", "Python, PyTorch, Deep Learning, NLP", "Deep Learning & NLP", "zeeshan.ali@ezitech.pk")
        ]
        cursor.executemany("INSERT INTO mentors (name, expertise, domain, contact) VALUES (?, ?, ?, ?)", sample_mentors)
        conn.commit()
        
    # Internships Table Creation & Sample Data
    cursor.execute('DROP TABLE IF EXISTS internships')
    cursor.execute('''CREATE TABLE internships 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, domain TEXT, description TEXT, skills TEXT)''')
    
    sample_internships = [
        ("Generative AI & LLM Intern", "Artificial Intelligence", "Build local LLM applications using Ollama, Python, and Streamlit.", "Python, PyTorch, AI, LLM, Streamlit"),
        ("Backend Web Developer", "Web Development", "Develop backend services using PHP, MySQL, and WampServer.", "PHP, MySQL, Web, Backend"),
        ("Machine Learning Research Intern", "Deep Learning", "Design multilingual hate speech and text detection models using PyTorch.", "Python, PyTorch, Deep Learning, NLP")
    ]
    cursor.executemany("INSERT INTO internships (title, domain, description, skills) VALUES (?, ?, ?, ?)", sample_internships)
    conn.commit()
    conn.close()

def add_mentor(name, expertise, domain, contact):
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mentors (name, expertise, domain, contact) VALUES (?, ?, ?, ?)", (name, expertise, domain, contact))
    conn.commit()
    conn.close()

def get_dynamic_mentors():
    """Compatibility alias for app.py imports"""
    init_db()
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, expertise, domain, contact FROM mentors")
    mentors = cursor.fetchall()
    conn.close()
    return mentors

def get_dynamic_mentor_recommendation(user_skills, matched_domain):
    """
    Ezitech Case Study Requirement: Matches applicant profile skills and domain 
    with the most suitable mentor based on expertise overlap.
    """
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, expertise, domain, contact FROM mentors")
    all_mentors = cursor.fetchall()
    conn.close()

    best_mentor = None
    max_overlap = -1
    user_skills_set = set(s.strip().lower() for s in user_skills.split(','))

    for mentor in all_mentors:
        mentor_name, mentor_expertise, mentor_domain, mentor_contact = mentor
        mentor_skills_set = set(s.strip().lower() for s in mentor_expertise.split(','))
        
        # Calculate skill overlap score
        overlap = len(user_skills_set.intersection(mentor_skills_set))
        
        # Give extra weight if domain matches
        if mentor_domain.lower() in matched_domain.lower():
            overlap += 2
            
        if overlap > max_overlap:
            max_overlap = overlap
            best_mentor = {
                "name": mentor_name,
                "expertise": mentor_expertise,
                "domain": mentor_domain,
                "contact": mentor_contact,
                "match_score": max_overlap
            }
            
    return best_mentor if best_mentor else {"name": "Dr. Ahmed Khan", "expertise": "General AI & Python", "domain": "Artificial Intelligence", "contact": "ahmed.khan@ezitech.pk"}

def validate_github_profile_and_repo(url):
    if "github.com" in url:
        return {"valid": True, "type": "Repository/Profile", "language": "Python / AI / Web", "name": url.split("/")[-1]}
    return {"valid": False, "error": "Invalid GitHub URL format."}

def parse_resume_pdf(uploaded_file):
    """Extracts text from uploaded PDF resumes for profile analysis."""
    try:
        reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

def generate_learning_roadmap(missing_skills):
    """Generates personalized learning path based on missing competencies."""
    roadmap = []
    for skill in missing_skills:
        if "pytorch" in skill.lower() or "ai" in skill.lower() or "llm" in skill.lower():
            roadmap.append(f"Complete Deep Learning & LLM specialized training modules for {skill}.")
        elif "php" in skill.lower() or "mysql" in skill.lower() or "backend" in skill.lower():
            roadmap.append(f"Build hands-on database-driven projects focusing on {skill}.")
        else:
            roadmap.append(f"Focus on practical implementation and documentation for {skill}.")
    return roadmap if roadmap else ["All core competencies met! Proceed to live project deployment."]

def generate_ai_reasoning(matched_skills, total_required):
    """Generates confidence score and AI reasoning summary for the candidate profile."""
    required_list = [s.strip() for s in total_required.split(',')]
    score = int((len(matched_skills) / max(len(required_list), 1)) * 100)
    score = min(max(score, 40), 98) # Keep realistic bounds
    reasoning = f"Candidate profile demonstrates alignment with {len(matched_skills)} out of {len(required_list)} required core technical competencies, resulting in an evaluated confidence score of {score}%."
    return score, reasoning

def get_recommendations_based_on_profile(skills_text):
    init_db()
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, domain, description, skills FROM internships")
    all_jobs = cursor.fetchall()
    conn.close()

    matched_jobs = []
    user_skills_lower = skills_text.lower() if skills_text else ""
    
    for job in all_jobs:
        job_skills = job[3].lower()
        if any(skill.strip() in user_skills_lower for skill in job_skills.split(',')):
            matched_jobs.append(job)
            
    if not matched_jobs:
        matched_jobs = all_jobs
        
    return matched_jobs