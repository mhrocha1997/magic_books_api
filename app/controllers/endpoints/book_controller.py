from fastapi import APIRouter, Depends
from schemas import Book
from sqlalchemy.orm import Session
from database import get_db
import models

router = APIRouter()

@router.post('/')
async def create_book(request: Book, db: Session = Depends(get_db)):
    new_book = models.Book(
        title=request.title,
        author=request.author,
        teacher=request.teacher,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book