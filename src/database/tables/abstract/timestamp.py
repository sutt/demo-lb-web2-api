from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.base import SQLABase


class CreatedAtTimestamp(SQLABase):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now(), nullable=False)


class ModifiedAtTimestamp(SQLABase):
    __abstract__ = True

    modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=func.now(), onupdate=func.now())


class TimestampedTable(CreatedAtTimestamp, ModifiedAtTimestamp):
    __abstract__ = True
