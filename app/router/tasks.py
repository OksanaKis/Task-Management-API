from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.router.deps_auth import get_current_user
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = Task(**payload.model_dump(), user_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=list[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.id.desc())
    )
    tasks = db.scalars(stmt).all()
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(task, k, v)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None