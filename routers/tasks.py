from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import model
import schema
from database import get_db
from datetime import datetime
from auth_token import get_current_user

router = APIRouter()


@router.post("/", response_model=schema.TaskResponse)
def create_task(
    task: schema.TaskCreate,
    db: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user),
):
    print("Current User", current_user.hashed_password)
    new_task = model.Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        user_id=current_user.id,
        create_at=datetime.utcnow(),
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/", response_model=list[schema.TaskResponse])
def get_tasks(
    status: str = None,
    priority: str = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(model.Task.user_id == current_user.id)

    if status:
        query.filter(model.Task.status == status)

    if property:
        query.filter(model.Task.priority == priority)

    tasks = query.offset(skip).limit(limit).all()

    return tasks


@router.get("/{task_id}", response_model=schema.TaskResponse)
def get_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    task = db.query(model.Task).filter(model.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail=" Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access Denied")
    return task


@router.put("/{task_id}", response_model=schema.TaskResponse)
def update_task(
    task_id: int,
    task_data: schema.TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    task = db.query(model.Task).filter(model.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.Status is not None:
        task.status = task_data.Status

    if task_data.priority is not None:
        task.priority = task_data.priority

        db.commit()
        db.refresh(task)

        return task


@router.delete("/{task_id}")
def delete_task(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    task = db.query(model.Task).filter(model.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}
