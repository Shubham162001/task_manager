from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

router.get("/users")


def get_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users
