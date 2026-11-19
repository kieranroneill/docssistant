from logging import Logger
from uuid import UUID

from chromadb.api.models.AsyncCollection import AsyncCollection
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from libs.agents.clients import ChatAgent, EmbeddingsAgent
from libs.agents.dependencies import get_chat_agent, get_embeddings_agent
from libs.chroma.dependencies import get_collection as get_chroma_collection
from libs.logging.dependencies import get_logger
from libs.postgres.dependencies import get_session as get_postgres_session

from .dtos import Conversation
from .requests import ChatRequest
from .services import Service

router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"],
)


@router.post(
    "/{conversation_id}/chat",
    response_model=Conversation,
    status_code=status.HTTP_201_CREATED,
)
async def chat_with_conversation_id(
    conversation_id: UUID,
    request: ChatRequest,
    chat_agent: ChatAgent = Depends(get_chat_agent),
    chroma_collection: AsyncCollection = Depends(get_chroma_collection),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> Conversation:
    service = Service(
        chat_agent=chat_agent,
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.chat(conversation_id=conversation_id, query=request.query)


@router.post(
    "/chat",
    response_model=Conversation,
    status_code=status.HTTP_201_CREATED,
)
async def chat(
    request: ChatRequest,
    chat_agent: ChatAgent = Depends(get_chat_agent),
    chroma_collection: AsyncCollection = Depends(get_chroma_collection),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> Conversation:
    service = Service(
        chat_agent=chat_agent,
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.chat(query=request.query)
