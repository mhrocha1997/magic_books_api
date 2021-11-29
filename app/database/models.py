from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.connection import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    magic_code = Column(String, unique=True, nullable=False)

    pages = relationship("Page", passive_deletes=True, back_populates="book")


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    image = Column(String, nullable=False)
    book_id = Column(Integer, ForeignKey(
        "books.id", ondelete="CASCADE"), nullable=False)

    book = relationship("Book", back_populates="pages")
