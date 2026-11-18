from api.platform.agents.clients import AbstractAgentClient
from api.platform.agents.dtos import ChatResult, Message, Usage
from api.platform.datetime.utilities import timestamp


class MockAgentClient(AbstractAgentClient):
    _chat_response: str | None

    def __init__(self) -> None:
        self._chat_response = None

    ##
    # public methods
    ##

    async def chat(self, query: str, messages: list[Message]) -> ChatResult:
        return ChatResult(
            content=self._chat_response or "I am unable to help you with that request.",
            created_at=timestamp(),
            model="test_model",
            role="assistant",
            usage=Usage(
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
            ),
        )

    def set_chat_response(self, chat_response: str) -> None:
        self._chat_response = chat_response
