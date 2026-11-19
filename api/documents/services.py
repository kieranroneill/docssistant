from asyncio import to_thread
from hashlib import sha256
from logging import Logger
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from chromadb.api.models.AsyncCollection import AsyncCollection
from langchain_text_splitters import RecursiveCharacterTextSplitter

from api.platform.agents.clients import AbstractEmbeddingsAgent
from api.platform.defaults.services import BaseService

from .errors import DocumentPathDoesNotExistError
from .repositories import Repository


class DocumentIndexerService(BaseService):
    _chunk_overlap: int
    _chunk_size: int
    _documents_repository: Repository
    _embeddings_agent: AbstractEmbeddingsAgent
    _splitter: RecursiveCharacterTextSplitter

    def __init__(
        self,
        chroma_collection: AsyncCollection,
        embeddings_agent: AbstractEmbeddingsAgent,
        logger: Logger,
    ):
        super().__init__(logger=logger)

        # TODO: make the chunks configurable
        self._chunk_overlap = 200
        self._chunk_size = 1500
        self._documents_repository = Repository(collection=chroma_collection, logger=logger)
        self._embeddings_agent = embeddings_agent
        self._splitter = RecursiveCharacterTextSplitter(chunk_size=self._chunk_size, chunk_overlap=self._chunk_overlap)

    ###
    # private methods
    ###

    async def _index_file(self, path: Path, documents_path: Path) -> bool:
        source = path.relative_to(documents_path).as_posix()
        document_id = str(uuid5(NAMESPACE_URL, f"docssistant:document_store:{source}"))
        content = await to_thread(path.read_text, encoding="utf-8")
        chunks = await to_thread(self._splitter.split_text, content)
        fingerprint = sha256(
            f"{self._embeddings_agent.model()}:{self._chunk_size}:{self._chunk_overlap}:v1\0{content}".encode("utf-8")
        ).hexdigest()
        ids = [f"{document_id}:{fingerprint}:{index}" for index in range(len(chunks))]
        existing_ids = set(await self._documents_repository.get_chunk_ids_by_document_id(document_id=document_id))

        if existing_ids == set(ids):
            self._logger.debug(f"document '{source}' is unchanged")

            return False

        self._logger.info(f"indexing document '{source}' ({len(chunks)} chunks)")

        for offset in range(0, len(chunks), 32):
            batch = chunks[offset : offset + 32]
            embeddings = await self._embeddings_agent.documents(texts=batch)

            if len(embeddings) != len(batch):
                raise ValueError(f"embedding count does not match chunk count for '{source}'")

            await self._documents_repository.upsert(
                ids=ids[offset : offset + 32],
                document_id=document_id,
                source=source,
                offset=offset,
                chunks=batch,
                embeddings=embeddings,
            )

        # remove stale chunks only after all replacement chunks were written
        await self._documents_repository.delete_chunks_by_ids(ids=sorted(existing_ids - set(ids)))

        return True

    ###
    # public methods
    ###

    async def index(self, documents_path: Path) -> int:
        if not documents_path.is_dir():
            raise DocumentPathDoesNotExistError(f"document directory '{documents_path}' does not exist")

        paths = await to_thread(lambda: sorted(documents_path.rglob("*")))
        indexed = 0

        self._logger.debug(f"indexing {len(paths)} documents from '{documents_path}'")

        for path in paths:
            if not path.is_file() or path.suffix.lower() not in {".txt", ".md"}:
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
