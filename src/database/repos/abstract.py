import abc

from sqlalchemy.ext.asyncio import AsyncSession


class SQLAAbstractRepo(abc.ABC):
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session
