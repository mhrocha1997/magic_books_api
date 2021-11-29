from fastapi import APIRouter, Depends, HTTPException, status
from starlette.status import HTTP_406_NOT_ACCEPTABLE
from schemas import Page, PageWithId
from sqlalchemy.orm import Session
from database.connection import get_db
from services import pages
router = APIRouter()


@router.post('/book/{book_id}', status_code=status.HTTP_201_CREATED, response_model=PageWithId)
async def create_page(request: Page, book_id, db: Session = Depends(get_db)):
    """
        Create one page and attach it to the book. It'can't be created more than six pages.
        The image must be sent as base64 encoded.      
    """
    try:
        return pages.create(request, book_id, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't create page",
        )


@router.get('/{page_id}', response_model=PageWithId)
async def get_page_by_id(page_id, db: Session = Depends(get_db)):
    """
        Find the page by its id.
    """
    try:
        return pages.get_by_id(page_id, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't get page",
        )


@router.put('/{page_id}', response_model=PageWithId)
async def update_page(page_id, request: Page, db: Session = Depends(get_db)):
    """
        Update page's text and image.
    """
    try:
        return pages.update(page_id, request, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't update page.",
        )


@router.delete('/{page_id}')
async def delete_page(page_id, db: Session = Depends(get_db)):
    """
        Delete the page.
    """
    try:
        return pages.delete(page_id, db)
    except HTTPException as e:
        raise e
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="couldn't delete page."
        )
