from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.schemas import BorrowSchema, BorrowResponse, PaginationWithDT, BorrowResponseList
from src.service.borrow import get_borrow_service, BorrowService

router = APIRouter(prefix='/api/v1/borrow', tags=['borrow'])


@router.post('/', response_model=BorrowResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow(
        borrow_data: BorrowSchema,
        service: BorrowService = Depends(get_borrow_service)
):
    return await service.lend_book(borrow_data)


@router.get('/', response_model=BorrowResponseList, status_code=status.HTTP_200_OK)
async def get_all_borrows(
        params=Depends(PaginationWithDT),
        service: BorrowService = Depends(get_borrow_service)
):
    result = await service.get_all(params)
    return {'borrows': result}


@router.get('/{id}', response_model=BorrowResponse, status_code=status.HTTP_200_OK)
async def get_one(
        id: UUID,
        service: BorrowService = Depends(get_borrow_service)
):
    return await service.get_one(id)


@router.patch('/{id}/return', status_code=status.HTTP_200_OK)
async def return_book(
        id: UUID,
        service: BorrowService = Depends(get_borrow_service)
):
    await service.return_book(id)
    return {'msg': 'success'}