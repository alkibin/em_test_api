from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas import CreateAuthorSchema, UpdateAuthorSchema, AuthorResponse, AuthorResponseList
from src.schemas import Pagination
from src.service.author import AuthorService, get_author_service

router = APIRouter(prefix='/api/v1/authors', tags=['authors'])


@router.post('/', response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
        params: CreateAuthorSchema,
        service: AuthorService = Depends(get_author_service)
):
    result = await service.add_author(params)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Автор уже существует'
        )
    return result


@router.get('/', response_model=AuthorResponseList, status_code=status.HTTP_200_OK)
async def get_authors(
        params=Depends(Pagination),
        service: AuthorService = Depends(get_author_service)
):
    authors = await service.get_all(params)
    return {'authors': authors}


@router.get('/{id}', response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def find_author(
        id: UUID,
        service: AuthorService = Depends(get_author_service)
):
    author = await service.find_author(author_id=id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=''
        )
    return {'author': author}


@router.put("/{id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def update_author(
        id: UUID,
        user_data: UpdateAuthorSchema,
        service: AuthorService = Depends(get_author_service)
):
    author = await service.update(id, user_data)
    if author is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=''
        )
    return author


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        id: UUID,
        service: AuthorService = Depends(get_author_service)
):
    result = await service.delete_author(id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Автор не найден'
        )
    return {'msg': 'success'}
