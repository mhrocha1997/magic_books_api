from fastapi import APIRouter, Depends, HTTPException, status
from schemas import AllBooks, Book, BookWithId, CompleteBook
from sqlalchemy.orm import Session
from database.connection import get_db
from services import books
router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookWithId)
async def create_book(request: Book, db: Session = Depends(get_db)):
    """
        Create a new book.
    """
    try:
        return books.create(db, request)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create book.",
        )


@router.get('/', response_model=AllBooks)
async def get_all_books(db: Session = Depends(get_db)):
    """
        List all books created without their pages. To see them you need to 
        get the book specifically by the Magic Code.
    """
    try:
        return books.get_all(db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get books."
        )


@router.get('/{magic_code}', response_model=CompleteBook)
async def get_book_by_magic_code(magic_code, db: Session = Depends(get_db)):
    """
        Find the book by its Magic Code.
    """
    try:
        return books.get_by_magic_code(magic_code, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get book.",
        )


@router.put('/{book_id}', response_model=BookWithId)
def update_book(book_id,  request: Book, db: Session = Depends(get_db)):
    """
        Update all book's attributes. You must provide all of them, otherwise, it will fail.
    """
    try:
        return books.update(book_id, request, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't update book.",
        )


@router.delete('/{book_id}')
def delete_book(book_id, db: Session = Depends(get_db)):
    """
        Delete the book.
    """
    try:
        return books.delete(book_id, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't delete book.",
        )
