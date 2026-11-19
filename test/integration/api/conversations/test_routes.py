from logging import Logger
from test.mocks.agents.clients import MockChatAgent, MockEmbeddingsAgent
from uuid import uuid4, uuid5

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.app import app
from api.conversations.dtos import (
    Conversation,
    ConversationMessage,
    ConversationSource,
    Usage,
)
from api.conversations.repositories import ConversationRepository
from libs.application.enums import ErrorCode
from libs.datetime.utilities import now, to_iso_string
from libs.documents.dtos import DocumentMatch
from libs.logging.utilities import get_logger


@pytest.fixture
def logger() -> Logger:
    return get_logger()


@pytest.fixture(autouse=True)
def agents(
    logger: Logger,
    mocker,
):
    mocker.patch(
        "api.app.ChatAgent",
        return_value=MockChatAgent(logger=logger),
    )
    mocker.patch(
        "api.app.EmbeddingsAgent",
        return_value=MockEmbeddingsAgent(logger=logger),
    )


class TestChatEndpoint:
    def test_should_fail_with_empty_query(
        self,
        logger: Logger,
    ) -> None:
        with TestClient(app) as client:
            result = client.post(
                "/api/conversations/chat",
                json={"query": ""},
            )

        assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert result.json()["detail"][0]["loc"] == ["body", "query"]

    def test_should_fail_if_no_conversation_exists(
        self,
        logger: Logger,
    ) -> None:
        with TestClient(app) as client:
            result = client.post(
                f"/api/conversations/{uuid4()}/chat",
                json={"query": "Say hello in one short sentence."},
            )

        assert result.status_code == status.HTTP_404_NOT_FOUND
        assert result.json()["detail"]["code"] == ErrorCode.CONVERSATION_NOT_FOUND_ERROR.value

    async def test_should_use_an_existing_conversation(
        self,
        logger: Logger,
        mocker,
    ) -> None:
        conversation_id = uuid4()
        query = "Can you tell me a joke?"
        response = "I can show you a joke, go look in the mirror."
        chat_agent = MockChatAgent(
            chat_response=response,
            logger=logger,
        )

        # save a conversation to the database
        async with app.state.postgres.create_session() as postgres:
            repository = ConversationRepository(
                logger=logger,
                postgres_session=postgres,
            )
            created_at = to_iso_string(now())

            await repository.add(
                dto=Conversation(
                    created_at=created_at,
                    active=True,
                    id=conversation_id,
                    messages=[
                        # user message
                        ConversationMessage(
                            content="Say hello in one short sentence.",
                            conversation_id=conversation_id,
                            created_at=created_at,
                            id=uuid4(),
                            model=None,
                            role="user",
                            sequence_number=0,
                            sources=[],
                            usage=None,
                        ),
                        # assistant message
                        ConversationMessage(
                            content="Hello! How can I help you today?",
                            conversation_id=conversation_id,
                            created_at=created_at,
                            id=uuid4(),
                            model=chat_agent.model(),
                            role="assistant",
                            sequence_number=1,
                            sources=[
                                ConversationSource(
                                    chunk_index=0,
                                    document_id=uuid5(uuid4(), "a cool doc"),
                                    id=uuid4(),
                                    page_number=34,
                                    reference=0,
                                    source="the interent",
                                ),
                            ],
                            usage=Usage(
                                input_tokens=30,
                                output_tokens=313,
                                total_tokens=343,
                            ),
                        ),
                    ],
                    updated_at=created_at,
                )
            )

        # setup mocks
        mocker.patch(
            "api.app.ChatAgent",
            return_value=chat_agent,
        )
        mocker.patch(
            "api.conversations.services.DocumentChunkRepository.search",
            return_value=[
                DocumentMatch(
                    chunk_index=0,
                    content="Hello! How can I help you today?",
                    distance=0.0,
                    document_id="test-document",
                )
            ],
        )

        with TestClient(app) as client:
            result = client.post(
                f"/api/conversations/{str(conversation_id)}/chat",
                json={"query": query},
            )

        assert result.status_code == status.HTTP_201_CREATED

        response_body = result.json()

        async with app.state.postgres.create_session() as postgres:
            repository = ConversationRepository(
                logger=logger,
                postgres_session=postgres,
            )
            conversation = await repository.get_by_id_with_messages(_id=response_body["id"])

            assert conversation is not None
            assert len(conversation.messages) == 4
            assert any(message.role == "user" and message.content == query for message in conversation.messages)
            assert any(message.role == "assistant" and message.content == response for message in conversation.messages)

    async def test_should_create_a_new_conversation(
        self,
        logger: Logger,
        mocker,
    ) -> None:
        query = "Say hello in one short sentence."
        response = "Hello! How can I help you today?"

        mocker.patch(
            "api.app.ChatAgent",
            return_value=MockChatAgent(
                chat_response=response,
                logger=logger,
            ),
        )
        mocker.patch(
            "api.conversations.services.DocumentChunkRepository.search",
            return_value=[
                DocumentMatch(
                    chunk_index=0,
                    content="Hello! How can I help you today?",
                    distance=0.0,
                    document_id="test-document",
                )
            ],
        )

        with TestClient(app) as client:
            result = client.post(
                "/api/conversations/chat",
                json={"query": query},
            )

        assert result.status_code == status.HTTP_201_CREATED

        response_body = result.json()

        async with app.state.postgres.create_session() as postgres:
            repository = ConversationRepository(
                logger=logger,
                postgres_session=postgres,
            )
            conversation = await repository.get_by_id_with_messages(_id=response_body["id"])

            assert conversation is not None
            assert len(conversation.messages) == 2
            assert any(message.role == "user" and message.content == query for message in conversation.messages)
            assert any(message.role == "assistant" and message.content == response for message in conversation.messages)
