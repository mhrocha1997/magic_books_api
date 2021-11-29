from pydantic import BaseModel
from typing import List, Optional

from pydantic.types import constr


class Page(BaseModel):
    text: Optional[constr(min_length=4)]
    image: Optional[constr(min_length=4)]


class PageWithId(Page):
    id: int
    book_id: int


class Book(BaseModel):
    title: Optional[constr(min_length=4)]
    author: Optional[constr(min_length=4)]
    teacher: Optional[constr(min_length=4)]


class BookWithId(Book):
    id: int
    magic_code: str


class AllBooks(BaseModel):
    books: List[BookWithId]

    class Config():
        orm_mode = True


class CompleteBook(Book):
    pages: List[dict] = []

    class Config():
        orm_mode = True
