from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.schemas import BookResponse, BookResponseList
from src.schemas import CreateBookSchema, Pagination, UpdateBookSchema
from src.service.book import get_book_service, BookService

router = APIRouter(prefix='/api/v1/books', tags=['books'])


@router.post('/', response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(
        book_data: CreateBookSchema,
        service: BookService = Depends(get_book_service)
):
   return await service.add_book(book_data)


@router.get('/', response_model=BookResponseList, status_code=status.HTTP_200_OK)
async def get_books(
        params=Depends(Pagination),
        service: BookService = Depends(get_book_service)
):
    books = await service.get_all(params)
    return {'books': books}


@router.get('/{id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book_info(
        id: UUID,
        service: BookService = Depends(get_book_service)
):
    return await service.get_book_info(book_id=id)


@router.put('/{id}', response_model=BookResponse, status_code=status.HTTP_200_OK)
async def update_book_info(
        id: UUID,
        book_data: UpdateBookSchema,
        service: BookService = Depends(get_book_service)
):
    return await service.update_book_info(id, book_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_book_info(
        id: UUID,
        service: BookService = Depends(get_book_service)
):
    await service.remove_book(book_id=id)
