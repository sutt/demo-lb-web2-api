from pydantic import BaseModel, Field

from domain.common.schemas import IdentifiableSchema, TimestampedSchema


class UserCreateDTO(BaseModel):
    github_id: int
    points: int = Field(0, ge=0)


class UserSchema(IdentifiableSchema, TimestampedSchema):
    github_id: int
    points: int
