 
from fastapi import APIRouter, HTTPException, status
from api.models.todo import Todo
from api.schemas.todo import PostTodo, GetTodo, PutTodo

todo_router =  APIRouter(prefix="/api", tags=["Todo"])

@todo_router.get("/")
async def get_todos():
    
    # Fetch the data
    data = await Todo.all()

# Manually convert each result into Pydantic models
    todos  =   [GetTodo.from_orm(todo) for todo in data]
    return todos

    
   

@todo_router.post("/")
async def create_todo(body: PostTodo):
    row = await Todo.create(**body.dict(exclude_unset=True))
    return await GetTodo.from_tortoise_orm(row)

@todo_router.put("/{key}")
async def update_todo(key: int, body: PutTodo):
    # Convert body to a dictionary excluding unset values
    data = body.dict(exclude_unset=True)
    
    # Check if the todo with the given key exists
    exists = await Todo.filter(id=key).exists()

    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    
    # Update the todo item
    await Todo.filter(id=key).update(**data)
    
    # Retrieve the updated Todo object 
    updated_todo = await Todo.get(id=key)
    
    # Manually convert the updated Todo model instance to a Pydantic model
    return GetTodo.from_orm(updated_todo)



@todo_router.delete("/{key}")
async def delete_todo(key: int):
    exists = await Todo.filter(id=key).exists()

    if not exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    await Todo.filter(id=key).delete()
    return {"message": "Todo deleted successfully"}

 