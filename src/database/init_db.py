__all__ = ["init_db"]

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import async_sessionmaker

from . import tables
from .base import SQLABase
from .engine import create_async_engine, init_tables
from .session import SessionScope


async def init_db(url: URL | str):
    async_engine = create_async_engine(url)
    SessionScope.init_sessionmaker(async_sessionmaker(async_engine, expire_on_commit=False))
    await init_tables(async_engine, SQLABase.metadata)
