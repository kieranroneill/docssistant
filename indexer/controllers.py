from logging import Logger
from pathlib import Path

from indexer.services import IndexerService
from libs.agents.clients import AbstractEmbeddingsAgent
from libs.chroma.clients import ChromaClient
from libs.defaults.controllers import BaseController
from libs.postgres.clients import PostgresClient


class IndexerController(BaseController):
    _chroma_client: ChromaClient
    _embeddings_agent: AbstractEmbeddingsAgent
    _postgres_client: PostgresClient

    def __init__(
        self,
        chroma_client: ChromaClient,
        embeddings_agent: AbstractEmbeddingsAgent,
        logger: Logger,
        postgres_client: PostgresClient,
    ):
        super().__init__(logger=logger)

        self._postgres_client = postgres_client
        self._embeddings_agent = embeddings_agent
        self._chroma_client = chroma_client

    async def index(self, documents_path: Path) -> int:
        """
        Creates a new Postgres session and runs the indexer.

        Args:
            documents_path: Path to the directory containing the documents to index.

        Returns:
            The number of documents indexed.
        """
        indexed = 0

        try:
            async with self._postgres_client.create_session() as session:
                indexer = IndexerService(
                    chroma_collection=await self._chroma_client.collection(),
                    embeddings_agent=self._embeddings_agent,
                    logger=self._logger,
                    postgres_session=session,
                )

                indexed = await indexer.index(documents_path=documents_path)

            self._logger.info(f"document indexing completed ({indexed} documents indexed)")
        except Exception:
            self._logger.exception("document indexing failed")

        return indexed
