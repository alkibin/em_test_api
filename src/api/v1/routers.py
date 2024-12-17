from fastapi import APIRouter

from authors import router as authort_router
from book import router as book_router
from borrow import router as borrow_router


router = APIRouter()
router.include_router(authort_router)
router.include_router(book_router)
router.include_router(borrow_router)