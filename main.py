import sqlite3
import requests
from pypdf import PdfReader

# Sample dataset for database initialization
sample_internships = [
    (
        "AI Research Intern",
        "Artificial Intelligence",
        "Work on fine-tuning LLMs and developing machine learning models.",
        "Python, PyTorch, LLMs",
    ),
    (
        "Generative AI Engineer",
        "Generative AI",
        "Build custom RAG pipelines and local AI applications using Ollama.",
        "Python, Streamlit, LangChain",
    ),
    (
        "Machine Learning Intern",
        "Machine Learning",
        "Develop predictive models and data analysis pipelines.",
        "Python, Scikit-Learn, Pandas",
    ),
]


def init_db():
  conn = sqlite3.connect("internships.db")
  cursor = conn.cursor()

  cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            domain TEXT,
            description TEXT,
            skills TEXT
        )
    """)

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


def parse_resume_pdf(uploaded_file):
  try:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
      text += page.extract_text() or ""
    return text
  except Exception as e:
    return f"Error parsing PDF: {str(e)}"


def analyze_github_repo_live(repo_identifier):
  try:
    cleaned_path = (
        repo_identifier.replace("https://github.com/", "").strip("/").split("/")
    )
    if len(cleaned_path) >= 2:
      owner, repo = cleaned_path[0], cleaned_path[1]
      api_url = f"https://api.github.com/repos/{owner}/{repo}"
      response = requests.get(api_url, timeout=10)
      if response.status_code == 200:
        data = response.json()
        return {
            "repo_name": data.get("name"),
            "description": data.get("description"),
            "language": data.get("language"),
            "stars": data.get("stargazers_count"),
            "status": "Success",
        }
    return {
        "status": "Error",
        "message": "Invalid repository format or not found.",
    }
  except Exception as e:
    return {"status": "Error", "message": str(e)}


def get_realtime_recommendations(user_skills):
  conn = sqlite3.connect("internships.db")
  cursor = conn.cursor()
  cursor.execute("SELECT title, domain, description, skills FROM internships")
  rows = cursor.fetchall()
  conn.close()

  recommendations = []
  user_skill_set = set([s.strip().lower() for s in user_skills.split(",")])

  for title, domain, description, skills in rows:
    job_skills = set([s.strip().lower() for s in skills.split(",")])
    intersection = user_skill_set.intersection(job_skills)
    recommendations.append({
        "title": title,
        "domain": domain,
        "description": description,
        "skills": skills,
        "match_score": len(intersection),
    })

  if not recommendations and rows:
    for title, domain, description, skills in rows:
      recommendations.append({
          "title": title,
          "domain": domain,
          "description": description,
          "skills": skills,
          "match_score": 0,
      })

  return sorted(recommendations, key=lambda x: x["match_score"], reverse=True)