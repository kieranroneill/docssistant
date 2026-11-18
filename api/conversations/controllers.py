from uuid import UUID, uuid4

from fastapi import HTTPException, status

from api.platform.agents.clients import AgentClient
from api.platform.application.enums import ErrorCode
from api.platform.http.responses import ErrorResponse

from .dtos import ConversationMessage
from .models import ConversationMessageModel, ConversationModel


class Controller:
    def __init__(self, agent: AgentClient):
        self._agent = agent

    ###
    # private functions
    ###

    async def _chat(self, query: str) -> ConversationMessage:
        pass

    async def _chat_with_conversation_id(self, query: str, conversation_id: UUID) -> ConversationMessage:
        pass

    ###
    # public functions
    ###

    async def chat(
        self,
        query: str,
        conversation_id: UUID | None = None,
    ) -> ConversationMessage:
        if query == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    code=ErrorCode.FIELD_REQUIRED_ERROR.value,
                    message="field 'query' must not be empty",
                ),
            )

        # initiate a new conversation
        if conversation_id is None:
            return await self._chat(query=query)

        return await self._chat_with_conversation_id(query=query, conversation_id=conversation_id)
