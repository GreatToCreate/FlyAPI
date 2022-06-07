from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta

from config import config

# ToDo Need a better way to deal with environmental variables here- they're all over the place
# Database url either defined as an environment variable or using a local sqlite instance

database_url: str = config.DB_URL

# Metadata object that is used to define certain sqlalchemy tables as well as used for Alembic migrations
Base: DeclarativeMeta = declarative_base()

# ToDo this is an area where the environmental variable problem is also present
# future parameter indicates that querying will use SQLAlchemy 2.0 style
engine = create_async_engine(database_url, future=True, echo=config.DEV_MODE)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Async session generator used for dependency injection on routes required database operations
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# ToDo Way to resolve circular import issue without delayed import?
# Intentionally delayed import to avoid circular import issues
from database.models.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
