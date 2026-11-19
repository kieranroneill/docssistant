import os
from logging import Logger

import chromadb
from chromadb.api.models.AsyncCollection import AsyncCollection


class ChromaClient:
    _collection: AsyncCollection | None
    _collection_name: str
    _host: str
    _logger: Logger
    _port: int

    def __init__(self, logger: Logger):
        collection = os.environ["CHROMA_COLLECTION"]

        if not collection:
            raise ValueError("CHROMA_COLLECTION environment variable is not set")

        host = os.environ["CHROMA_HOST"]

        if not host:
            raise ValueError("CHROMA_HOST environment variable is not set")

        port = os.environ["CHROMA_PORT"]

        if not port:
            raise ValueError("CHROMA_PORT environment variable is not set")

        self._collection = None
        self._collection_name = collection
        self._host = host
        self._port = int(port)
        self._logger = logger

    ##
    # public methods
    ##

    async def initialize(self) -> None:
        chroma = await chromadb.AsyncHttpClient(
            host=self._host,
            port=self._port,
        )

        self._collection = await chroma.get_or_create_collection(
            name=self._collection_name,
            embedding_function=None,
            metadata={"hnsw:space": "cosine"},
        )

    async def collection(self) -> AsyncCollection:
        if self._collection is None:
            raise RuntimeError("client has not been initialized: call 'initialize()'")

        return self._collection
