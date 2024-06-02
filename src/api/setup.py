import uvicorn

from .app import app
from .dependencies import setup_dependencies
from .services.jwt import JWTService
from .services.lnbits import LNBitsService


async def run_api(
    host: str,
    port: int,
    jwt_access_token_secret: str,
    lnbits_base_url: str,
    lnbits_invoice_key: str,
    lnbits_callback_secret: str,
) -> None:
    setup_dependencies(app)
    JWTService.init("HS256", jwt_access_token_secret)
    LNBitsService.init(lnbits_base_url, lnbits_invoice_key, lnbits_callback_secret)

    uvicorn_config = uvicorn.Config(app, host=host, port=port)
    uvicorn_server = uvicorn.Server(uvicorn_config)
    await uvicorn_server.serve()
