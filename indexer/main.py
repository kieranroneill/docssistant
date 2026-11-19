import asyncio
import logging
import os
from pathlib import Path

from indexer.services import IndexerService
from libs.agents.clients import EmbeddingsAgent
from libs.chroma.clients import ChromaClient
from libs.logging.utilities import get_logger
from libs.postgres.clients import PostgresClient


async def main() -> None:
    logger = get_logger()
    documents_path = Path(__file__).resolve().parent.parent / ".documents"
    chroma = ChromaClient(logger=logger)
    embeddings_agent = EmbeddingsAgent(logger=logger)
    postgres = PostgresClient(logger=logger)

    try:
        await chroma.initialize()

        async with postgres.create_session() as session:
            indexer = IndexerService(
                chroma_collection=await chroma.collection(),
                embeddings_agent=embeddings_agent,
                logger=logger,
                postgres_session=session,
            )

            indexed = await indexer.index(documents_path=documents_path)

        logger.info(f"document indexing completed ({indexed} documents indexed)")
    finally:
        await postgres.dispose()


if __name__ == "__main__":
    logging.basicConfig(format="%(levelname)s: %(message)s", level=os.getenv("LOG_LEVEL", "INFO").upper())

    asyncio.run(main())
