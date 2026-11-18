import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.conversations.routes import router as conversations_router
from api.healthcheck.routes import router as healthcheck_router
from api.platform.agents.clients import AgentClient
from api.platform.logging.utilities import get_logger
from api.platform.postgres.utilities import url as postgres_url


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(lifespan=_lifespan, title=f"{title} API")

    # add routers
    _app.include_router(conversations_router)
    _app.include_router(healthcheck_router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    postgres_engine = create_async_engine(postgres_url(), pool_pre_ping=True)
    logger = get_logger()

    # attach dependencies
    _app.state.agent = AgentClient(logger=logger)
    _app.state.logger = logger
    _app.state.postgres_session_factory = async_sessionmaker(
        bind=postgres_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    try:
        yield
    # cleanup
    finally:
        await postgres_engine.dispose()


app = _create_app()
