from logging import Logger

from chromadb.api.models.AsyncCollection import AsyncCollection

from .dtos import DocumentMatch


class Repository:
    _logger: Logger

    def __init__(self, logger: Logger, collection: AsyncCollection):
        self._logger = logger
        self._collection = collection

    ##
    # public methods
    ##

    async def search(
        self,
        embeddings: list[float],
        limit: int = 5,
    ) -> list[DocumentMatch]:
        result = await self._collection.query(
            include=["documents", "metadatas", "distances"],
            n_results=limit,
            query_embeddings=[embeddings],
        )
        documents = result["documents"]
        metadatas = result["metadatas"]
        distances = result["distances"]

        if documents is None or metadatas is None or distances is None:
            return []

        return [
            DocumentMatch(
                document_id=str(metadata["document_id"]),
                chunk_index=int(metadata["chunk_index"]),
                content=content,
                distance=distance,
            )
            for content, metadata, distance in zip(
                documents[0],
                metadatas[0],
                distances[0],
                strict=True,
            )
        ]
