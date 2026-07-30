import sqlite3

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


def get_all_internships():
  conn = sqlite3.connect("internships.db")
  cursor = conn.cursor()
  cursor.execute(
      "SELECT title, domain, description, skills FROM internships"
  )
  rows = cursor.fetchall()
  conn.close()
  return rows


def recommend_internships(user_skills):
  # Recommendation logic based on matching skills
  internships = get_all_internships()
  recommendations = []
  user_skill_set = set([s.strip().lower() for s in user_skills.split(",")])

  for title, domain, description, skills in internships:
    job_skills = set([s.strip().lower() for s in skills.split(",")])
    # Match criteria
    intersection = user_skill_set.intersection(job_skills)
    if intersection:
      recommendations.append({
          "title": title,
          "domain": domain,
          "description": description,
          "skills": skills,
          "match_score": len(intersection),
      })

  # Fallback if no direct match
  if not recommendations and internships:
    for title, domain, description, skills in internships:
      recommendations.append({
          "title": title,
          "domain": domain,
          "description": description,
          "skills": skills,
          "match_score": 0,
      })

  return sorted(recommendations, key=lambda x: x["match_score"], reverse=True)