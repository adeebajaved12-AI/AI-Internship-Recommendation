import sqlite3
import os
import requests
import pypdf
from sentence_transformers import SentenceTransformer, util

# Load lightweight embedding model for real-time semantic matching
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def init_db():
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mentors 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, expertise TEXT, domain TEXT, contact TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS internships 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, domain TEXT, description TEXT, skills TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS feedback_logs 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, student_name TEXT, track_title TEXT, rating TEXT, comments TEXT)''')
    
    cursor.execute("SELECT COUNT(*) FROM internships")
    if cursor.fetchone()[0] == 0:
        sample_internships = [
            ("Generative AI & LLM Intern", "Artificial Intelligence", "Build local LLM applications using Ollama, Python, and Streamlit.", "Python, PyTorch, AI, LLM, Streamlit"),
            ("Backend Web Developer", "Web Development", "Develop backend services using PHP, MySQL, and WampServer.", "PHP, MySQL, Web, Backend"),
            ("Machine Learning Research Intern", "Deep Learning", "Design multilingual hate speech and text detection models using PyTorch.", "Python, PyTorch, Deep Learning, NLP")
        ]
        cursor.executemany("INSERT INTO internships (title, domain, description, skills) VALUES (?, ?, ?, ?)", sample_internships)
        conn.commit()
    conn.close()

def analyze_github_repo_live(repo_url):
    """Fetches real-time repository metadata and language statistics via GitHub REST API"""
    try:
        if "github.com" not in repo_url:
            return {"valid": False, "error": "Invalid GitHub URL format."}
        
        parts = repo_url.rstrip("/").split("/")
        if len(parts) < 2:
            return {"valid": False, "error": "Malformed GitHub URL."}
        
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        headers = {}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
            
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            lang_response = requests.get(data.get("languages_url"), headers=headers, timeout=10)
            languages = list(lang_response.json().keys()) if lang_response.status_code == 200 else []
            
            return {
                "valid": True,
                "name": data.get("name"),
                "description": data.get("description", ""),
                "stars": data.get("stargazers_count", 0),
                "languages": languages,
                "topics": data.get("topics", [])
            }
        else:
            return {"valid": False, "error": f"API Error: Status {response.status_code}"}
    except Exception as e:
        return {"valid": False, "error": str(e)}

def parse_resume_pdf(uploaded_file):
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

def get_realtime_recommendations(skills_text):
    """Semantic vector similarity matching using SentenceTransformers on live extracted skills"""
    init_db()
    conn = sqlite3.connect('internships.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, domain, description, skills FROM internships")
    all_jobs = cursor.fetchall()
    conn.close()

    if not skills_text.strip():
        return all_jobs

    user_embedding = embedder.encode(skills_text, convert_to_tensor=True)
    scored_jobs = []

    for job in all_jobs:
        job_skills_text = job[3]
        job_embedding = embedder.encode(job_skills_text, convert_to_tensor=True)
        similarity = util.cos_sim(user_embedding, job_embedding).item()
        scored_jobs.append((similarity, job))

    scored_jobs.sort(key=lambda x: x[0], reverse=True)
    return [job for score, job in scored_jobs]
import sqlite3


def init_db():
  conn = sqlite3.connect("internships.db")
  cursor = conn.cursor()

  # Create the table if it doesn't already exist
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            domain TEXT,
            description TEXT,
            skills TEXT
        )
    """)

  # Check if table is empty before inserting sample data to prevent duplicates
  cursor.execute("SELECT COUNT(*) FROM internships")
  count = cursor.fetchone()[0]

  if count == 0:
    cursor.executemany(
        """
            INSERT INTO internships (title, domain, description, skills) 
            VALUES (?, ?, ?, ?)
        """,
        sample_internships,
    )

  conn.commit()
  conn.close()