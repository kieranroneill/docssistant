import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import healthcheck
from api.platform.agents.clients import AgentClient


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(title=f"{title} API")

    _app.include_router(healthcheck.routes.router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    _app.state.agent = AgentClient()

    yield
    # cleanup


app = _create_app()
