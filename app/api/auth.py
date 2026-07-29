from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str

# SIGNUP ENDPOINT
@router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user_data.email, hashed_password=user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id}

# LOGIN ENDPOINT 
@router.post("/login")
def login(user_credentials: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    if not user or user.hashed_password != user_credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    return {"message": "Login successful", "user_id": user.id}