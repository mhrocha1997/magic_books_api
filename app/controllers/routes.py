from fastapi import APIRouter

from .endpoints import books
from .endpoints import pages

router = APIRouter()

router.include_router(books.router, prefix='/books', tags=['books'])
router.include_router(pages.router, prefix='/pages', tags=['pages'])