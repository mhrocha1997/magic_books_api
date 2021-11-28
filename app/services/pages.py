from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import models

def create(request_body, book_id, db: Session):
    book = db.query(models.Book).filter_by(id=book_id).first()
        
    if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Book with id {book_id} not found.',
            )

    pages = db.query(models.Page).filter_by(book_id=book_id).count()
    
    if pages >=6:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Limit of pages for this book already reached.'
        )

    new_page = models.Page(
        text=request_body.text,
        image=request_body.image,
        book_id=book_id
    )

    db.add(new_page)
    db.commit()
    db.refresh(new_page)

    return new_page.__dict__

def get_by_id(id, db: Session):
    page = db.query(models.Page).filter_by(id=id).first()

    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Page with id {id} not found.',
        )

    return page.__dict__

def update(id, request_body, db: Session):
    page = db.query(models.Page).filter_by(id=id)

    if not page.first():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Page with id {id} not found.',
            )

    page.update(request_body.dict())
    db.commit()
    return page.first().__dict__

def delete(id, db: Session):
    page = db.query(models.Page).filter_by(id=id)

    if not page.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Page with id {id} not found.'
        )
    page.delete(synchronize_session=False)
    db.commit()
    return f'Page {id} deleted.'
