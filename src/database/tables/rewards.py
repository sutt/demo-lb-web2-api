from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from database.tables import IdentifiableTable, TimestampedTable


class RewardModel(IdentifiableTable, TimestampedTable):
    __tablename__ = 'rewards'

    rewarder_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    reward_amount: Mapped[int] = mapped_column(BigInteger, nullable=False)

    # TODO: Move issues to another table and link to here by foreign key
    issue_github_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    issue_github_owner: Mapped[str] = mapped_column(nullable=False)
    issue_github_repo: Mapped[str] = mapped_column(nullable=False)
    issue_github_number: Mapped[int] = mapped_column(BigInteger, nullable=False)

    html_url: Mapped[str | None] = mapped_column(nullable=True)

    winner_id: Mapped[UUID | None] = mapped_column(ForeignKey('users.id'), nullable=True)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=False), nullable=True)
