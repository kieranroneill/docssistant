import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.conversations.routes import router as conversations_router
from api.healthcheck.routes import router as healthcheck_router
from libs.agents.clients import ChatAgent, EmbeddingsAgent
from libs.chroma.clients import ChromaClient
from libs.logging.utilities import get_logger
from libs.postgres.clients import PostgresClient


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(lifespan=_lifespan, title=f"{title} API")

    # add routers
    _app.include_router(conversations_router)
    _app.include_router(healthcheck_router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger = get_logger()
    chroma = ChromaClient(logger=logger)
    embeddings_agent = EmbeddingsAgent(logger=logger)
    postgres = PostgresClient(logger=logger)

    try:
        await chroma.initialize()

        # attach dependencies
        _app.state.chat_agent = ChatAgent(logger=logger)
        _app.state.chroma = chroma
        _app.state.embeddings_agent = embeddings_agent
        _app.state.logger = logger
        _app.state.postgres = postgres

        yield
    # cleanup
    finally:
        await postgres.dispose()


app = _create_app()
