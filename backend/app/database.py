import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base, engine
from app.models.student import StudentProfile
from app.models.user import User
from app.models.internship import Internship

def init_db():
    print("Creating SQLAlchemy tables...")
    # SQLAlchemy ke zariye saari models ki tables fresh banayein gi (with all columns like email)
    Base.metadata.create_all(bind=engine)
    print("SQLAlchemy tables created successfully!")
    
    # Raw sqlite3 connection se sample internships insert kar dein (agar zaroori hon)
    conn = sqlite3.connect("internships.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            required_skills TEXT
        )
    """)
    
    sample_jobs = [
        ("AI Intern", "Arch Technologies", "python, machine learning, nlp"),
        ("Python Developer", "Ezitech", "python, sql, flask"),
        ("Data Analyst Intern", "Tech Solutions", "python, sql, machine learning")
    ]
    
    for job in sample_jobs:
        cursor.execute("""
            INSERT INTO internships_raw (title, company, required_skills)
            SELECT ?, ?, ? 
            WHERE NOT EXISTS (SELECT 1 FROM internships_raw WHERE title = ?)
        """, (job[0], job[1], job[2], job[0]))
        
    conn.commit()
    conn.close()
    print("Sample internships initialized!")

if __name__ == "__main__":
    init_db()