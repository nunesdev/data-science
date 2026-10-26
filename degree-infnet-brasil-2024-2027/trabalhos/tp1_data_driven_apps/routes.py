from datetime import date
from typing import Optional

from fastapi import APIRouter, HTTPException

from models import BirthdayRequest, UserCreate, UserResponse

router = APIRouter()

_users: dict[str, UserResponse] = {
    "bruno": UserResponse(username="bruno", message="Welcome, bruno!"),
    "bob": UserResponse(username="bob", message="Welcome, bob!"),
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


def _birthday_in_year(year: int, birthday: date) -> date:
    try:
        return date(year, birthday.month, birthday.day)
    except ValueError:
        return date(year, 2, 28)


def _days_until_next_birthday(birthday: date, today: Optional[date] = None) -> int:
    today = today or date.today()
    next_birthday = _birthday_in_year(today.year, birthday)
    if next_birthday < today:
        next_birthday = _birthday_in_year(today.year + 1, birthday)
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
    return UserResponse(
        username=user.username,
        message=f"Welcome, {user.username}!",
    )


@router.post("/create-user", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate) -> UserResponse:
    key = payload.username.lower()
    if key in _users:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    user = UserResponse(
        username=payload.username,
        message=f"Welcome, {payload.username}!",
    )
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
def birthday_countdown(payload: BirthdayRequest) -> dict[str, str]:
    days = _days_until_next_birthday(payload.birthday)
    return {
        "message": (
            f"Olá, {payload.name}! Faltam {days} dias para o seu próximo aniversário."
        ),
    }
