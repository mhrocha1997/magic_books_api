from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Book
from sqlalchemy.orm import Session
from database.connection import get_db
import string
import random
from database import models

router = APIRouter()

def generate_magic_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@router.post('/')
async def create_book(request: Book, db: Session = Depends(get_db)):
    try:
        new_book = models.Book(
            title=request.title,
            author=request.author,
            teacher=request.teacher,
            magic_code=generate_magic_code()
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return new_book
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e,
        )

@router.get('/{magic_code}', status_code=201)
async def get_book_by_magic_code(magic_code, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter_by(magic_code=magic_code).first()

        if not book:
            return HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail='Invalid Magic Code',
            )

        pages = db.query(models.Page).filter_by(book_id=book.id).all()
        if pages:
            book.__dict__["pages"] = pages
        return book
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get book",
        )
