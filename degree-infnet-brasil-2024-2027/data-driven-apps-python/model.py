from pydantic import BaseModel



class TodoItem(BaseModel):
  id: int
  item: str