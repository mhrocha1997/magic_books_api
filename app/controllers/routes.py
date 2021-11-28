from fastapi import APIRouter

from .endpoints import books
from .endpoints import pages

router = APIRouter()

router.include_router(books.router, prefix='/books', tags=['Books'])
router.include_router(pages.router, prefix='/pages', tags=['Pages'])