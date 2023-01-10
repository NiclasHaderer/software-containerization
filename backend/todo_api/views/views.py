import time
from typing import List

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from todo_api.database import TODO_TABLE
from todo_api.views.helpers import extract_username, get_user_from_db, crate_user, get_user_from_request, \
    retrieve_todo, get_todos_from_db
from todo_api.views.models import Login, User, PartialTodo, ReturnTodo, PostTodo, ToDo, OrderBy

router = APIRouter()


@router.post("/login", response_model=User)
async def login(login_form: Login):
    user = get_user_from_db(login_form.username)

    if not user:
        raise HTTPException(400, "User does not exist")

    if not user.password_valid(login_form.password):
        raise HTTPException(400, "Password wrong")

    return user


@router.post("/create-account", response_model=None)
async def login(login_form: Login):
    user = get_user_from_db(login_form.username)

    if user:
        raise HTTPException(400, "User already exists")

    crate_user(login_form.username, login_form.password)


@router.get("/account", response_model=User)
async def login(request: Request) -> User:
    username = extract_username(request)

    return get_user_from_db(username)


@router.get("/todo/{todo_id}", response_model=ReturnTodo)
async def get_todo(todo_id: int, request: Request) -> ReturnTodo:
    todo_db = TODO_TABLE.get(todo_id)
    user = get_user_from_request(request)

    if not todo_db:
        raise HTTPException(404, "Item not found")

    todo = ReturnTodo(**todo_db)

    # Normally you should not admit, that the to-do exists, but...
    if todo.user_id != user.id:
        raise HTTPException(403, "You don't have access to this item")

    return todo


@router.patch("/todo/{todo_id}", response_model=ReturnTodo)
async def update_todo(todo_id: int, partial_todo: PartialTodo, request: Request) -> ReturnTodo:
    todo = retrieve_todo(todo_id, request)

    user = get_user_from_request(request)
    if todo.user_id != user.id:
        raise HTTPException(403, "You don't have access to this item")

    todo.merge_in(partial_todo)
    todo_dict = todo.dict()
    del todo_dict["id"]
    TODO_TABLE.update(todo_dict, doc_ids=[todo_id])
    return todo


@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int, request: Request) -> None:
    todo = retrieve_todo(todo_id, request)

    user = get_user_from_request(request)
    if todo.user_id != user.id:
        raise HTTPException(403, "You don't have access to this item")

    TODO_TABLE.remove(doc_ids=[todo_id])


@router.get("/todo", response_model=List[ReturnTodo])
async def get_todos(request: Request, order: OrderBy = None, reverse: bool = False) -> List[ReturnTodo]:
    todo_items = get_todos_from_db(request)

    if order:
        todo_items.sort(key=lambda i: getattr(i, order.value), reverse=reverse)

    return todo_items


@router.post("/todo", response_model=ReturnTodo)
async def create_todo(post_todo: PostTodo, request: Request) -> ReturnTodo:
    user = get_user_from_request(request)
    todo = ToDo(**post_todo.dict(), date=time.time(), user_id=user.id)
    todo_id = TODO_TABLE.insert(todo.dict())
    return ReturnTodo(**todo.dict(), id=todo_id)


@router.get("/tags", response_model=List[str])
async def get_tags(request: Request) -> List[str]:
    todo_list = get_todos_from_db(request)

    tag_list: List[str] = []
    for todo in todo_list:
        for tag in todo.tags:
            tag_list.append(tag)

    return sorted(list(set(tag_list)))


@router.get("/tags/{tag}", response_model=List[ReturnTodo])
async def get_tag(tag: str, request: Request) -> List[ReturnTodo]:
    todo_list = get_todos_from_db(request)

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if tag in todo.tags:
            return_list.append(todo)

    return return_list


@router.get("/search", response_model=List[ReturnTodo])
async def search(q: str, request: Request) -> List[ReturnTodo]:
    todo_list = get_todos_from_db(request)

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if q.lower() in todo.heading.lower() or q.lower() in todo.content.lower():
            return_list.append(todo)

    return return_list
