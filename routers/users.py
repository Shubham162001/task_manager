from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import model, schema
from utils import hash_password
from auth_token import get_current_user

router = APIRouter()

router.get("/users")


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(model.User).all()
    return users


@router.post("/register", response_model=schema.UserResponse)
def register_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(model.User).filter(model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(
        f"Registering user: {user.username}, Email: {user.email} and password: {user.password}"
    )
    hashed_password = hash_password(user.password)

    new_user = model.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user
