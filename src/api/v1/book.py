from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas import CreateBookSchema, Pagination
from src.schemas import BookResponse, BookResponseList
from src.service.book import get_book_service, BookService

router = APIRouter(prefix='/api/v1/books', tags=['books'])


@router.post('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
        book_data: CreateBookSchema,
        service: BookService = Depends(get_book_service)
):
    await service.add_book(book_data)


@router.get('/', response_model=BookResponseList, status_code=status.HTTP_201_CREATED)
async def get_books(
        params=Depends(Pagination),
        service: BookService = Depends(get_book_service)
):
    books = await service.get_all(params)
    return {'books': books}


@router.get('/{id}', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def get_book_info(
        id: int,
        service: BookService = Depends(get_book_service)
):
    book = await service.get_book_info(book_id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book


@router.put('/{id}', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def get_book_info():
    pass


@router.delete('/{id}', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def get_book_info():
    pass




