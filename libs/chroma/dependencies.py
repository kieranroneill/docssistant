from chromadb.api.models.AsyncCollection import AsyncCollection
from fastapi import Request

from .clients import ChromaClient


async def get_collection(request: Request) -> AsyncCollection:
    chroma: ChromaClient = request.app.state.chroma

    return await chroma.collection()
