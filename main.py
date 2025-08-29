from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

todo_list: List[TodoItem] = []

@app.post("/todos/", response_model=TodoItem)
def create_todo(item: TodoItem):
    if any(t.id == item.id for t in todo_list):
        raise HTTPException(status_code=400, detail="Task with this ID already exists.")
    todo_list.append(item)
    return item

@app.get("/todos/", response_model=List[TodoItem])
def get_all_todos():
    return todo_list

@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    for i, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[i] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Task not found")