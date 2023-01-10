import base64
import json
from typing import Dict, Optional, List

from todo_api.database import USER_TABLE, TODO_TABLE
from fastapi import HTTPException
from starlette.requests import Request
from tinydb import Query, where
from todo_api.views.models import User, ReturnTodo


def extract_username(request: Request) -> str:
    user = decode_user_dict(request)
    return user["username"]


def decode_user_dict(request: Request) -> Dict[str, str]:
    header = request.headers.get("Authorization")
    decoded_header = base64.decodebytes(bytes(header, encoding="UTF_8"))
    return json.loads(decoded_header)


def generate_token(username: str, password: str) -> str:
    return User.generate_token(username, password)


def get_user_from_request(request: Request) -> Optional[User]:
    username = extract_username(request)
    return get_user_from_db(username)


def get_user_from_db(username: str) -> Optional[User]:
    user_query = Query()
    db_user = USER_TABLE.search(user_query.username == username)

    if not db_user:
        return None

    db_user = db_user[0]

    return User(username=username, token=db_user["token"], id=db_user.doc_id)


def crate_user(username: str, password: str) -> User:
    token = generate_token(username, password)
    USER_TABLE.insert({"username": username, "token": token})
    return get_user_from_db(username)


def retrieve_todo(todo_id: int, request: Request) -> ReturnTodo:
    user = get_user_from_request(request)
    todo_db = TODO_TABLE.get(doc_id=todo_id)

    if not todo_db:
        raise HTTPException(404, "Item not found")

    if todo_db["user_id"] != user.id:
        raise HTTPException(403, "You don't have access to this item")

    return ReturnTodo(**todo_db, id=todo_db.doc_id)


def get_todos_from_db(request: Request) -> List[ReturnTodo]:
    user = get_user_from_request(request)
    todo_items = TODO_TABLE.search(where("user_id") == user.id)
    return [ReturnTodo(**todo, id=todo.doc_id) for todo in todo_items]
