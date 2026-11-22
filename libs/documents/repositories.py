from logging import Logger
from uuid import UUID

import numpy as np
from chromadb.api.models.AsyncCollection import AsyncCollection
from chromadb.api.types import Metadata, Where
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from libs.defaults.repositories import BaseRepository

from .constants import MAX_MATCH_DISTANCE
from .dtos import DocumentChunk, DocumentMatch, DocumentVersion
from .models import DocumentVersionModel


class DocumentChunkRepository:
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
        active_versions: list[DocumentVersion],
        limit: int = 5,
        max_distance: float = MAX_MATCH_DISTANCE,
    ) -> list[DocumentMatch]:
        """
        Performs a constrained vector similarity lookup for document chunks and applies a distance threshold to keep
        only relevant matches. The lookup is skipped when no constraints are available, preventing broad, unfiltered
        retrieval.

        Note: Chroma's collection uses cosine distance, so 0.0 is an exact match and 2.0 is the opposite. A top-k search
        always returns its k nearest chunks, even when every one of them is unrelated, so without an upper bound an
        unanswerable question still reaches the chat agent with plausible-looking context. This value is deliberately
        permissive: it is meant to discard the clearly irrelevant, not to make fine-grained relevance judgements.

        Args:
            embeddings: Embedding vector used as the query for nearest-neighbour matching.
            active_versions: Document versions that constrain the search scope.
            limit: Maximum number of nearest candidates to request before relevance filtering.
            max_distance: Maximum accepted distance for a candidate to be considered relevant.

        Returns:
            Relevant document matches whose distances do not exceed the configured maximum distance.

        Raises:
            ValueError: If returned result groups cannot be combined because their lengths differ, or if numeric
            metadata cannot be converted.
            KeyError: If required metadata is missing from a returned result.
        """
        # never fall back to an unfiltered query
        if not active_versions:
            return []

        filters: list[Where] = []

        for active_version in active_versions:
            document_filter: Where = {"document_id": str(active_version.document_id)}
            version_filter: Where = {"version": active_version.version}
            filters.append({"$and": [document_filter, version_filter]})

        where: Where = filters[0]

        if len(filters) > 1:
            where = {"$or": filters}
        result = await self._collection.query(
            include=["documents", "metadatas", "distances"],
            n_results=limit,
            query_embeddings=np.asarray([embeddings], dtype=np.float32),
            where=where,
        )
        documents = result["documents"]
        metadatas = result["metadatas"]
        distances = result["distances"]

        if documents is None or metadatas is None or distances is None:
            return []

        matches = [
            DocumentMatch(
                chunk_index=int(str(metadata["chunk_index"])),
                content=content,
                document_id=str(metadata["document_id"]),
                distance=distance,
                source=str(metadata.get("source", "")),
                page_number=(int(str(metadata["page_number"])) if metadata.get("page_number") is not None else None),
            )
            for content, metadata, distance in zip(
                documents[0],
                metadatas[0],
                distances[0],
                strict=True,
            )
        ]

        # drop anything the query is not actually close to
        # a nearest-neighbour search has no  concept of "no answer" - it returns its k closest chunks regardless - so
        # this is what lets the caller distinguish a weak match from a real one and abstain.
        relevant = [match for match in matches if match.distance <= max_distance]

        for match in matches:
            self._logger.debug(
                f"match '{match.source}' chunk {match.chunk_index} has a distance of {match.distance:.4f} "
                f"({'kept' if match.distance <= max_distance else 'discarded'})"
            )

        if len(relevant) < len(matches):
            self._logger.debug(
                f"discarded {len(matches) - len(relevant)} of {len(matches)} matches "
                f"above the maximum distance of {max_distance}"
            )

        return relevant

    async def upsert(
        self,
        chunks: list[DocumentChunk],
        document_id: str,
        embeddings: list[list[float]],
        ids: list[str],
        offset: int,
        source: str,
        version: str,
    ) -> None:
        metadatas: list[Metadata] = []

        for index, chunk in enumerate(chunks):
            metadata: dict[str, str | int] = {
                "chunk_index": offset + index,
                "document_id": document_id,
                "version": version,
                "source": source,
            }

            if chunk.page_number is not None:
                metadata["page_number"] = chunk.page_number

            metadatas.append(metadata)

        await self._collection.upsert(
            documents=[chunk.content for chunk in chunks],
            embeddings=np.asarray(embeddings, dtype=np.float32),
            ids=ids,
            metadatas=metadatas,
        )


