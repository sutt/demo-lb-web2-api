from fastapi import APIRouter

from . import user, auth, rewards

router = APIRouter()


router.include_router(auth.router, prefix='/auth')
router.include_router(user.router, prefix='/users')
router.include_router(rewards.router, prefix='/rewards')
