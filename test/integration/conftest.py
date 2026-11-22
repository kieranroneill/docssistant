from logging import Logger
from pathlib import Path
from test.mocks.agents.clients import MockChatAgent, MockEmbeddingsAgent
from typing import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from chromadb.api.models.AsyncCollection import AsyncCollection
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from libs.chroma.clients import ChromaClient
from libs.logging.utilities import get_logger
from libs.postgres.clients import PostgresClient


def pytest_sessionstart() -> None:
    load_dotenv(".env.test")


@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


###
# dependencies
##


@pytest.fixture
def logger() -> Logger:
    return get_logger()


@pytest.fixture
def chat_agent(logger: Logger) -> MockChatAgent:
    return MockChatAgent(logger=logger)


@pytest.fixture
def embeddings_agent(logger: Logger) -> MockEmbeddingsAgent:
    return MockEmbeddingsAgent(logger=logger)


@pytest.fixture
async def postgres_client(logger: Logger) -> AsyncIterator[PostgresClient]:
    client = PostgresClient(logger=logger)

    try:
        yield client
    finally:
        await client.dispose()


@pytest.fixture
async def chroma_client(logger: Logger) -> AsyncIterator[ChromaClient]:
    client = ChromaClient(logger=logger)

    await client.initialize()

    yield client


@pytest.fixture
async def chroma_collection(chroma_client: ChromaClient) -> AsyncCollection:
    return await chroma_client.collection()


@pytest.fixture
async def postgres_session(postgres_client: PostgresClient) -> AsyncIterator[AsyncSession]:
    async with postgres_client.create_session() as session:
        yield session


###
# documents
##


@pytest.fixture
def documents_path() -> Path:
    """
    The static documents in 'test/fixtures/documents', indexed in place.

    Note: The indexer walks a directory recursively and indexes everything it finds, so each scenario has its own
    subdirectory; pointing a test at the root would make its results depend on every other scenario's documents.
    """
    return Path(__file__).resolve().parents[1] / "fixtures" / "documents"


@pytest.fixture
def temp_documents_path(tmp_path: Path) -> Path:
    """
    An empty, writable documents directory.

    Note: For tests that change or delete a document; those cannot use the static fixtures, as they would leave the
    working tree dirty and would not survive a second run.
    """
    path = tmp_path / "__documents__"

    path.mkdir()

    return path
