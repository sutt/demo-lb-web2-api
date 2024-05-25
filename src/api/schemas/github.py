from pydantic import BaseModel


class GithubUserSchema(BaseModel):
    id: int
