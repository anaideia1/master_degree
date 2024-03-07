from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from backend.config import config


# create session factory to generate new database sessions
async_session_maker = async_sessionmaker(
    bind=create_async_engine(config.database.dsn),
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
