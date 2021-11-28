from pydantic import BaseModel
from typing import List


class Page(BaseModel):
    text: str
    image: str

class PageWithId(Page):
    id: int
    book_id: int

class Book(BaseModel):
    title: str
    author: str
    teacher: str

class BookWithId(Book):
    id: int
    magic_code: str

class AllBooks(BaseModel):
    books: List[BookWithId]

    class Config():
        orm_mode=True

class CompleteBook(Book):
    pages: List[dict] = []

    class Config():
        orm_mode = True