from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base

class Book(Base):
    __tablename__='books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    teacher = Column(String)
    magic_code = Column(String, unique=True)

    pages = relationship("Page", back_populates="book")

class Page(Base):
    __tablename__='pages'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    image = Column(String)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="pages")