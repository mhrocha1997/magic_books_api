from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_406_NOT_ACCEPTABLE
from schemas import Page, PageWithId
from sqlalchemy.orm import Session
from database.connection import get_db
from database import models

router = APIRouter()

@router.post('/book/{book_id}', status_code=status.HTTP_201_CREATED, response_model=PageWithId)
async def create_page(request: Page, book_id, db: Session = Depends(get_db)):
    """
        Create one page and attach it to the book. It'can't be created more than six pages.         
    """
    try:
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
            text=request.text,
            image=request.image,
            book_id=book_id
        )

        db.add(new_page)
        db.commit()
        db.refresh(new_page)

        return new_page.__dict__
        
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create page",
        )

@router.get('/{id}', response_model=PageWithId)
async def get_page_by_id(id, db: Session = Depends(get_db)):
    """
        Find the page by its id.
    """
    try:
        page = db.query(models.Page).filter_by(id=id).first()

        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Page with id {id} not found.',
            )

        return page.__dict__

    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get page",
        )

@router.put('/{id}', response_model=PageWithId)
async def update_page(id, request: Page, db: Session = Depends(get_db)):
    """
        Update page's text and image.
    """
    try:
        page = db.query(models.Page).filter_by(id=id)

        if not page.first():
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Page with id {id} not found.',
                )

        page.update(request.dict())
        db.commit()
        return page.first().__dict__

    except HTTPException as e:
        raise e 
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't update page.",
        )

@router.delete('/{id}')
async def delete_page(id, db: Session = Depends(get_db)):
    """
        Delete the page.
    """
    try:
        page = db.query(models.Page).filter_by(id=id)

        if not page.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Page with id {id} not found.'
            )
        page.delete(synchronize_session=False)
        db.commit()
        return f'Page {id} deleted.'

    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detailt="couldn't delete page."
        )
