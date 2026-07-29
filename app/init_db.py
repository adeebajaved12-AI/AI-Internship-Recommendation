from app.database import engine, Base
from app.models.student import Student
from app.models.user import User

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()