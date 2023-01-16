from __future__ import annotations

from enum import Enum
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


class PartialTodo(BaseModel):
    heading: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    image_url: Optional[str]
    done: Optional[bool]


class PostToDo(BaseModel):
    heading: str
    content: str
    tags: List[str] = Field(default_factory=list, )
    done: bool = Field(default=False)
    image_url: Optional[str]

    def merge_in(self, todo: PartialTodo) -> None:
        if todo.heading is not None:
            self.heading = todo.heading

        if todo.content is not None:
            self.content = todo.content

        if todo.tags is not None:
            self.tags = todo.tags

        if todo.image_url is not None:
            self.image_url = todo.image_url

        if todo.done is not None:
            self.done = todo.done


class ReturnTodo(PostToDo):
    created: float
    id: UUID


class OrderBy(Enum):
    date = "date"
    title = "title"


class VersionResponse(BaseModel):
    version: str
