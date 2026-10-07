from fastapi import APIRouter
from model import TodoItem

todo_router = APIRouter()

@todo_router.get("/")
async def welcome():
  return {'message':'hello!'}

@todo_router.get("/status")
async def status():
  return {'message': 'status ok'}


todo_list = ["acabate","çamã"]

@todo_router.post("/todo")
async def add(item: str):
  todo_list.append(item)
  return {'message': f"item '{item} foi adicionad"}

@todo_router.get("/todo")
async def retrieve():
  return {'data': todo_list}

todo_dic = {0:'Banana',1:'Melao'}


@todo_router.post("/todo_pydantic")
async def add_pydantic(todo_item: TodoItem):
  todo_dic[todo_item.id] = todo_item.item
  return {'message': f"O item '{todo_item.item} foi adicionad"}

@todo_router.get("/todo_pydantic")
async def retrieve_pydantic():
  return {'data': todo_dic}
