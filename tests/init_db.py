import asyncio
import random
import uuid
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy import text

from src.core.config import settings
from src.db.base import engine
from src.db.session import async_session
from src.models import Book, Author, User, Borrow
from src.models.common import Base

faker = Faker('ru_RU')


async def create_schema(engine):
    async with engine.begin() as conn:
        await conn.execute(text('CREATE SCHEMA IF NOT EXISTS book_library'))


async def init_db() -> None:
    await create_schema(engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(text('DROP SCHEMA IF EXISTS book_library CASCADE'))


author_uuids = [uuid.uuid4() for _ in range(1000)]
book_uuids = [uuid.uuid4() for _ in range(5000)]
user_uuids = [uuid.uuid4() for _ in range(500)]
borrow_uuids1 = [uuid.uuid4() for _ in range(100)]
borrow_uuids2 = [uuid.uuid4() for _ in range(50)]


async def fill_bd_test_data():
    async with async_session() as session:
        for author_uuid in author_uuids:
            session.add(
                Author(
                    id=author_uuid,
                    name=faker.first_name(),
                    surname=faker.last_name(),
                    birthdate=faker.date_of_birth(minimum_age=18, maximum_age=500)
                )
            )

        for book_uuid in book_uuids:
            session.add(
                Book(
                    id=book_uuid,
                    title=faker.catch_phrase(),
                    description=faker.text(max_nb_chars=100),
                    author_id=random.choice(author_uuids),
                    quantity=random.randint(1, 100)
                )
            )

        for user_uuid in user_uuids:
            session.add(
                User(
                    id=user_uuid,
                    name=faker.first_name(),
                    surname=faker.last_name(),
                )
            )

        await session.commit()
        now = datetime.now()
        for i in range(100):
            borrow_dt = faker.date_time(end_datetime=now - timedelta(days=settings.borrow_period))
            closed_borrows = Borrow(
                id=borrow_uuids1[i],
                book_id=random.choice(book_uuids),
                user_id=random.choice(user_uuids),
                borrow_dt=borrow_dt,
                return_dt=borrow_dt + timedelta(random.randint(5, 100))
            )
            session.add(closed_borrows)

        for i in range(50):
            user_id = user_uuids.pop()
            open_borrows = Borrow(
                id=borrow_uuids2[i],
                book_id=random.choice(book_uuids),
                user_id=user_id,
                borrow_dt=faker.past_datetime(),
            )
            session.add(open_borrows)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(fill_bd_test_data())
