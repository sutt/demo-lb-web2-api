from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from database.tables.abstract import IdentifiableTable, TimestampedTable


class UserModel(IdentifiableTable, TimestampedTable):
    __tablename__ = 'users'

    github_id: Mapped[int] = mapped_column(BIGINT, nullable=False, unique=True)

    points: Mapped[int] = mapped_column(BIGINT, nullable=False, default=0)
