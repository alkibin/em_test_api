from datetime import datetime, timedelta

from fastapi import Depends

from src.core.config import settings
from src.db.session import AsyncSession, get_session
from src.models import Book, Borrow, User
from src.schemas import HTTPErrors, BorrowResponse


class BorrowService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def lend_book(self, borrow_data):
        book = await self.session.get(Book, borrow_data.book_id)
        if book is None:
            raise HTTPErrors.not_found('book')
        if book.quantity == 0:
            raise HTTPErrors.no_book_in_stock()
        user = await self.session.get(User, borrow_data.user_id)
        if user is None:
            raise HTTPErrors.not_found('user')

        borrow = Borrow(**borrow_data.model_dump())
        self.session.add(borrow)
        book.quantity -= 1

        await self.session.commit()
        now = datetime.now()

        return BorrowResponse(
            book_id=book.id,
            user_id=user.id,
            expected_return_date=now + timedelta(days=settings.borrow_period)
        )

    async def get_all(self, params):
        borrows = await Borrow.get_all(
            self.session,
            params.page_size,
            params.page_number,
            params.start_date,
            params.end_date
        )
        return [
            BorrowResponse(
                book_id=borrow.book_id,
                user_id=borrow.user_id,
                expected_return_date=borrow.borrow_dt + timedelta(days=settings.borrow_period)
            ) for borrow in borrows
        ]

    async def get_one(self, borrow_id):
        borrow = await self.session.get(Borrow, borrow_id)
        if borrow is None:
            raise HTTPErrors.not_found('borrow')

        return BorrowResponse(
            book_id=borrow_id.book_id,
            user_id=borrow_id.user_id,
            expected_return_date=borrow.borrow_dt + settings.borrow_period
        )

    async def return_book(self, borrow_id):
        borrow = await self.session.get(Borrow, borrow_id)
        if borrow is None:
            raise HTTPErrors.not_found('borrow')
        if borrow.return_dt:
            raise HTTPErrors.book_already_returned()

        book = await self.session.get(Book, borrow.book_id)
        book.quantity += 1
        borrow.return_dt = datetime.now()
        await self.session.commit()


def get_borrow_service(session=Depends(get_session)):
    return BorrowService(session)
