from datetime import datetime
from typing import Annotated

from fastapi import Query, HTTPException, status
from pydantic import BaseModel


class Pagination(BaseModel):
    page_number: Annotated[int, Query(ge=0)] = 0
    page_size: Annotated[int, Query(ge=1)] = 20


class PaginationWithDT(Pagination):
    start_date: datetime = datetime.min
    end_date: datetime = datetime.max


class HTTPErrors:
    @staticmethod
    def not_found(entity: str = "Entity"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} not found",
        )

    @staticmethod
    def already_exists(entity: str = "Entity"):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{entity} already exists",
        )

    @staticmethod
    def no_book_in_stock():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No book in stock",
        )

    @staticmethod
    def book_already_returned():
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book already returned",
        )

