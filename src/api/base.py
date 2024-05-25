import uvicorn

from .app import app
from .dependencies import setup_dependencies


async def run_api(host: str, port: int) -> None:
    setup_dependencies(app)

    uvicorn_config = uvicorn.Config(app, host=host, port=port)
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()
