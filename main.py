from fastapi import FastAPI, Depends, HTTPException
from routers.auth import router as auth_router
from sqlalchemy.orm import Session
import model, schema
from database import Base, engine
from utils import hash_password
from routers.users import router as user_router
from routers.tasks import router as task_router
import uvicorn

app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["Users"])

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
#Base.metadata.create_all(bind=engine)
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
