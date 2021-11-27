from fastapi import APIRouter

from .endpoints import book_controller
from . endpoints import page_controller

router = APIRouter()

router.include_router(book_controller.router, prefix='/books', tags=['books'])
router.include_router(page_controller.router, prefix='/pages', tags=['pages'])