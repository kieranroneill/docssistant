from chromadb.api.models.Collection import Collection
from fastapi import Request

from .clients import ChromaClient


async def get_collection(request: Request) -> Collection:
    chroma: ChromaClient = request.app.state.chroma

    return await chroma.collection()
