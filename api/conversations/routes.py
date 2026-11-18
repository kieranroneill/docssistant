from logging import Logger
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.platform.agents.clients import AgentClient
from api.platform.agents.dependencies import get_agent
from api.platform.logging.dependencies import get_logger
from api.platform.postgres.dependencies import get_postgres

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
    agent: AgentClient = Depends(get_agent),
    logger: Logger = Depends(get_logger),
    postgres: AsyncSession = Depends(get_postgres),
) -> Conversation:
    service = Service(agent=agent, logger=logger, postgres=postgres)

    return await service.chat(conversation_id=conversation_id, query=request.query)


@router.post(
    "/chat",
    response_model=Conversation,
    status_code=status.HTTP_201_CREATED,
)
async def chat(
    request: ChatRequest,
    agent: AgentClient = Depends(get_agent),
    logger: Logger = Depends(get_logger),
    postgres: AsyncSession = Depends(get_postgres),
) -> Conversation:
    service = Service(agent=agent, logger=logger, postgres=postgres)

    return await service.chat(query=request.query)
