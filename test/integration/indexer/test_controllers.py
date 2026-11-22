from logging import Logger
from pathlib import Path
from test.mocks.agents.clients import MockEmbeddingsAgent

import pytest

from indexer.controllers import IndexerController
from libs.chroma.clients import ChromaClient
from libs.documents.repositories import DocumentVersionRepository
from libs.postgres.clients import PostgresClient


@pytest.fixture
def controller(
    chroma_client: ChromaClient,
    embeddings_agent: MockEmbeddingsAgent,
    logger: Logger,
    postgres_client: PostgresClient,
) -> IndexerController:
    return IndexerController(
        chroma_client=chroma_client,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_client=postgres_client,
    )


class TestIndex:
    async def test_should_index_the_documents_path(
        self,
        controller: IndexerController,
        documents_path: Path,
        logger: Logger,
        postgres_client: PostgresClient,
    ) -> None:
        assert await controller.index(documents_path=documents_path / "text") == 1

        # the controller manages its own session, so read the result back on a fresh one
        async with postgres_client.create_session() as session:
            repository = DocumentVersionRepository(logger=logger, postgres_session=session)
            active_versions = await repository.get_all_active()

        assert [version.source for version in active_versions] == ["handbook.md"]

    async def test_should_not_raise_if_the_documents_path_does_not_exist(
        self,
        controller: IndexerController,
        documents_path: Path,
        mocker,
    ) -> None:
        # the indexer runs in a watch loop, so a failed pass must be logged rather than raised
        exception = mocker.spy(controller._logger, "exception")

        assert await controller.index(documents_path=documents_path / "does-not-exist") == 0

        exception.assert_called_once_with("document indexing failed")
