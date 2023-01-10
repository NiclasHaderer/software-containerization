import time
from typing import List

from fastapi import APIRouter, HTTPException

from todo_api.database import TODO_TABLE
from todo_api.views.helpers import retrieve_todo, get_todos_from_db
from todo_api.views.models import PartialTodo, ReturnTodo, PostTodo, ToDo, OrderBy

router = APIRouter()


@router.get("/todo/{todo_id}", response_model=ReturnTodo)
async def get_todo(todo_id: int) -> ReturnTodo:
    todo_db = TODO_TABLE.get(todo_id)

    if not todo_db:
        raise HTTPException(404, "Item not found")

    return ReturnTodo(**todo_db)


@router.patch("/todo/{todo_id}", response_model=ReturnTodo)
async def update_todo(todo_id: int, partial_todo: PartialTodo) -> ReturnTodo:
    todo = retrieve_todo(todo_id)
    todo.merge_in(partial_todo)
    todo_dict = todo.dict()
    del todo_dict["id"]
    TODO_TABLE.update(todo_dict, doc_ids=[todo_id])
    return todo


@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: int) -> None:
    TODO_TABLE.remove(doc_ids=[todo_id])


@router.get("/todo", response_model=List[ReturnTodo])
async def get_todos(order: OrderBy = None, reverse: bool = False) -> List[ReturnTodo]:
    todo_items = get_todos_from_db()

    if order:
        todo_items.sort(key=lambda item: getattr(item, order.value()), reverse=reverse)

    return todo_items


@router.post("/todo", response_model=ReturnTodo)
async def create_todo(post_todo: PostTodo) -> ReturnTodo:
    todo = ToDo(**post_todo.dict(), date=time.time())
    todo_id = TODO_TABLE.insert(todo.dict())
    return ReturnTodo(**todo.dict(), id=todo_id)


@router.get("/tags", response_model=List[str])
async def get_tags() -> List[str]:
    todo_list = get_todos_from_db()

    tag_list: List[str] = []
    for todo in todo_list:
        for tag in todo.tags:
            tag_list.append(tag)

    return sorted(list(set(tag_list)))


@router.get("/tags/{tag}", response_model=List[ReturnTodo])
async def get_tag(tag: str) -> List[ReturnTodo]:
    todo_list = get_todos_from_db()

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if tag in todo.tags:
            return_list.append(todo)

    return return_list


@router.get("/search", response_model=List[ReturnTodo])
async def search(q: str) -> List[ReturnTodo]:
    todo_list = get_todos_from_db()

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if q.lower() in todo.heading.lower() or q.lower() in todo.content.lower():
            return_list.append(todo)

    return return_list
