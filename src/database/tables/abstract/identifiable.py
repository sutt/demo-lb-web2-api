from uuid import UUID

from sqlalchemy import UUID as SQLA_UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.base import SQLABase


class IdentifiableTable(SQLABase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(SQLA_UUID, primary_key=True, unique=True, nullable=False)
