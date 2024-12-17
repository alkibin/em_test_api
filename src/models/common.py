import uuid
from datetime import datetime

from sqlalchemy import select, func, ForeignKey, CheckConstraint, UniqueConstraint, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, selectinload, mapped_column, relationship, DeclarativeBase

from src.db import crud


class Base(DeclarativeBase):
    pass

    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"{self.__class__.__name__}, {', '.join(cols)}"


class BaseWithId(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class Author(BaseWithId):
    __tablename__ = "author"
    __table_args__ = (UniqueConstraint("name", "surname", "birthdate", name='name_surmane_birth_const'), )

    name: Mapped[str]
    surname: Mapped[str]
    birthdate: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    book: Mapped[list['Book']] = relationship(back_populates="author", cascade="all, delete")

    @classmethod
    async def get_by_args(cls, session, **kwargs):
        query = select(cls).filter_by(**kwargs)
        return (await session.scalars(query)).one_or_none()

    @classmethod
    async def get_all(cls, session, limit, offset):
        query = crud._get_all(cls, limit, offset)
        return (await session.scalars(query)).all()


class Book(BaseWithId):
    __tablename__ = 'book'
    __table_args__ = (
        CheckConstraint('quantity >= 0', name='check_quantity_positive'),
    )

    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[uuid] = mapped_column(ForeignKey("author.id"))
    quantity: Mapped[int]

    author: Mapped['Author'] = relationship(back_populates="book")
    borrow: Mapped[list["Borrow"]] = relationship(back_populates="book", cascade="all, delete")

    @classmethod
    async def get_by_args(cls, session, **kwargs):
        query = select(cls).filter_by(**kwargs)
        return (await session.scalars(query)).one_or_none()

    @classmethod
    async def get_all(cls, session, limit, offset):
        query = crud._get_all(cls, limit, offset)
        return (await session.scalars(query)).all()

    @classmethod
    async def get_with_author(cls, session, **kwargs):
        query = select(cls).options(selectinload(cls.author)).filter_by(**kwargs)
        return (await session.scalars(query)).one_or_none()


class Borrow(BaseWithId):
    __tablename__ = "borrow"

    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("book.id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    borrow_dt: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    return_dt: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))

    book: Mapped["Book"] = relationship(back_populates="borrow")
    user: Mapped["User"] = relationship(back_populates="borrow")

    @classmethod
    async def get_all(cls, session, limit, offset, start_date, end_date):
        query = crud._get_all(cls, limit, offset).filter(
            cls.borrow_dt >= start_date,
            cls.borrow_dt <= end_date
        )
        return (await session.scalars(query)).all()


class User(BaseWithId):
    __tablename__ = "user"

    name: Mapped[str]
    surname: Mapped[str]

    borrow: Mapped[list["Borrow"]] = relationship(back_populates="user")

