from uuid import UUID

from fastapi import APIRouter, Depends, status

from api.platform.agents.clients import AgentClient
from api.platform.agents.dependencies import get_agent

from .controllers import Controller
from .dtos import ConversationMessage
from .requests import ChatRequest

router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"],
)


@router.post(
    "/{conversation_id}/chat",
    response_model=ConversationMessage,
    status_code=status.HTTP_201_CREATED,
)
async def chat_with_conversation_id(
    conversation_id: UUID,
    request: ChatRequest,
    agent: AgentClient = Depends(get_agent),
) -> ConversationMessage:
    controller = Controller(agent=agent)

    return await controller.chat(conversation_id=conversation_id, query=request.query)


@router.post(
    "/chat",
    response_model=ConversationMessage,
    status_code=status.HTTP_201_CREATED,
)
async def chat(
    request: ChatRequest,
    agent: AgentClient = Depends(get_agent),
) -> ConversationMessage:
    controller = Controller(agent=agent)

    return await controller.chat(query=request.query)
