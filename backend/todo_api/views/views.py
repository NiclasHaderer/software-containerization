from typing import List
from uuid import UUID

from fastapi import APIRouter

from todo_api.views.helpers import retrieve_todo, get_todos_from_db, save_todo, delete_todo as delete_todo_db
from todo_api.views.models import PartialTodo, ReturnTodo, PostToDo, OrderBy, VersionResponse

from todo_api.settings import SETTINGS

router = APIRouter(prefix=SETTINGS.api_prefix)


@router.get("/todo/{todo_id}", response_model=ReturnTodo)
async def get_todo(todo_id: UUID) -> ReturnTodo:
    return await retrieve_todo(todo_id)


@router.patch("/todo/{todo_id}", response_model=ReturnTodo)
async def update_todo(todo_id: UUID, partial_todo: PartialTodo) -> ReturnTodo:
    todo = await retrieve_todo(todo_id)
    todo.merge_in(partial_todo)
    return await save_todo(todo)


@router.delete("/todo/{todo_id}")
async def delete_todo(todo_id: UUID) -> None:
    await delete_todo_db(todo_id)


@router.get("/todo", response_model=List[ReturnTodo])
async def get_todos(order: OrderBy = None, reverse: bool = False) -> List[ReturnTodo]:
    todo_items = await get_todos_from_db()

    if order:
        todo_items.sort(key=lambda item: getattr(item, order.value()), reverse=reverse)

    return todo_items


@router.post("/todo", response_model=ReturnTodo)
async def create_todo(post_todo: PostToDo) -> ReturnTodo:
    return await save_todo(post_todo)


@router.get("/tags", response_model=List[str])
async def get_tags() -> List[str]:
    todo_list = await get_todos_from_db()

    tag_list: List[str] = []
    for todo in todo_list:
        for tag in todo.tags:
            tag_list.append(tag)

    return sorted(list(set(tag_list)))


@router.get("/tags/{tag}", response_model=List[ReturnTodo])
async def get_tag(tag: str) -> List[ReturnTodo]:
    todo_list = await get_todos_from_db()

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if tag in todo.tags:
            return_list.append(todo)

    return return_list


@router.get("/search", response_model=List[ReturnTodo])
async def search(q: str) -> List[ReturnTodo]:
    todo_list = await get_todos_from_db()

    return_list: List[ReturnTodo] = []

    for todo in todo_list:
        if q.lower() in todo.heading.lower() or q.lower() in todo.content.lower():
            return_list.append(todo)

    return return_list


@router.get("/version", response_model=VersionResponse)
def get_version() -> VersionResponse:
    return VersionResponse(version="1.0.0")
