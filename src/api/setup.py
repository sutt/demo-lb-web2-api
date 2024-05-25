import uvicorn

from .app import app
from .dependencies import setup_dependencies
from .services.jwt import JWTService


async def run_api(
    host: str,
    port: int,
    jwt_access_token_secret: str,
) -> None:
    setup_dependencies(app)
    JWTService.init("HS256", jwt_access_token_secret)

    uvicorn_config = uvicorn.Config(app, host=host, port=port)
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()
