from fastapi import FastAPI
from todo import todo_router

app = FastAPI()
app.include_router(todo_router)

@app.get("/")
async def welcome():
  return {'message':'hello!'}

@app.get("/status")
async def status():
  return {'message': 'status ok'}

