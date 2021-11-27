from pydantic import BaseModel

class Page(BaseModel):
    text: str
    image: str


class Book(BaseModel):
    title: str
    author: str
    teacher: str