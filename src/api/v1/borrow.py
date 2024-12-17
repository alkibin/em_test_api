from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.book import CreateBookModel, BookFindParams, Pagination, BookStatus
from src.schemas.response import BookResponse, BookResponseList
from src.service.service import get_book_manager, BookService

router = APIRouter(prefix='/api/v1/borrow', tags=['borrow'])


@router.post('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow():
    pass


@router.get('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow():
    pass


@router.get('/{id}', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow():
    pass


@router.patch('/{id}/return', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow():
    pass