from logging import Logger
from test.mocks.agents.clients import MockChatAgent, MockEmbeddingsAgent

import pytest


@pytest.fixture(autouse=True)
def agents(
    logger: Logger,
    mocker,
    embeddings_agent: MockEmbeddingsAgent,
    chat_agent: MockChatAgent,
):
    mocker.patch(
        "api.app.ChatAgent",
        return_value=chat_agent,
    )
    mocker.patch(
        "api.app.EmbeddingsAgent",
        return_value=embeddings_agent,
    )
