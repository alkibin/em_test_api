from datetime import datetime

from pydantic import BaseModel


class CreateAuthorSchema(BaseModel):
    name: str
    surname: str
    birthdate: datetime


class UpdateAuthorSchema(CreateAuthorSchema):
    pass


