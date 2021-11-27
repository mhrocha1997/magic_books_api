from fastapi import APIRouter, Depends
from schemas import Page
from sqlalchemy.orm import Session
from database import get_db
router = APIRouter()

@router.post('/book/{id}')
async def create_page(request: Page, id, db: Session = Depends(get_db)):
    pass
