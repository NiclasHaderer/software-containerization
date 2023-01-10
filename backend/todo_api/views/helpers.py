from typing import List

from todo_api.database import TODO_TABLE
from todo_api.views.models import ReturnTodo


def retrieve_todo(todo_id: int) -> ReturnTodo:
    todo_db = TODO_TABLE.get(doc_id=todo_id)
    return ReturnTodo(**todo_db, id=todo_db.doc_id)


def get_todos_from_db() -> List[ReturnTodo]:
    todo_items = TODO_TABLE.all()
    return [ReturnTodo(**todo, id=todo.doc_id) for todo in todo_items]
