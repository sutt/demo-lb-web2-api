from fastapi import FastAPI

from .user import di_user
from .reward import di_reward


def setup_dependencies(app: FastAPI) -> None:
    di_user(app)
    di_reward(app)
