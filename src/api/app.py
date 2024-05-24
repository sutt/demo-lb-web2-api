from fastapi import FastAPI, status
from starlette.responses import RedirectResponse

app = FastAPI(title='Lightning Bounties Demo')


@app.get('/')
def index():
    return RedirectResponse('/docs', status_code=status.HTTP_308_PERMANENT_REDIRECT)
