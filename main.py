import sqlite3
import os

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