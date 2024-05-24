import asyncio

import api

import config


async def run_app() -> None:
    await api.run_api(config.HOST, config.PORT)


if __name__ == '__main__':
    asyncio.run(run_app())
