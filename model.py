from sqlalchemy import Column, Integer, String, Text, String, DateTime, ForeignKey
from database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    status = Column(String)
    prioprity = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    create_at = Column(DateTime)
    update_at = Column(DateTime)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(50), unique=True)
    hashed_password = Column(String(50), unique=True)
    created_at = Column(DateTime)
