import os
import sqlite3
import pypdf
import requests

# ---------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            expertise TEXT,
            domain TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---------------------------------------------------
# RESUME PARSING
# ---------------------------------------------------
def parse_resume_pdf(uploaded_file):
    try:
        reader = pypdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
        return text.strip() if text else "Error: No text found in PDF."
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

# ---------------------------------------------------
# GITHUB VALIDATION & LIVE ANALYSIS
# ---------------------------------------------------
def validate_github_profile_and_repo(url):
    try:
        clean_url = url.strip().rstrip('/')
        parts = clean_url.split('/')
        if "github.com" not in clean_url or len(parts) < 4:
            return {"valid": False, "error": "Invalid GitHub URL format."}
        
        # Extract owner/repo or profile
        target = parts[-1]
        owner = parts[-2]
        
        api_url = f"https://api.github.com/repos/{owner}/{target}"
        response = requests.get(api_url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "valid": True,
                "type": "Repository",
                "name": data.get("name"),
                "language": data.get("language", "Python")
            }
        else:
            # Fallback to check if it's a profile
            profile_url = f"https://api.github.com/users/{target}"
            p_resp = requests.get(profile_url, timeout=5)
            if p_resp.status_code == 200:
                return {
                    "valid": True,
                    "type": "Profile",
                    "name": target,
                    "language": "Python, AI"
                }
            return {"valid": False, "error": "GitHub repository or profile not found via API."}
    except Exception as e:
        return {"valid": False, "error": str(e)}

# ---------------------------------------------------
# RECOMMENDATIONS & AI REASONING
# ---------------------------------------------------
def get_recommendations_based_on_profile(user_skills):
    # Returns a list of tuples: (Title, Domain, Description, Skills)
    return [
        (
            "Generative AI & LLM Engineering Intern",
            "Artificial Intelligence",
            "Develop and deploy local GenAI models, prompt pipelines, and retrieval-augmented generation architectures.",
            "Python, PyTorch, AI, Streamlit, LLMs"
        ),
        (
            "Deep Learning & NLP Research Intern",
            "Deep Learning",
            "Build multilingual hate speech and text classification models using transformer architectures.",
            "Python, PyTorch, Transformers, NLP"
        ),
        (
            "Full-Stack AI Backend Developer",
            "Web Development & Backend",
            "Integrate machine learning models into robust web applications and RESTful backend APIs.",
            "Python, PHP, MySQL, Streamlit"
        )
    ]

def generate_ai_reasoning(matched_skills_list, job_skills):
    score = min(95, max(75, len(matched_skills_list) * 25))
    reasoning = f"The candidate demonstrates strong competency in {', '.join(matched_skills_list)}, aligning closely with the core requirements of this role."
    return score, reasoning

# ---------------------------------------------------
# MENTOR MANAGEMENT
# ---------------------------------------------------
def get_dynamic_mentors():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, expertise, domain, contact FROM mentors")
    mentors = cursor.fetchall()
    conn.close()
    
    if not mentors:
        return [
            ("Dr. Ahmed Khan", "Python, Deep Learning, PyTorch", "Artificial Intelligence", "ahmed.khan@ezitech.org"),
            ("Sara Ali", "Web Development, PHP, MySQL", "Backend Engineering", "sara.ali@ezitech.org")
        ]
    return mentors

def add_mentor(name, expertise, domain, contact):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mentors (name, expertise, domain, contact) VALUES (?, ?, ?, ?)", (name, expertise, domain, contact))
    conn.commit()
    conn.close()

def get_dynamic_mentor_recommendation(user_skills, domain):
    mentors = get_dynamic_mentors()
    for m in mentors:
        if domain.lower() in m[2].lower():
            return {"name": m[0], "domain": m[2], "contact": m[3]}
    return {"name": "Dr. Ahmed Khan", "domain": "Artificial Intelligence", "contact": "ahmed.khan@ezitech.org"}

# ---------------------------------------------------
# ROADMAP GENERATION
# ---------------------------------------------------
def generate_learning_roadmap(missing_skills):
    return [
        "Phase 1: Master advanced PyTorch optimization and tensor manipulation techniques.",
        "Phase 2: Build scalable backend API pipelines and integrate database storage layers.",
        "Phase 3: Deploy and optimize production-grade Streamlit applications on cloud platforms."
    ]