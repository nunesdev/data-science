from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException

from models import BirthdayRequest, UserCreate, UserResponse

router = APIRouter()

_users: dict[str, UserResponse] = {
    "bruno": UserResponse(username="bruno", age=37),
    "bob": UserResponse(username="bob", age=34),
}

_items: dict[int, dict] = {
    1: {"item_id": 1, "name": "Notebook"},
    2: {"item_id": 2, "name": "Mouse"},
}


class InvalidItemIdError(Exception):
    def __init__(self, item_id: int) -> None:
        self.item_id = item_id
        super().__init__(f"Item id {item_id} é inválido")


def _validate_item_id(item_id: int) -> None:
    if item_id < 1:
        raise InvalidItemIdError(item_id)


def _days_until_next_birthday(birth_date: date, today: Optional[date] = None) -> int:
    today = today or date.today()
    next_birthday = date(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, birth_date.month, birth_date.day)
    return (next_birthday - today).days


@router.get("/")
def read_root() -> str:
    return "Hello, FastAPI!"


@router.get("/status")
def read_status() -> dict[str, str]:
    return {"status": "ok", "message": "Servidor em funcionamento"}


@router.get("/user/{username}", response_model=UserResponse)
def get_user(username: str) -> UserResponse:
    user = _users.get(username.lower())
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.post("/create-user", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate) -> UserResponse:
    key = payload.username.lower()
    if key in _users:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user = UserResponse(username=payload.username, age=payload.age)
    _users[key] = user
    return user


@router.get("/item/{item_id}")
def get_item(item_id: int) -> dict:
    _validate_item_id(item_id)
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    return item


@router.delete("/item/{item_id}")
def delete_item(item_id: int) -> dict[str, str]:
    _validate_item_id(item_id)
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    del _items[item_id]
    return {"message": f"Item {item_id} removido com sucesso"}


@router.post("/birthday")
def birthday_countdown(payload: BirthdayRequest) -> dict:
    days = _days_until_next_birthday(payload.birth_date)
    return {
        "name": payload.name,
        "days_until_next_birthday": days,
    }
