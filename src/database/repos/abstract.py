import abc

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAAbstractRepo(abc.ABC):
    _session: AsyncSession
