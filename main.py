import sqlite3
import os

def add_mentor(name, expertise, contact):
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mentors 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, expertise TEXT, contact TEXT)''')
    cursor.execute("INSERT INTO mentors (name, expertise, contact) VALUES (?, ?, ?)", (name, expertise, contact))
    conn.commit()
    conn.close()

def get_dynamic_mentors():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mentors 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, expertise TEXT, contact TEXT)''')
    cursor.execute("SELECT name, expertise, contact FROM mentors")
    mentors = cursor.fetchall()
    conn.close()
    return mentors

def validate_github_profile_and_repo(url):
    if "github.com" in url:
        return {"valid": True, "type": "Repository/Profile", "language": "Python / AI / Web", "name": url.split("/")[-1]}
    return {"valid": False, "error": "Invalid GitHub URL format."}

def get_recommendations_based_on_profile(skills_text):
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    
    # Purani table ko drop kar ke fresh table create karein taake schema conflict khatam ho jaye
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