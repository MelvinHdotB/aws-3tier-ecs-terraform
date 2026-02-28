from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str

tasks: List[Task] = []
next_id = 1

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = Task(id=next_id, title=task.title)
    next_id += 1
    tasks.append(new_task)
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t.id == task_id:
            tasks.pop(i)
            return {"deleted": True, "task_id": task_id}
    raise HTTPException(status_code=404, detail="Task not found")