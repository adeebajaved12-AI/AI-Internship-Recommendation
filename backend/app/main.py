from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database.connection import engine, Base
from app.models import user, student, internship
from app.api import auth, profile, recommend, resume 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup ke waqt tables create hon gi
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic agar koi ho

app = FastAPI(title="AI Internship Recommendation API", lifespan=lifespan)

# CORS Middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Internship Recommendation System!"}

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommendation"])
app.include_router(resume.router, prefix="/resume", tags=["Resume Parsing"])