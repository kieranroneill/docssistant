import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from api.conversations.routes import router as conversations_router
from api.documents.routes import router as documents_router
from api.healthcheck.routes import router as healthcheck_router
from api.versions.routes import router as versions_router
from libs.agents.clients import ChatAgent, EmbeddingsAgent
from libs.application.dtos import Application
from libs.application.utilities import get_version
from libs.chroma.clients import ChromaClient
from libs.logging.utilities import get_logger
from libs.postgres.clients import PostgresClient


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(description=os.environ["DESCRIPTION"], lifespan=_lifespan, title=f"{title} API")

    # add routers
    _app.include_router(conversations_router)
    _app.include_router(documents_router)
    _app.include_router(healthcheck_router)
    _app.include_router(versions_router)

    return _app


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    logger = get_logger()
    chroma = ChromaClient(logger=logger)
    embeddings_agent = EmbeddingsAgent(logger=logger)
    postgres = PostgresClient(logger=logger)
    root_path = Path(__file__).resolve().parents[1]

    try:
        await chroma.initialize()

        # attach dependencies
        _app.state.chat_agent = ChatAgent(logger=logger)
        _app.state.chroma = chroma
        _app.state.documents_path = root_path / ".documents"
        _app.state.embeddings_agent = embeddings_agent
        _app.state.logger = logger
        _app.state.postgres = postgres
        _app.state.application = Application(
            environment=os.environ["ENVIRONMENT"],
            description=os.environ["DESCRIPTION"],
            title=f"{os.environ["TITLE"]} API",
            version=get_version(root_path / "pyproject.toml"),
        )

        yield
    # cleanup
    finally:
        await postgres.dispose()


app = _create_app()
