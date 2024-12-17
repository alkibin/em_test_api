from typing import Annotated

from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    page_number: Annotated[int, Query(ge=0)] = 0
    page_size: Annotated[int, Query(ge=1)] = 20
