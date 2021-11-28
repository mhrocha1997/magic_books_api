from pydantic import BaseModel
from typing import List


class Page(BaseModel):
    text: str
    image: str


class Book(BaseModel):
    title: str
    author: str
    teacher: str


class CompleteBook(Book):
    pages: List[dict] = []

    class Config():
        orm_mode = True