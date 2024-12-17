from fastapi import Depends

from src.models import Author
from src.db.session import AsyncSession, get_session


class AuthorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_author(self, params):
        existing_author = await Author.get_by_args(self.session, **params.model_dump())
        if existing_author:
            return None

        author = Author(**params.model_dump())
        self.session.add(author)
        await self.session.commit()
        return author

    async def get_all(self, params):
        return await Author.get_all(self.session, params)

    async def find_author(self, author_id):
        return await Author.get_by_args(self.session, id=author_id)

    async def update(self, author_id, user_data):
        user = await Author.get_by_args(self.session, id=author_id)
        if not user:
            return None
        update_values = {
            key: val for key, val in user_data.model_dict()
            if hasattr(user, key) and val is not None
        }
        for key, val in update_values:
            setattr(user, key, val)

        self.session.add(user)
        await self.session.commit()
        return user

    async def delete_author(self, author_id):
        author = await Author.get_by_args(self.session, id=author_id)
        if author:
            await self.session.remove(author)
            await self.session.commit()


def get_author_service(session=Depends(get_session)):
    return AuthorService(session)
