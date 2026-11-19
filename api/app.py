import asyncio
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from logging import Logger
from pathlib import Path

from fastapi import FastAPI

from api.conversations.routes import router as conversations_router
from api.documents.services import DocumentIndexerService
from api.healthcheck.routes import router as healthcheck_router
from api.platform.agents.clients import ChatAgent, EmbeddingsAgent
from api.platform.chroma.clients import ChromaClient
from api.platform.logging.utilities import get_logger
from api.platform.postgres.clients import PostgresClient


def _create_app() -> FastAPI:
    title = os.environ["TITLE"]
    _app = FastAPI(lifespan=_lifespan, title=f"{title} API")

    # add routers
    _app.include_router(conversations_router)
    _app.include_router(healthcheck_router)

    return _app


async def _document_index_task(
    chroma: ChromaClient, documents_path: Path, embeddings_agent: EmbeddingsAgent, logger: Logger
) -> None:
    try:
        documents_service = DocumentIndexerService(
            chroma_collection=await chroma.collection(),
            embeddings_agent=embeddings_agent,
            logger=logger,
        )

        indexed = await documents_service.index(documents_path=documents_path)
    except asyncio.CancelledError:
        logger.info("document indexing cancelled")
    except Exception as e:
        logger.error(f"document indexing failed on documents in at'{documents_path}': {e}")
    else:
        logger.info(f"document indexing completed ({indexed} documents indexed)")


@asynccontextmanager
async def _lifespan(_app: FastAPI) -> AsyncIterator[None]:
    documents_path = Path(__file__).resolve().parent.parent / ".documents"
    indexing_task: asyncio.Task[None] | None = None
    logger = get_logger()
    chroma = ChromaClient(logger=logger)
    embeddings_agent = EmbeddingsAgent(logger=logger)
    postgres = PostgresClient(logger=logger)

    try:
        await chroma.initialize()

        # create a thread to index documents at `/.documents` in the background
        indexing_task = asyncio.create_task(
            _document_index_task(
                chroma=chroma,
                documents_path=documents_path,
                embeddings_agent=embeddings_agent,
                logger=logger,
            ),
            name="document-indexing-task",
        )

        # attach dependencies
        _app.state.chat_agent = ChatAgent(logger=logger)
        _app.state.chroma = chroma
        _app.state.embeddings_agent = embeddings_agent
        _app.state.logger = logger
        _app.state.postgres = postgres

        yield
    # cleanup
    finally:
        if indexing_task is not None:
            indexing_task.cancel()

            # await the indexing task to complete cancellation
            with suppress(asyncio.CancelledError):
                await indexing_task

        await postgres.dispose()


app = _create_app()
