from logging import raiseExceptions
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Book, CompleteBook
from sqlalchemy.orm import Session
from database.connection import get_db
import string
import random
from database import models

router = APIRouter()

def generate_magic_code(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(request: Book, db: Session = Depends(get_db)):
    try:
        """
            Create a new book.
        """
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
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create book",
        )

@router.get('/')
async def get_all_books(db: Session = Depends(get_db)):
    try:
        """
            List all books created without their pages. To see them you need to 
            get the book by specifically by the Magic Code.
        """
        books = db.query(models.Book).all()
        
        if not books:
            return HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail="No Book Found."
            )
        
        return books
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get books."
        )

@router.get('/{magic_code}', response_model=CompleteBook)
async def get_book_by_magic_code(magic_code, db: Session = Depends(get_db)):
    try:
        """
            Finds the book by the Magic Code.
        """
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
    except HTTPException as e:
        raise e
    except:
         raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Couldn't get book",
            )

@router.delete('/{id}')
def delete_book(id, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter_by(id=id)
        if not book.first():
            if not book.fist():
                return HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Book with id {id} not found',
                    )

        book.delete(synchronize_session=False)
        db.commit()
        return f'Book {id} deleted.'
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't delete book.",
        )

@router.put('/{id}')
def update_book(id,  request: Book, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter_by(id=id)
        
        if not book.first():
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Book with id {id} not found',
                )

        book.update(request.dict())
        db.commit()
        return book.first()
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't update book.",
        )
