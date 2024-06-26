import asyncio

import api

import config
from database import init_db


async def run_app() -> None:
    await init_db(config.DB_URL)
    await api.run_api(config.HOST, config.PORT, config.JWT_ACCESS_TOKEN_SECRET)


if __name__ == '__main__':
    asyncio.run(run_app())
