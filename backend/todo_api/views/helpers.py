import uuid
from datetime import datetime
from typing import List
from uuid import UUID

from fastapi import HTTPException

from todo_api.database import get_db
from todo_api.views.models import ReturnTodo, PostToDo


async def retrieve_todo(todo_id: UUID) -> ReturnTodo:
    db = await get_db()
    todo_item = await db.fetch_one("""SELECT * from todos WHERE id = :id""", {"id": todo_id})
    if todo_item is None:
        raise HTTPException(404, "Item not found")

    return ReturnTodo(**todo_item._mapping)


async def get_todos_from_db() -> List[ReturnTodo]:
    db = await get_db()
    todos = await db.fetch_all("SELECT * from todos")
    return [ReturnTodo(**todo._mapping) for todo in todos]


async def save_todo(todo: ReturnTodo | PostToDo) -> ReturnTodo:
    db = await get_db()
    if isinstance(todo, ReturnTodo):
        update_dict = todo.dict()
        del update_dict["created"]
        await db.execute(
            """UPDATE todos
                SET content  = :content,
                    done     = :done,
                    heading  = :heading,
                    image_url = :image_url,
                    tags     = :tags
                WHERE id = :id
            """,
            update_dict
        )
        return todo
    else:
        todo_id = uuid.uuid4()
        await db.execute(
            """
            INSERT INTO todos (id, heading, content, done, image_url, created, tags)
            VALUES (:id, :heading, :content, :done, :image_url, :created, :tags)
            """, {
                **todo.dict(),
                "id": todo_id,
                "created": datetime.now().timestamp()
            })
        return await retrieve_todo(todo_id)


async def delete_todo(todo_id: UUID) -> None:
    db = await get_db()
    await db.execute("""DELETE FROM todos WHERE id = :id""", {"id": todo_id})
