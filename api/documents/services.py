import json
from asyncio import to_thread
from hashlib import sha256
from logging import Logger
from pathlib import Path
from uuid import NAMESPACE_URL, uuid4, uuid5

from chromadb.api.models.AsyncCollection import AsyncCollection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdfplumber import open as open_pdf
from sqlalchemy.ext.asyncio import AsyncSession

from api.platform.agents.clients import AbstractEmbeddingsAgent
from api.platform.defaults.services import BaseService

from .dtos import DocumentChunk, DocumentVersion
from .errors import DocumentPathDoesNotExistError
from .repositories import DocumentChunkRepository, DocumentVersionRepository


class DocumentIndexerService(BaseService):
    _chunk_overlap: int
    _chunk_size: int
    _document_chunk_repository: DocumentChunkRepository
    _document_version_repository: DocumentVersionRepository
    _embeddings_agent: AbstractEmbeddingsAgent
    _splitter: RecursiveCharacterTextSplitter

    def __init__(
        self,
        chroma_collection: AsyncCollection,
        embeddings_agent: AbstractEmbeddingsAgent,
        logger: Logger,
        postgres_session: AsyncSession,
    ):
        super().__init__(logger=logger)

        # TODO: make the chunks configurable
        self._chunk_overlap = 200
        self._chunk_size = 1500
        self._document_chunk_repository = DocumentChunkRepository(collection=chroma_collection, logger=logger)
        self._document_version_repository = DocumentVersionRepository(logger=logger, postgres_session=postgres_session)
        self._embeddings_agent = embeddings_agent
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=self._chunk_size, chunk_overlap=self._chunk_overlap)

    ###
    # private static methods
    ###

    def _extract_pdf(self, path: Path) -> list[DocumentChunk]:
        chunks: list[DocumentChunk] = []

        with open_pdf(path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                content = page.extract_text() or ""

                chunks.extend(
                    DocumentChunk(
                        content=text,
                        page_number=page_number,
                    )
                    for text in self._splitter.split_text(content)
                )

        return chunks

    def _extract_text(self, path: Path) -> list[DocumentChunk]:
        content = path.read_text(encoding="utf-8")

        return [DocumentChunk(content=text) for text in self._splitter.split_text(content)]

    def _fingerprint(self, chunks: list[DocumentChunk]) -> str:
        return sha256(
            (f"{self._embeddings_agent.model()}:" f"{self._chunk_size}:{self._chunk_overlap}:v1\0" f"{json.dumps(
                    [chunk.model_dump() for chunk in chunks],
                    ensure_ascii=False,
                    sort_keys=True,
                )}").encode("utf-8")
        ).hexdigest()

    ###
    # private methods
    ###

    async def _index_file(self, path: Path, documents_path: Path) -> bool:
        chunks: list[DocumentChunk] = []
        source = path.relative_to(documents_path).as_posix()

        if path.suffix.lower() == ".md" or path.suffix.lower() == ".txt":
            chunks = await to_thread(self._extract_text, path)

        if path.suffix.lower() == ".pdf":
            chunks = await to_thread(self._extract_pdf, path)

        if len(chunks) <= 0:
            self._logger.warning(
                "document '%s' contains no extractable text; keeping its previous active version", source
            )

            return False

        document_id = uuid5(NAMESPACE_URL, f"docssistant:document_store:{source}")
        fingerprint = await to_thread(self._fingerprint, chunks)
        ids = [f"{document_id}:{fingerprint}:{index}" for index in range(len(chunks))]
        existing_ids = set(
            await self._document_chunk_repository.get_chunk_ids_by_document_id(document_id=str(document_id))
        )
        active_versions = await self._document_version_repository.get_all_active()

        if set(ids).issubset(existing_ids) and any(
            active.document_id == document_id and active.version == fingerprint for active in active_versions
        ):
            self._logger.info(f"document '{source}' is unchanged")

            return False

        self._logger.info(f"indexing document '{source}' ({len(chunks)} chunks)")

        for offset in range(0, len(chunks), 32):
            batch = chunks[offset : offset + 32]
            embeddings = await self._embeddings_agent.documents(
                texts=[chunk.content for chunk in batch],
            )

            if len(embeddings) != len(batch):
                self._logger.warning(
                    f"embedding count({len(embeddings)}) does not match chunk count ({len(batch)}) for '{source}'"
                )

                return False

            await self._document_chunk_repository.upsert(
                chunks=batch,
                document_id=str(document_id),
                embeddings=embeddings,
                ids=ids[offset : offset + 32],
                offset=offset,
                source=source,
                version=fingerprint,
            )

        # publish the new version
        await self._document_version_repository.publish(
            document_id=document_id,
            source=source,
            version=fingerprint,
        )

        return True

    ###
    # public methods
    ###

    async def index(self, documents_path: Path) -> int:
        if not documents_path.is_dir():
            raise DocumentPathDoesNotExistError(f"document directory '{documents_path}' does not exist")

        paths = await to_thread(lambda: sorted(documents_path.rglob("*")))
        indexed = 0

        self._logger.info(f"indexing {len(paths)} documents from '{documents_path}'")

        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".md", ".pdf", ".txt"}:
                continue

            # avoid symlinks that reference outside the documents' directory.
            if not path.resolve().is_relative_to(documents_path.resolve()):
                continue

            try:
                success = await self._index_file(documents_path=documents_path, path=path)

                if success:
                    indexed += 1
            except Exception as e:
                self._logger.error(f"failed to index document '{path}': {e}")

        return indexed
