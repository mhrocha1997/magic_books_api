from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Book(Base):
    __tablename__='books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    teacher = Column(String)

    pages = relationship("Page", back_populates="owner")

class Page(Base):
    __tablename__='pages'
    id=Column(Integer, primary_key=True, index=True)
    text = Column(String)
    image = Column(String)
    owner_id = Column(Integer, ForeignKey("books.id"))

    owner = relationship("Book", back_populates="pages")