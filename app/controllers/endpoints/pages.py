from fastapi import APIRouter, Depends, HTTPException, status
from schemas import Page
from sqlalchemy.orm import Session
from database.connection import get_db
from database import models

router = APIRouter()

@router.post('/book/{book_id}')
async def create_page(request: Page, book_id, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter_by(id=book_id).one()
        
        if not book:
            if not book:
                return HTTPException(
                    status_code=status.HTTP_204_NO_CONTENT,
                    detail="Book doesn't exists",
                )

        new_page = models.Page(
            text=request.text,
            image=request.image,
            book_id=book_id
        )

        db.add(new_page)
        db.commit()
        db.refresh(new_page)

        return new_page
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create page",
        )
