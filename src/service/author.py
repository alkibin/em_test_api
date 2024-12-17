from fastapi import Depends

from src.db.session import AsyncSession, get_session
from src.models import Author
from src.schemas import HTTPErrors


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_author(self, params):
        existing_author = await Author.get_by_args(self.session, **params.model_dump())
        if existing_author:
            raise HTTPErrors.already_exists('author')

        author = Author(**params.model_dump())
        self.session.add(author)
        await self.session.commit()
        return author

    async def get_all(self, params):
        return await Author.get_all(
            self.session,
            params.page_size,
            params.page_number
        )

    async def find_author(self, author_id):
        author = await self.session.get(Author, author_id)
        if author is None:
            raise HTTPErrors.not_found('author')
        return author

    async def update(self, author_id, user_data):
        author = await self.session.get(Author, author_id)
        if not author:
            raise HTTPErrors.not_found('author')

        update_values = {
            key: val for key, val in user_data.model_dump().items()
            if hasattr(author, key) and val is not None
        }
        for key, val in update_values.items():
            setattr(author, key, val)

        self.session.add(author)
        await self.session.commit()
        return author

    async def delete_author(self, author_id):
        author = await self.session.get(Author, author_id)
        if not author:
            raise HTTPErrors.not_found('author')

        await self.session.delete(author)
        await self.session.commit()


def get_author_service(session=Depends(get_session)):
    return AuthorService(session)
