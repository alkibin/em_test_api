from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.schemas import CreateAuthorSchema, UpdateAuthorSchema, AuthorResponse, AuthorResponseList
from src.schemas import Pagination
from src.service.author import AuthorService, get_author_service

router = APIRouter(prefix='/api/v1/authors', tags=['authors'])


@router.post('/', response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
        params: CreateAuthorSchema,
        service: AuthorService = Depends(get_author_service)
):
    return await service.add_author(params)


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
    return await service.find_author(author_id=id)


@router.put("/{id}", response_model=AuthorResponse, status_code=status.HTTP_200_OK)
async def update_author(
        id: UUID,
        user_data: UpdateAuthorSchema,
        service: AuthorService = Depends(get_author_service)
):
    return await service.update(id, user_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_author(
        id: UUID,
        service: AuthorService = Depends(get_author_service)
):
    await service.delete_author(id)
