import uuid
from uuid import UUID
from datetime import datetime

from sqlalchemy import Column, Integer, String, insert, select, update, and_, or_, delete, func, ForeignKey, \
    CheckConstraint, UniqueConstraint
from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from src.schemas.book import BookStatusEnum


class Base(DeclarativeBase):
    pass

    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"{self.__class__.__name__}, {', '.join(cols)}"


class BaseWithId(Base):
    __abstract__ = True

    id: Mapped[uuid] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Author(BaseWithId):
    __tablename__ = "author"
    __table_args__ = (UniqueConstraint("name", "surname", "birth_date", name='name_surmane_birth_const'))

    name: Mapped[str]
    surname: Mapped[str]
    birth_date: Mapped[datetime | None]

    book: [list['Book']] = relationship(back_populates="author")

    @classmethod
    async def get_by_args(cls, session, **kwargs):
        query = select(cls).filter_by(**kwargs)
        return await session.scalars(query).one_or_none()

    @classmethod
    async def get_all(cls, session, params):
        limit = params.page_size
        offset = params.page_number
        query = select(cls)
        if limit:
            query = query.limit()
        if offset:
            query = query.offset()
        return await session.scalar(query).all()


class Book(BaseWithId):
    __tablename__ = 'book'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[uuid] = mapped_column(ForeignKey("author.id", ondelete="CASCADE"))
    quantity: Mapped[int]

    author: Mapped['Author'] = relationship(back_populates="book")
    borrow: Mapped["Borrow"] = relationship(back_populates="book")

    @classmethod
    async def get_by_args(cls, session, **kwargs):
        query = select(cls).filter_by(**kwargs)
        return await session.scalars(query).one_or_none()

    @classmethod
    async def get_all(cls, session, limit, offset):
        query = select(cls)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return session.scalars(query).all()


class Borrow(BaseWithId):
    __tablename__ = "borrow"

    book_id: Mapped[uuid] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"))
    client_name: Mapped[str]
    borrow_dt: Mapped[datetime]
    return_dt: Mapped[datetime]

    book: Mapped["Book"] = relationship(back_populates="borrow")
