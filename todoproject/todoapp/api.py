from ninja import Router, Schema, Query
from typing import List
from datetime import date
from .models import Todo
from django.shortcuts import get_object_or_404

api = Router()

# ✅ Schema definitions
class TodoSchema(Schema):
    id: int
    title: str
    description: str
    status: str
    due_date: date
    created_at: date


class TodoCreateSchema(Schema):
    title: str
    description: str
    status: str
    due_date: date


# ✅ List all todos with filtering and search
@api.get("/todos", response=List[TodoSchema])
def list_todos(
    request,
    status: str = Query(None),
    due_date: date = Query(None),
    search: str = Query(None),
):
    todos = Todo.objects.all()

    if status:
        todos = todos.filter(status=status)

    if due_date:
        todos = todos.filter(due_date=due_date)

    if search:
        todos = todos.filter(title__icontains=search) | todos.filter(description__icontains=search)

    return list(todos)


# ✅ Get one todo
@api.get("/todos/{todo_id}", response=TodoSchema)
def get_todo(request, todo_id: int):
    return get_object_or_404(Todo, id=todo_id)


# ✅ Create a new todo
@api.post("/todos", response=TodoSchema)
def create_todo(request, data: TodoCreateSchema):
    todo = Todo.objects.create(**data.dict())
    return todo


# ✅ Update a todo
@api.put("/todos/{todo_id}", response=TodoSchema)
def update_todo(request, todo_id: int, data: TodoCreateSchema):
    todo = get_object_or_404(Todo, id=todo_id)
    for attr, value in data.dict().items():
        setattr(todo, attr, value)
    todo.save()
    return todo


# ✅ Delete a todo
@api.delete("/todos/{todo_id}")
def delete_todo(request, todo_id: int):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return {"success": True}


# ✅ Get overdue todos
@api.get("/todos/overdue", response=List[TodoSchema])
def overdue_todos(request):
    today = date.today()
    return list(Todo.objects.filter(status="pending", due_date__lt=today))
