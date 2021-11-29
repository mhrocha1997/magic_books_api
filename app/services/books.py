from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import models
import string
import random


def generate_magic_code(size=6, chars=string.ascii_uppercase):
    """
        Generates Magic Code with 6 random capital letters.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def create(db: Session, body):
    new_book = models.Book(
        title=body.title,
        author=body.author,
        teacher=body.teacher,
        magic_code=generate_magic_code()
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book.__dict__


def get_all(db: Session):
    books = db.query(models.Book).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Book Found."
        )

    response_books = {"books": [book.__dict__ for book in books]}
    return response_books


def get_by_magic_code(magic_code, db: Session):
    book = db.query(models.Book).filter_by(magic_code=magic_code).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with Magic Code {magic_code} not found',
        )

    pages = db.query(models.Page).filter_by(book_id=book.id).all()
    if pages:
        book.__dict__["pages"] = [page.__dict__ for page in pages]
    return book.__dict__


def update(id, body, db: Session):
    book = db.query(models.Book).filter_by(id=id)

    if not book.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with id {id} not found',
        )

    book.update(body.dict())
    db.commit()
    return book.first().__dict__


def delete(id, db: Session):
    book = db.query(models.Book).filter_by(id=id)
    if not book.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with id {id} not found',
        )

    book.delete(synchronize_session=False)
    db.commit()
    return f'Book {id} deleted.'
