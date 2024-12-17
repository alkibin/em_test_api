from fastapi import Depends

from src.db.session import AsyncSession, get_session
from src.models import Book, Author
from src.schemas import HTTPErrors


class BookService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_book(self, book_data):
        existing_book = await Book.get_by_args(self.session, **book_data.model_dump())
        if existing_book:
            raise HTTPErrors.already_exists(f'book {book_data.title}')

        author = await self.session.get(Author, book_data.author_id)
        if author is None:
            raise HTTPErrors.not_found(f'author')

        new_book = Book(**book_data.model_dump())
        self.session.add(new_book)
        await self.session.commit()
        return new_book

    async def get_all(self, params):
        return await Book.get_all(self.session, params.page_size, params.page_number)

    async def get_book_info(self, book_id):
        book = await self.session.get(Book, book_id)
        if book is None:
            raise HTTPErrors.not_found(f'book')
        return book

    async def update_book_info(self, book_id, new_data):
        book = await Book.get_with_author(self.session, id=book_id)
        if book is None:
            raise HTTPErrors.not_found('book')
        if new_data.author_id:
            author = await self.session.get(Author, new_data.author_id)
            if author is None:
                raise HTTPErrors.not_found('author')

        upd_data = {
            key: val for key, val in new_data.model_dump().items()
            if hasattr(book, key) and val is not None
        }
        for key, val in upd_data.items():
            setattr(book, key, val)
        await self.session.commit()
        return book

    async def remove_book(self, book_id):
        book = await self.session.get(Book, book_id)
        if book is None:
            raise HTTPErrors.not_found()

        await self.session.delete(book)
        await self.session.commit()


def get_book_service(session=Depends(get_session)):
    return BookService(session)
