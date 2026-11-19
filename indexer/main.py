import asyncio
import logging
import os
from pathlib import Path

from watchfiles import awatch

from indexer.controllers import IndexerController
from libs.agents.clients import EmbeddingsAgent
from libs.chroma.clients import ChromaClient
from libs.documents.constants import SUPPORTED_DOCUMENT_EXTENSIONS
from libs.logging.utilities import get_logger
from libs.postgres.clients import PostgresClient


async def main() -> None:
    logger = get_logger()
    documents_path = Path(__file__).resolve().parent.parent / ".documents"
    chroma_client = ChromaClient(logger=logger)
    postgres_client = PostgresClient(logger=logger)

    try:
        await chroma_client.initialize()

        indexer_controller = IndexerController(
            chroma_client=chroma_client,
            embeddings_agent=EmbeddingsAgent(logger=logger),
            logger=logger,
            postgres_client=postgres_client,
        )

        # perform an initial pass
        await indexer_controller.index(documents_path=documents_path)

        async for changes in awatch(
            documents_path,
            debounce=2000,
            recursive=True,
            force_polling=True,
            step=500,
            yield_on_timeout=True,
            rust_timeout=60_000,
        ):
            supported_change = any(Path(path).suffix.lower() in SUPPORTED_DOCUMENT_EXTENSIONS for _, path in changes)

            # if there are any file changes, run the indexer
            if not changes or supported_change:
                await indexer_controller.index(documents_path=documents_path)

    finally:
        await postgres_client.dispose()


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=os.getenv("LOG_LEVEL", "INFO").upper())

    asyncio.run(main())
