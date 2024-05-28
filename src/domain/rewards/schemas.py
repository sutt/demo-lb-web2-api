from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.common.schemas import IdentifiableSchema, TimestampedSchema, UpdateRequestSchema


class CreateRewardDTO(BaseModel):
    rewarder_id: UUID
    reward_amount: int = Field(..., gt=0)

    issue_github_id: int
    issue_github_owner: str
    issue_github_repo: str
    issue_github_number: int

    html_url: str


class RewardSchema(IdentifiableSchema, TimestampedSchema):
    rewarder_id: UUID
    reward_amount: int

    issue_github_id: int
    issue_github_owner: str
    issue_github_repo: str
    issue_github_number: int

    html_url: str

    winner_id: UUID | None = Field(None)
    claimed_at: datetime | None = Field(None)


class UpdateRewardDTO(UpdateRequestSchema):
    winner_id: UUID | None = Field(None)
    claimed_at: datetime | None = Field(None)
