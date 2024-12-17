from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from src.core.config import settings
engine = create_async_engine(settings.database_url, echo=settings.db_echo, future=True)
