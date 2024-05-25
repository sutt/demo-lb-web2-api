from fastapi import FastAPI, status
from starlette.responses import RedirectResponse

from .routers import api

app = FastAPI(title='Lightning Bounties Demo')

app.include_router(api.router, prefix='/api')


@app.get('/')
def index():
    return RedirectResponse('/docs', status_code=status.HTTP_308_PERMANENT_REDIRECT)
