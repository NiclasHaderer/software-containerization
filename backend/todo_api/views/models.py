from __future__ import annotations

from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class PasswordChange(BaseModel):
    old_password: str
    new_password: str


class PartialTodo(BaseModel):
    heading: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    imageUrl: Optional[str]
    done: Optional[bool]


class PostTodo(BaseModel):
    heading: str
    content: str
    tags: List[str] = Field(default_factory=list)
    done: bool = Field(default=False)
    imageUrl: Optional[str]

    def merge_in(self, todo: PartialTodo) -> None:
        if todo.heading is not None:
            self.heading = todo.heading

        if todo.content is not None:
            self.content = todo.content

        if todo.tags is not None:
            self.tags = todo.tags

        if todo.imageUrl is not None:
            self.imageUrl = todo.imageUrl

        if todo.done is not None:
            self.done = todo.done


class ToDo(PostTodo):
    date: float


class ReturnTodo(ToDo):
    id: int


class OrderBy(Enum):
    date = "date"
    title = "title"
