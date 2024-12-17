import uuid

from datetime import datetime

from pydantic import BaseModel


class CreateBookSchema(BaseModel):
    title: str
    description: str
    author_id: uuid.UUID
    quantity: int


class BookFindParams(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None

