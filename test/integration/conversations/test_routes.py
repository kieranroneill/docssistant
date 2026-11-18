from test.mocks.platform.agents.clients import MockAgentClient

import pytest
from fastapi.testclient import TestClient

from api.app import app
from api.platform.logging.utilities import get_logger


@pytest.fixture
def agent_client() -> MockAgentClient:
    return MockAgentClient(logger=get_logger())


class TestChatEndpoint:
    def test_with_empty_query(
        self,
        mocker,
        agent_client: MockAgentClient,
    ) -> None:
        mocker.patch(
            "api.app.AgentClient",
            return_value=agent_client,
        )

        with TestClient(app) as client:
            response = client.post(
                "/api/conversations/chat",
                json={"query": ""},
            )

        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "query"]
