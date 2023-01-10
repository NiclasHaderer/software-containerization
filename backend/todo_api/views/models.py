from __future__ import annotations

import base64
import json
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class User(BaseModel):
    username: str
    token: str
    id: int

    def password_valid(self, password: str) -> bool:
        token = User.generate_token(self.username, password)
        return token == self.token

    @staticmethod
    def generate_token(username: str, password: str) -> str:
        token_object = {
            "username": username,
            "password": password
        }
        token_str = bytes(f"{json.dumps(token_object)}", encoding="UTF_8")
        return str(base64.encodebytes(token_str), encoding="UTF_8").replace("\n", "")


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
    user_id: int


class ReturnTodo(ToDo):
    id: int


class Login(BaseModel):
    username: str
    password: str


class OrderBy(Enum):
    date = "date"
    title = "title"
