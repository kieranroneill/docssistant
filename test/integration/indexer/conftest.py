from collections.abc import AsyncIterator

import pytest
from sqlalchemy import delete

from libs.chroma.clients import ChromaClient
from libs.documents.models import DocumentVersionModel
from libs.postgres.clients import PostgresClient


@pytest.fixture(autouse=True)
async def clear_document_chunks(chroma_client: ChromaClient) -> AsyncIterator[None]:
    """
    Empty the Chroma collection on each test.
    """
    collection = await chroma_client.collection()
    result = await collection.get(include=[])

    if result["ids"]:
        await collection.delete(ids=result["ids"])

    yield


@pytest.fixture(autouse=True)
async def clear_document_versions(postgres_client: PostgresClient) -> AsyncIterator[None]:
    """
    Empty document versions on each test.
    """
    async with postgres_client.create_session() as session:
        await session.execute(delete(DocumentVersionModel))
        await session.commit()

    yield
