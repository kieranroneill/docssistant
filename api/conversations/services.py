from logging import Logger
from uuid import UUID, uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.platform.agents.clients import AbstractAgentClient
from api.platform.agents.dtos import Message
from api.platform.application.enums import ErrorCode
from api.platform.defaults.services import BaseService
from api.platform.http.responses import ErrorResponse

from .dtos import Conversation, ConversationMessage, Usage
from .repositories import ConversationMessageRepository, ConversationRepository


class Service(BaseService):
    _agent: AbstractAgentClient
    _conversation_message_repository: ConversationMessageRepository
    _conversation_repository: ConversationRepository

    def __init__(self, logger: Logger, agent: AbstractAgentClient, postgres: AsyncSession):
        super().__init__(logger=logger)

        self._agent = agent
        self._conversation_message_repository = ConversationMessageRepository(logger=logger, postgres=postgres)
        self._conversation_repository = ConversationRepository(logger=logger, postgres=postgres)

    ###
    # private methods
    ###

    async def _chat(self, query: str) -> Conversation:
        try:
            result = await self._agent.chat(
                messages=[
                    Message(
                        content=query,
                        role="user",
                    )
                ]
            )
        except Exception as e:
            self._logger.error(f"failed to get a response from the agent: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                    message="failed to get a response from the agent",
                ),
            )

        self._logger.debug(f"got a response from the agent: {result}")

        conversation_id = uuid4()
        sequence = 0
        conversation = Conversation(
            created_at=result.created_at,
            active=True,
            id=conversation_id,
            messages=[
                # user message
                ConversationMessage(
                    content=query,
                    conversation_id=conversation_id,
                    created_at=result.created_at,
                    id=uuid4(),
                    model=None,
                    role="user",
                    sequence_number=sequence,
                    usage=None,
                ),
                # assistant message
                ConversationMessage(
                    content=result.content,
                    conversation_id=conversation_id,
                    created_at=result.created_at,
                    id=uuid4(),
                    model=result.model,
                    role=result.role,
                    sequence_number=sequence + 1,
                    usage=Usage(
                        input_tokens=result.usage.input_tokens,
                        output_tokens=result.usage.output_tokens,
                        total_tokens=result.usage.total_tokens,
                    ),
                ),
            ],
            updated_at=result.created_at,
        )

        try:
            conversation = await self._conversation_repository.add(dto=conversation)
            conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation.id)

            if conversation is None:
                raise Exception("failed to save conversation")

            return conversation
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                    message="failed to save conversation",
                ),
            )

    async def _chat_with_conversation_id(self, query: str, conversation_id: UUID) -> Conversation:
        conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation_id)

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorResponse(
                    code=ErrorCode.CONVERSATION_NOT_FOUND_ERROR.value,
                    message=f"conversation '{conversation_id}' not found",
                ),
            )

        messages = [Message(content=message.content, role=message.role) for message in conversation.messages]

        messages.append(
            Message(
                content=query,
                role="user",
            )
        )

        try:
            result = await self._agent.chat(messages=messages)
        except Exception as e:
            self._logger.error(f"failed to get a response from the agent for conversation '{conversation_id}': {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                    message="failed to get a response from the agent",
                ),
            )

        sequence = len(conversation.messages) + 1

        try:
            await self._conversation_message_repository.bulk_add(
                dtos=[
                    # user message
                    ConversationMessage(
                        content=query,
                        conversation_id=conversation.id,
                        created_at=result.created_at,
                        id=uuid4(),
                        model=None,
                        role="user",
                        sequence_number=sequence,
                        usage=None,
                    ),
                    # assistant message
                    ConversationMessage(
                        content=result.content,
                        conversation_id=conversation.id,
                        created_at=result.created_at,
                        id=uuid4(),
                        model=result.model,
                        role=result.role,
                        sequence_number=sequence + 1,
                        usage=Usage(
                            input_tokens=result.usage.input_tokens,
                            output_tokens=result.usage.output_tokens,
                            total_tokens=result.usage.total_tokens,
                        ),
                    ),
                ]
            )

            conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation.id)

            if conversation is None:
                raise Exception("failed to save conversation")

            return conversation
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    code=ErrorCode.INTERNAL_SERVER_ERROR.value,
                    message="failed to save conversation",
                ),
            )

    ###
    # public methods
    ###

    async def chat(
        self,
        query: str,
        conversation_id: UUID | None = None,
    ) -> Conversation:
        # initiate a new conversation
        if conversation_id is None:
            return await self._chat(query=query)

        return await self._chat_with_conversation_id(query=query, conversation_id=conversation_id)
