from fastapi import FastAPI

from domain.rewards.service import RewardServiceABC
from impl.rewards.service import RewardService


def get_service() -> RewardServiceABC:
    return RewardService()


def di_reward(app: FastAPI) -> None:
    app.dependency_overrides[RewardServiceABC] = get_service
