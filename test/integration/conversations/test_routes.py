from logging import Logger
from test.mocks.platform.agents.clients import MockAgentClient
from uuid import uuid4

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from api.app import app
from api.conversations.repositories import ConversationRepository
from api.platform.application.enums import ErrorCode
from api.platform.logging.utilities import get_logger


@pytest.fixture
def logger() -> Logger:
    return get_logger()


class TestChatEndpoint:
    def test_should_fail_with_empty_query(
        self,
        logger: Logger,
        mocker,
    ) -> None:
        mocker.patch(
            "api.app.AgentClient",
            return_value=MockAgentClient(logger=logger),
        )

        with TestClient(app) as client:
            result = client.post(
                "/api/conversations/chat",
                json={"query": ""},
            )

        assert result.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
        assert result.json()["detail"][0]["loc"] == ["body", "query"]

    async def test_should_fail_if_no_conversation_exists(
        self,
        logger: Logger,
        mocker,
    ) -> None:
        mocker.patch(
            "api.app.AgentClient",
            return_value=MockAgentClient(
                logger=logger,
            ),
        )

        with TestClient(app) as client:
            result = client.post(
                f"/api/conversations/{uuid4()}/chat",
                json={"query": "Say hello in one short sentence."},
            )

        assert result.status_code == status.HTTP_404_NOT_FOUND
        assert result.json()["detail"]["code"] == ErrorCode.CONVERSATION_NOT_FOUND_ERROR.value

    async def test_should_create_a_new_conversation(
        self,
        logger: Logger,
        mocker,
    ) -> None:
        query = "Say hello in one short sentence."
        response = "Hello! How can I help you today?"

        mocker.patch(
            "api.app.AgentClient",
            return_value=MockAgentClient(
                chat_response=response,
                logger=logger,
            ),
        )

        with TestClient(app) as client:
            result = client.post(
                "/api/conversations/chat",
                json={"query": query},
            )

        assert result.status_code == status.HTTP_201_CREATED

        response_body = result.json()

        async with app.state.postgres_session_factory() as postgres:
            repository = ConversationRepository(
                logger=logger,
                postgres=postgres,
            )
            saved = await repository.get_by_id_with_messages(_id=response_body["id"])

            assert saved is not None
            assert saved.active is True
            assert str(saved.id) == response_body["id"]
            assert [(message.role, message.content) for message in saved.messages] == [
                ("user", query),
                ("assistant", response),
            ]
