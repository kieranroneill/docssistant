import os
from abc import ABC, abstractmethod
from logging import Logger

from langchain.agents import create_agent
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langgraph.graph.state import CompiledStateGraph

from api.platform.datetime.utilities import now, to_iso_string

from .dtos import ChatResult, Message, Usage


class AbstractAgentClient(ABC):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    ##
    # public methods
    ##
    @abstractmethod
    async def chat(self, messages: list[Message]) -> ChatResult:
        pass

    @abstractmethod
    def chat_model(self) -> str:
        pass

    @abstractmethod
    def embeddings_model(self) -> str:
        pass


class AgentClient(AbstractAgentClient):
    _chat_model: ChatOllama
    _embeddings_model: OllamaEmbeddings

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

        base_url = os.environ["OLLAMA_BASE_URL"]

        if base_url is None:
            raise ValueError("OLLAMA_BASE_URL environment variable is not set")

        chat_model_name = os.environ["OLLAMA_CHAT_MODEL"]

        if chat_model_name is None:
            raise ValueError("OLLAMA_CHAT_MODEL environment variable is not set")

        embeddings_model_name = os.environ["OLLAMA_EMBEDDING_MODEL"]

        if embeddings_model_name is None:
            raise ValueError("OLLAMA_EMBEDDING_MODEL environment variable is not set")

        chat_model = ChatOllama(
            base_url=base_url,
            model=chat_model_name,
            temperature=0,
        )
        embeddings_model = OllamaEmbeddings(
            base_url=base_url,
            model=embeddings_model_name,
        )

        self.chat_model = chat_model
        self._embeddings_model = embeddings_model

    async def chat(self, messages: list[Message]) -> ChatResult:
        agent: CompiledStateGraph = create_agent(
            model=self._chat_model,
            system_prompt="""
            You are a helpful assistant.
            """,
        )
        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "content": message.content,
                        "role": message.role,
                    }
                    for message in messages
                ]
            }
        )
        last = result["messages"][-1]
        content = last.content or ""
        metadata = last.response_metadata or {}
        model = metadata.get("model") or metadata.get("model_name") or self._chat_model.model
        usage = last.usage_metadata or {}

        return ChatResult(
            content=content,
            created_at=metadata.get("created_at", to_iso_string(now())),
            model=model,
            role="assistant",
            usage=Usage(
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                total_tokens=usage.get("total_tokens", 0),
            ),
        )

    def chat_model(self) -> str:
        return self._chat_model.model

    def embeddings_model(self) -> str:
        return self._embeddings_model.model
