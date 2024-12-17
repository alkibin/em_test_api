import uuid

from pydantic import BaseModel


class BorrowSchema(BaseModel):
    book_id: uuid.UUID
    user_id: uuid.UUID

