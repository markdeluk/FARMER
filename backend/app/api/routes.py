from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services import user_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
def read_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = user_service.create_user(db, name, email)
    return user
