import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.conversations.routes import router as conversations_router
from api.healthcheck.routes import router as healthcheck_router
from api.platform.agents.clients import AgentClient


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(lifespan=_lifespan, title=f"{title} API")

    # add routers
    _app.include_router(conversations_router)
    _app.include_router(healthcheck_router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    _app.state.agent = AgentClient()

    yield
    # cleanup


app = _create_app()
