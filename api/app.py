import os

from fastapi import FastAPI

from api import healthcheck


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(title=f"{title} API")

    _app.include_router(healthcheck.routes.router)

    return _app


app = _create_app()
