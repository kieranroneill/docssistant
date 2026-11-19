from logging import Logger
from uuid import UUID, uuid4

from chromadb.api.models.AsyncCollection import AsyncCollection
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from api.documents.repositories import Repository as DocumentsRepository
from api.platform.agents.clients import AbstractChatAgent, AbstractEmbeddingsAgent
from api.platform.agents.dtos import ChatMessage, ChatResult
from api.platform.application.errors import InternalServerError
from api.platform.datetime.utilities import now, to_iso_string
from api.platform.defaults.services import BaseService

from .dtos import Conversation, ConversationMessage, Usage
from .errors import ConversationNotFoundError
from .repositories import ConversationMessageRepository, ConversationRepository


class Service(BaseService):
    _chat_agent: AbstractChatAgent
    _conversation_message_repository: ConversationMessageRepository
    _conversation_repository: ConversationRepository
    _documents_repository: DocumentsRepository
    _embeddings_agent: AbstractEmbeddingsAgent

    def __init__(
        self,
        chat_agent: AbstractChatAgent,
        chroma_collection: AsyncCollection,
        embeddings_agent: AbstractEmbeddingsAgent,
        logger: Logger,
        postgres_session: AsyncSession,
    ):
        super().__init__(logger=logger)

        self._chat_agent = chat_agent
        self._documents_repository = DocumentsRepository(collection=chroma_collection, logger=logger)
        self._conversation_message_repository = ConversationMessageRepository(logger=logger, postgres=postgres_session)
        self._conversation_repository = ConversationRepository(logger=logger, postgres=postgres_session)
        self._embeddings_agent = embeddings_agent

    ###
    # private methods
    ###

    async def _call_agents(self, query: str, messages: list[ChatMessage]) -> ChatResult:
        self._logger.debug(f"calling embeddings agent '{self._embeddings_agent.model()}' with query: '{query}'")

        # first we get the embeddings from the embedding agent
        try:
            embeddings = await self._embeddings_agent.query(query=query)
        except Exception as e:
            self._logger.error(f"failed to get a response from the embedding agent: {e}")

            raise InternalServerError(message="failed to get a response from the embedding agent").to_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        matches = await self._documents_repository.search(embeddings=embeddings)

        # if not document chunk matches where found, there is no need to continue
        if not matches:
            self._logger.debug(f"no document chunks found for the query: '{query}'")

            return ChatResult(
                content="I couldn’t find relevant information in the available documents.",
                created_at=to_iso_string(now()),
                input_tokens=0,
                model="application",
                output_tokens=0,
                role="assistant",
                total_tokens=0,
            )

        excerpts = []

        # create extra context for the model with matched sources
        for number, match in enumerate(matches, start=1):
            location = match.source or match.document_id

            if match.page_number is not None:
                location += f", page {match.page_number}"

            excerpts.append(f"[{number}] {location}\n{match.content}")

        # update the query with document excerpts:
        #
        # Document excerpts:
        # [1] employee-handbook.pdf, PDF page 12
        # Employees receive 25 days of annual leave.
        #
        # Question:
        # How much annual leave do employees receive?
        context = "\n\n".join(excerpts)
        content = f"Document excerpts:\n{context}\n\nQuestion:\n{query}"

        self._logger.debug(
            f"calling chat agent '{self._chat_agent.model()}' with embedded query:\n" f"```\n" f"{content}\n" f"```"
        )

        _messages = messages.copy()

        _messages.append(
            ChatMessage(
                content=content,
                role="user",
            )
        )

        try:
            result = await self._chat_agent.chat(messages=_messages)
        except Exception as e:
            self._logger.error(f"failed to get a response from the chat agent: {e}")

            raise InternalServerError(message="failed to get a response from the chat agent").to_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return result

    async def _chat(self, query: str) -> Conversation:
        result = await self._call_agents(messages=[], query=query)
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
                        input_tokens=result.input_tokens,
                        output_tokens=result.output_tokens,
                        total_tokens=result.total_tokens,
                    ),
                ),
            ],
            updated_at=result.created_at,
        )

        try:
            conversation = await self._conversation_repository.add(dto=conversation)
            conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation.id)

            if conversation is None:
                raise Exception("conversation is empty")

            return conversation
        except Exception as e:
            self._logger.error(f"failed to save conversation '{conversation_id}': {e}")

            raise InternalServerError(message="failed to save conversation").to_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def _chat_with_conversation_id(self, query: str, conversation_id: UUID) -> Conversation:
        conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation_id)

        if conversation is None:
            raise ConversationNotFoundError(message=f"conversation '{conversation_id}' not found").to_http_exception(
                status_code=status.HTTP_404_NOT_FOUND
            )

        result = await self._call_agents(
            messages=[ChatMessage(content=message.content, role=message.role) for message in conversation.messages],
            query=query,
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
                            input_tokens=result.input_tokens,
                            output_tokens=result.output_tokens,
                            total_tokens=result.total_tokens,
                        ),
                    ),
                ]
            )

            conversation = await self._conversation_repository.get_by_id_with_messages(_id=conversation.id)

            if conversation is None:
                raise Exception

            return conversation
        except Exception:
            raise InternalServerError(message="failed to get a response from the agent").to_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
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