class DocumentVersionRepository(BaseRepository[DocumentVersionModel, DocumentVersion]):
    ##
    # private methods
    ##

    @property
    def _model_type(self) -> type[DocumentVersionModel]:
        return DocumentVersionModel

    def _to_model(self, dto: DocumentVersion) -> DocumentVersionModel:
        return dto.to_model()

    async def _to_dto(self, model: DocumentVersionModel) -> DocumentVersion:
        return DocumentVersion.from_model(model)

    ##
    # public methods
    ##

    async def deactivate(self, document_id: UUID) -> None:
        """
        Simply deactivates all document version by the given document ID.

        Args:
            document_id: The document ID to deactivate.
        """
        try:
            await self._postgres_session.execute(
                update(DocumentVersionModel)
                .where(
                    DocumentVersionModel.document_id == document_id,
                    DocumentVersionModel.active.is_(True),
                )
                .values(active=False)
            )
            await self._postgres_session.commit()
        except BaseException:
            await self._postgres_session.rollback()
            raise

    async def get_by_document_id(self, document_id: UUID) -> DocumentVersion | None:
        """
        Returns document version by its document ID.

        Args:
            document_id: The document ID to retrieve.

        Returns:
            DocumentVersion | None: The document or None if no document exists.
        """
        statement = select(DocumentVersionModel).where(DocumentVersionModel.document_id == document_id)
        result = await self._postgres_session.execute(statement)
        model = result.scalar_one_or_none()

        return DocumentVersion.from_model(model) if model else None

    async def get_all_active(self) -> list[DocumentVersion]:
        """
        Returns all active document versions.

        Returns:
            list[DocumentVersion]: A list of active document versions.
        """
        statement = select(DocumentVersionModel).where(DocumentVersionModel.active.is_(True))
        result = await self._postgres_session.execute(statement)
        models = result.scalars().all()

        return [DocumentVersion.from_model(model) for model in models]

    async def publish(self, document_id: UUID, source: str, version: str) -> None:
        """
        Publishes a new version atomically.

        1. Adds the new version, but leaves it inactive.
        2. Deactivates the previous active version(s).
        3. Activates the new version.

        Note: If any of the steps fail, the transaction will be rolled back.

        Args:
            document_id (UUID): The ID of the document to publish a new version for.
            source (str): The source of the new version.
            version (str): The version of the new version.

        Raises:
            Exception: If any of the steps fail.
        """
        try:
            # first insert the new version and set to inactive
            await self._postgres_session.execute(
                insert(DocumentVersionModel)
                .values(
                    active=False,
                    document_id=document_id,
                    source=source,
                    version=version,
                )
                .on_conflict_do_nothing(constraint="uq_document_versions_document_version")
            )
            # deactivate the previous active version(s)
            await self._postgres_session.execute(
                update(DocumentVersionModel)
                .where(DocumentVersionModel.document_id == document_id, DocumentVersionModel.active.is_(True))
                .values(active=False)
            )
            # activate the new version
            await self._postgres_session.execute(
                update(DocumentVersionModel)
                .where(
                    DocumentVersionModel.document_id == document_id,
                    DocumentVersionModel.version == version,
                )
                .values(active=True, source=source)
            )
            await self._postgres_session.commit()
        except BaseException:
            await self._postgres_session.rollback()
            raise
