import uuid

from pydantic import BaseModel, ConfigDict
from books import CreateBookSchema
from . author import CreateAuthorSchema


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
    books: BookResponse


class BookResponseList(BaseModel):
    books: list[BookResponse]
    model_config = ConfigDict(
        from_attributes=True
    )
