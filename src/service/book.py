from fastapi import Depends

from src.models import Book
from src.db.session import AsyncSession, get_session


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_book(self, book_data):
        existing_book = await Book.get_by_args(self.session, **book_data.model_dump())
        if existing_book:
            return None

        new_book = Book(**book_data)
        self.session.add(new_book)
        await self.session.commit()
        return new_book

    async def get_all(self, params):
        return await Book.get_all(self.session, params.page_size, params.page_number)

    async def get_book_info(self, book_id):
        return await Book.get_by_args(self.session, id=book_id)





def get_book_service(session=Depends(get_session)):
    return BookService(session)
