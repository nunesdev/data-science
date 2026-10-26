from datetime import date

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    username: str
    age: int


class UserCreate(BaseModel):
    username: str
    age: int = Field(gt=0, description="Idade deve ser um número inteiro positivo")


class BirthdayRequest(BaseModel):
    name: str
    birth_date: date
