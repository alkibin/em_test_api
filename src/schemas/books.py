import uuid

from pydantic import BaseModel, Field


class CreateBookSchema(BaseModel):
    title: str
    description: str
    author_id: uuid.UUID
    quantity: int = Field(0, ge=0)


class UpdateBookSchema(CreateBookSchema):
    pass


class BookFindParams(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None

