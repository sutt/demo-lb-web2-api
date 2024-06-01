from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from domain.common.schemas import IdentifiableSchema, TimestampedSchema, UpdateRequestSchema


class CreateRewardDTO(BaseModel):
    rewarder_id: UUID
    reward_amount: int = Field(..., gt=0)

    issue_github_id: int
    repo_full_name: str
    issue_github_number: int

    html_url: str


class RewardSchema(IdentifiableSchema, TimestampedSchema):
    rewarder_id: UUID
    reward_amount: int

    issue_github_id: int
    repo_full_name: str
    issue_github_number: int

    html_url: str

    winner_id: UUID | None = Field(None)
    claimed_at: datetime | None = Field(None)


class UpdateRewardDTO(UpdateRequestSchema):
    winner_id: UUID | None = Field(None)
    claimed_at: datetime | None = Field(None)


class RewardResultSchema(BaseModel):
    total_points: int = Field(0, ge=0)
    rewarded_for: list[RewardSchema]
    already_claimed: list[RewardSchema]
