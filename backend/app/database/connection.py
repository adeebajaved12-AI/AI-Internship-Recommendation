# File: backend/database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# @ symbol ko %40 se replace kar diya gaya hai taake URL correctly parse ho
DATABASE_URL = "postgresql://postgres:kashmir%40786@127.0.0.1:5432/ezitech_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()