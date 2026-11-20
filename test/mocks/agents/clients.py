from logging import Logger

from libs.agents.clients import AbstractChatAgent, AbstractEmbeddingsAgent
from libs.agents.dtos import ChatMessage, ChatResult
from libs.datetime.utilities import now


class MockChatAgent(AbstractChatAgent):
    _chat_response: str | None

    def __init__(self, logger: Logger, chat_response: str | None = None) -> None:
        super().__init__(logger=logger)

        self._chat_response = chat_response

    ##
    # public methods
    ##

    async def chat(self, messages: list[ChatMessage]) -> ChatResult:
        return ChatResult(
            content=self._chat_response or "I am unable to help you with that request.",
            created_at=now(),
            input_tokens=0,
            model="test-chat-model",
            output_tokens=0,
            role="assistant",
            total_tokens=0,
        )

    def model(self) -> str:
        return "test-chat-model"

    def set_chat_response(self, chat_response: str) -> None:
        self._chat_response = chat_response


class MockEmbeddingsAgent(AbstractEmbeddingsAgent):
    _query_response: list[float] | None

    def __init__(self, logger: Logger, query_response: list[float] | None = None) -> None:
        super().__init__(logger=logger)

        self._query_response = query_response

    ##
    # public methods
    ##

    async def documents(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0] for _ in texts]

    async def query(self, query: str) -> list[float]:
        return [1.0, 0.0]

    def model(self) -> str:
        return "test-embeddings-model"

    def set_query_response(self, response: list[float]) -> None:
        self._query_response = response
