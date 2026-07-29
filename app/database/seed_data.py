from app.database.connection import SessionLocal
from app.models.internship import Internship

db = SessionLocal()

# Kuch sample internships
jobs = [
    Internship(title="AI Researcher", company="Neural AI", required_skills="Python, PyTorch, Deep Learning"),
    Internship(title="Python Intern", company="Tech Solutions", required_skills="Python, SQL, FastAPI")
]

db.add_all(jobs)
db.commit()
db.close()
print("Data successfully added to database!")