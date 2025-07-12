from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

app = FastAPI(
    title = "Task Manager API",
    description = "A Task Manager API is a backend service that lets users create, read, update, and delete tasks (CRUD operations) programmatically through HTTP requests (like POST, GET, PUT, DELETE)."
)

task_id = 1#creating a variable named task_id to uniquely identify the tasks.
Tasks = {}#temporarily declaring a tasks list to add all the tasks here. Will shortly replace it with an actual database.


#Defining a pydantic model here. Pydantic models says "when someone sends me tasks, it should have a id, title, description, status, due date, created_at, updated_at. Otherwise it rejects it automatically."
#defining a post method for creating tasks.

class taskmodel(BaseModel):
    id : str = Field(..., example = "1")
    title : str = Field(..., example = "My first note")
    description : Optional[str] = Field(None, example = "This is my first note")
    status : str = Field(..., example = "ongoing")
    due_date : datetime = Field(..., example = "2025-04-02T15:00:00")
    created_at : Optional[date] = Field(None, example = "2025-04-01")
    updated_at : datetime = Field(None, example = "2025-04-03T12:00:00")

#adding tasks
@app.post("/tasks/")
def create_task(task: taskmodel):
    global task_id
    Tasks[task_id] = task
    task_id += 1
    return{"id": task_id-1, **task.dict()}

#viewing tasks by id
@app.get("/tasks/{task_id}")
def view_task_byid(task_id:int):
    if task_id in Tasks:
        task = Tasks[task_id]
        return{"id": task_id, **task.dict()}
    else:
        raise HTTPException(status_code = 404, detail = "Task not found.")

#viewing tasks
@app.get("/tasks/")
def view_task():
    all_tasks = []
    for task_id, task in Tasks.items():
        task_data = {"id": task_id, **task.dict()}
        all_tasks.append(task_data)
    return all_tasks

#editing tasks from id 
@app.put("/tasks/{task_id}")
def edit_task(task_id: int, task: taskmodel):
    if task_id not in Tasks:
        raise HTTPException(status_code = 404, details = "Task not found.")
    else:
        Tasks[task_id] = task
        return{"id": task_id, **task.dict()}

#deleting tasks from id
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    if task_id in Tasks:
        del[task_id]
        return{"message": "Task deleted successfully."}
    else:
        raise HTTPException(status_code = 404, detail = "Task not found.")
    