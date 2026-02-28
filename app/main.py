from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import TaskModel

app = FastAPI()

Base.metadata.create_all(bind=engine)


class TaskCreate(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True  # pydantic v2


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/tasks", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(title=task.title)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"deleted": True, "task_id": task_id}
