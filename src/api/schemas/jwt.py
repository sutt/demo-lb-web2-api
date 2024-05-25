import datetime
from uuid import UUID

from pydantic import BaseModel, field_validator


class GetAccessTokenDTO(BaseModel):
    user_id: str
    github_token: str

    @field_validator('user_id', mode='before')
    @classmethod
    def transform_id_to_str(cls, value) -> str:
        return str(value)


class AccessTokenPayloadSchema(BaseModel):
    user_id: str
    github_token: str
    exp: datetime.datetime


class TokenResponse(BaseModel):
    access_token: str
