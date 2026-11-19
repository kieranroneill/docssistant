from logging import Logger

import numpy as np
from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.api.types import Metadata, Where

from .dtos import DocumentMatch


class Repository:
    _logger: Logger

    def __init__(self, logger: Logger, collection: AsyncCollection):
        self._logger = logger
        self._collection = collection

    ##
    # public methods
    ##

    async def delete_chunks_by_ids(self, ids: list[str]) -> None:
        if ids:
            await self._collection.delete(ids=ids)

    async def get_chunk_ids_by_document_id(self, document_id: str) -> list[str]:
        where: Where = {"document_id": document_id}
        result = await self._collection.get(include=[], where=where)

        return result["ids"]

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
                chunk_index=int(str(metadata["chunk_index"])),
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

    async def upsert(
        self,
        ids: list[str],
        document_id: str,
        source: str,
        offset: int,
        chunks: list[str],
        embeddings: list[list[float]],
    ) -> None:
        metadatas: list[Metadata] = []

        for index in range(len(chunks)):
            metadata: Metadata = {"document_id": document_id, "source": source, "chunk_index": offset + index}
            metadatas.append(metadata)

        await self._collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=np.asarray(embeddings, dtype=np.float32),
            metadatas=metadatas,
        )
