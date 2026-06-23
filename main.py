from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.orm import Session

from database import Base, engine

from routers.users import router as user_router
import uvicorn

app = FastAPI()
app.include_router(user_router, prefix="/tasks", tags=["Tasks"])

# Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127,0.0.1", port=8000, reload=True)
