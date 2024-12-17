from fastapi import Depends

from src.models import Author
from src.db.session import AsyncSession, get_session


class BorrowService:
    def __init__(self, session: AsyncSession):
        self.session = session




def get_borrow_service(session=Depends(get_session)):
    return BorrowService(session)
