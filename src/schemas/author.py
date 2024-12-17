from datetime import datetime

from pydantic import BaseModel


class CreateAuthorSchema(BaseModel):
    name: str
    surname: str
    birthdate: datetime


class UpdateAuthorSchema(BaseModel):
    title: str | None = None
    surname: str | None = None
    birthdate: str | None = None


