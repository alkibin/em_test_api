import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .author import CreateAuthorSchema
from .books import CreateBookSchema


class AuthorResponse(CreateAuthorSchema):
    id: uuid.UUID


class AuthorResponseList(BaseModel):
    authors: list[AuthorResponse]


class BookResponse(CreateBookSchema):
    id: uuid.UUID

    model_config = ConfigDict(
        from_attributes=True
    )


class BookResponseList(BaseModel):
    books: list[BookResponse]
    model_config = ConfigDict(
        from_attributes=True
    )


class BorrowResponse(BaseModel):
    book_id: uuid.UUID
    user_id: uuid.UUID
    expected_return_date: datetime | None = None


class BorrowResponseList(BaseModel):
    borrows: list[BorrowResponse]