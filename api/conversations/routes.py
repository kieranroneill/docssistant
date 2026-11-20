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

from .requests import ChatRequest
from .responses import ConversationResponse, ConversationWithMessagesResponse
from .services import Service

router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"],
)


@router.get(
    "",
    description="Get the list of conversations",
    response_model=list[ConversationResponse],
    status_code=status.HTTP_200_OK,
)
async def conversations(
    chat_agent: ChatAgent = Depends(get_chat_agent),
    chroma_collection: AsyncCollection = Depends(get_chroma_collection),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> list[ConversationResponse]:
    service = Service(
        chat_agent=chat_agent,
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.conversations()


@router.get(
    "/{conversation_id}",
    description="Get conversation by the {conversation_id}",
    response_model=ConversationWithMessagesResponse,
    status_code=status.HTTP_200_OK,
)
async def conversation_by_id(
    conversation_id: UUID,
    chat_agent: ChatAgent = Depends(get_chat_agent),
    chroma_collection: AsyncCollection = Depends(get_chroma_collection),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> ConversationWithMessagesResponse:
    service = Service(
        chat_agent=chat_agent,
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.conversation_by_id(_id=conversation_id)


@router.post(
    "/{conversation_id}/chat",
    description="Sends a new query to the existing conversation",
    response_model=ConversationWithMessagesResponse,
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
) -> ConversationWithMessagesResponse:
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
    description="Initiates a new conversation",
    response_model=ConversationWithMessagesResponse,
    status_code=status.HTTP_201_CREATED,
)
async def chat(
    request: ChatRequest,
    chat_agent: ChatAgent = Depends(get_chat_agent),
    chroma_collection: AsyncCollection = Depends(get_chroma_collection),
    embeddings_agent: EmbeddingsAgent = Depends(get_embeddings_agent),
    logger: Logger = Depends(get_logger),
    postgres_session: AsyncSession = Depends(get_postgres_session),
) -> ConversationWithMessagesResponse:
    service = Service(
        chat_agent=chat_agent,
        chroma_collection=chroma_collection,
        embeddings_agent=embeddings_agent,
        logger=logger,
        postgres_session=postgres_session,
    )

    return await service.chat(query=request.query)
